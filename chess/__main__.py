"""Entry point so the game can be launched with `python -m chess`."""

from __future__ import annotations


def main() -> None:
    try:
        from .gui import run
    except ImportError as exc:  # tkinter missing on some Python builds
        raise SystemExit(
            "tkinter is required to run the chess GUI.\n"
            "On macOS with Homebrew Python, install it with:\n"
            "    brew install python-tk\n"
            f"(original error: {exc})"
        )
    run()


if __name__ == "__main__":
    main()
