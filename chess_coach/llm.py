"""The connection to the model: one request shape, made carefully.

Everything that knows about Anthropic's API lives in this file. `tutor.py`
knows only that it can hand over a system prompt, some messages, and a JSON
schema, and get a dict back. That split is what lets the whole coaching layer
be tested at full fidelity with no network and no key — `FakeBackend` satisfies
the same three-method surface the real one does.

Two properties are worth stating outright, because they are the ones that would
otherwise be discovered the hard way:

**Missing credentials are not an error.** The book coach is complete on its own.
If there is no key, `resolve()` returns a reason string instead of a client, the
AI commands say what to set, and every other mode behaves exactly as before.

**Every reply is schema-constrained JSON.** Not prose that gets scraped for a
move. The alternative — asking for prose and hunting for something that looks
like `Nf3` — fails on the two cases that matter most: prose that names a move
inside a variation, and prose that names no move at all.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Sequence

DEFAULT_MODEL = "claude-opus-5"

# Tutor answers are a paragraph and a move. The cap is a latency and cost
# choice, not a guess at how long the answer needs to be: a coach that writes
# two thousand words has misunderstood the job.
MAX_TOKENS = 4000


class LLMUnavailable(RuntimeError):
    """No usable client, or the call failed. Always carries a readable reason."""


# --- configuration ---------------------------------------------------------
@dataclass(frozen=True)
class Config:
    """Where to send the request, resolved once from the environment.

    Two deployments are supported because two are what people actually have:
    a first-party API key, and Claude served through Google Vertex (which is
    how most corporate access is wired). `provider="vertex"` is chosen
    automatically when the Vertex project is set and no API key is, so in a
    shell that already has the Vertex variables exported this needs no setup.
    """

    provider: str  # "anthropic" | "vertex"
    model: str = DEFAULT_MODEL
    project: Optional[str] = None
    region: str = "global"
    base_url: Optional[str] = None
    skip_auth: bool = False  # the gateway authenticates, not this process

    @classmethod
    def from_env(cls, env: Optional[Dict[str, str]] = None) -> "Config":
        env = dict(os.environ if env is None else env)
        wanted = env.get("CHESS_COACH_PROVIDER", "auto").lower()
        vertex_project = env.get("ANTHROPIC_VERTEX_PROJECT_ID") or None
        if wanted == "auto":
            has_key = bool(env.get("ANTHROPIC_API_KEY"))
            wanted = "vertex" if vertex_project and not has_key else "anthropic"
        return cls(
            provider=wanted,
            model=env.get("CHESS_COACH_MODEL") or DEFAULT_MODEL,
            project=vertex_project,
            region=env.get("CLOUD_ML_REGION") or "global",
            base_url=env.get("ANTHROPIC_VERTEX_BASE_URL")
            if wanted == "vertex"
            else env.get("ANTHROPIC_BASE_URL"),
            skip_auth=(env.get("CLAUDE_CODE_SKIP_VERTEX_AUTH") or "").lower()
            in ("1", "true", "yes"),
        )

    def missing(self, env: Optional[Dict[str, str]] = None) -> Optional[str]:
        """Why a call would fail right now, or None if it would work."""
        env = dict(os.environ if env is None else env)
        if self.provider == "vertex":
            if not self.project:
                return "Vertex needs ANTHROPIC_VERTEX_PROJECT_ID."
            return None
        if not env.get("ANTHROPIC_API_KEY") and not env.get("ANTHROPIC_AUTH_TOKEN"):
            return (
                "No credentials. Export ANTHROPIC_API_KEY, or set "
                "ANTHROPIC_VERTEX_PROJECT_ID to use a Vertex deployment."
            )
        return None

    def describe(self) -> str:
        where = "Vertex" if self.provider == "vertex" else "Anthropic API"
        return f"{self.model} via {where}"


# --- the real backend ------------------------------------------------------
class AnthropicBackend:
    """One method, `ask_json`, over the Messages API.

    Requests stream even though nothing is displayed as it arrives. Streaming
    is what keeps a slow, thinking-heavy answer from tripping the SDK's HTTP
    timeout, and the deltas double as a progress signal for the caller's
    spinner — which matters here, because a chess question at `high` effort can
    take the better part of a minute and a frozen terminal reads as a hang.
    """

    def __init__(self, config: Optional[Config] = None) -> None:
        self.config = config or Config.from_env()
        self._client: Any = None

    # The client is built on first use, not in __init__, so that constructing a
    # Tutor never fails and never costs an import of a heavy SDK.
    def _connect(self) -> Any:
        if self._client is not None:
            return self._client
        reason = self.config.missing()
        if reason:
            raise LLMUnavailable(reason)
        try:
            import anthropic
        except ImportError as exc:  # pragma: no cover - depends on the install
            raise LLMUnavailable(
                "The anthropic package is not installed. `pip install anthropic`"
            ) from exc

        if self.config.provider == "vertex":
            kwargs: Dict[str, Any] = {
                "project_id": self.config.project,
                "region": self.config.region,
            }
            if self.config.base_url:
                kwargs["base_url"] = self.config.base_url
            if self.config.skip_auth:
                # The gateway signs the request. Passing a token — any token —
                # is what stops the SDK reaching for Google credentials that
                # are not there and do not need to be.
                kwargs["access_token"] = "gateway"
            self._client = anthropic.AnthropicVertex(**kwargs)
        else:
            kwargs = {}
            if self.config.base_url:
                kwargs["base_url"] = self.config.base_url
            self._client = anthropic.Anthropic(**kwargs)
        return self._client

    def ask_json(
        self,
        *,
        system: str,
        messages: Sequence[Dict[str, Any]],
        schema: Dict[str, Any],
        effort: str = "medium",
        max_tokens: int = MAX_TOKENS,
        on_progress: Optional[Callable[[], None]] = None,
    ) -> Dict[str, Any]:
        import json

        import anthropic

        client = self._connect()
        try:
            with client.messages.stream(
                model=self.config.model,
                max_tokens=max_tokens,
                # The system prompt is the same on every call in a session —
                # the persona, the house style, and the repertoire index. Ask
                # for it to be cached; whether it lands depends on it clearing
                # the model's minimum cacheable prefix, and nothing breaks if
                # it does not.
                system=[
                    {
                        "type": "text",
                        "text": system,
                        "cache_control": {"type": "ephemeral"},
                    }
                ],
                messages=list(messages),
                # Explicit rather than defaulted: on Opus 5 omitting `thinking`
                # already means adaptive, but this file should still do the
                # right thing if CHESS_COACH_MODEL points somewhere older.
                thinking={"type": "adaptive"},
                output_config={
                    "effort": effort,
                    "format": {"type": "json_schema", "schema": schema},
                },
            ) as stream:
                for _chunk in stream.text_stream:
                    if on_progress:
                        on_progress()
                message = stream.get_final_message()
        except anthropic.APIError as exc:
            raise LLMUnavailable(f"{type(exc).__name__}: {exc}") from exc
        except Exception as exc:  # network, auth, anything the SDK lets through
            raise LLMUnavailable(f"{type(exc).__name__}: {exc}") from exc

        if message.stop_reason == "refusal":
            raise LLMUnavailable("The model declined to answer that one.")

        text = next((b.text for b in message.content if b.type == "text"), "")
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            # Should not happen — the schema is enforced server-side — but a
            # coach that raises a JSONDecodeError at the learner is no coach.
            raise LLMUnavailable(f"Unreadable reply from the model: {exc}") from exc


# --- the test backend ------------------------------------------------------
class FakeBackend:
    """A scripted stand-in with the same surface as `AnthropicBackend`.

    Holds the replies to hand out in order and records every call, so the
    prompt-building and the grounding checks can both be tested exactly as they
    run in production. The tutor never learns which one it is talking to.
    """

    def __init__(self, replies: Sequence[Dict[str, Any]]) -> None:
        self.replies: List[Dict[str, Any]] = list(replies)
        self.calls: List[Dict[str, Any]] = []
        self.config = Config(provider="fake", model="fake-model")

    def ask_json(self, **kwargs: Any) -> Dict[str, Any]:
        self.calls.append(kwargs)
        if not self.replies:
            raise LLMUnavailable("FakeBackend ran out of scripted replies")
        return self.replies.pop(0)


def resolve(
    config: Optional[Config] = None, env: Optional[Dict[str, str]] = None
) -> "tuple[Optional[AnthropicBackend], Optional[str]]":
    """(backend, None) if a call could work, or (None, reason) if it could not.

    Returning the reason rather than raising is deliberate: "there is no AI
    coach today, and here is the one line that would fix it" is information the
    learner should get once at startup, not an exception at the moment they
    first ask a question.

    `env` exists so a test can describe an environment instead of inheriting
    whichever variables the developer happens to have exported.
    """
    config = config or Config.from_env(env)
    reason = config.missing(env)
    if reason:
        return None, reason
    return AnthropicBackend(config), None
