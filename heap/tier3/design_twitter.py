"""Design Twitter
https://leetcode.com/problems/design-twitter/

Tier 3 — prepare if you have time · Heap / Priority Queue

Support `post_tweet`, `get_news_feed` (the 10 most recent tweets from the user
and everyone they follow, newest first), `follow`, and `unfollow`.

A merge of k sorted streams — the same shape as Merge k Sorted Lists.

Example:
    Input:  post_tweet(1, 5), get_news_feed(1), follow(1, 2), post_tweet(2, 6)
    Output: [5], then [6, 5]

Run: python heap/tier3/design_twitter.py
"""


class Twitter:
    def __init__(self) -> None:
        # TODO: implement
        raise NotImplementedError

    def post_tweet(self, user_id: int, tweet_id: int) -> None:
        raise NotImplementedError

    def get_news_feed(self, user_id: int) -> list[int]:
        """The 10 most recent tweet ids visible to `user_id`, newest first."""
        raise NotImplementedError

    def follow(self, follower_id: int, followee_id: int) -> None:
        raise NotImplementedError

    def unfollow(self, follower_id: int, followee_id: int) -> None:
        raise NotImplementedError


if __name__ == "__main__":
    twitter = Twitter()
    twitter.post_tweet(1, 5)
    assert twitter.get_news_feed(1) == [5]
    twitter.follow(1, 2)
    twitter.post_tweet(2, 6)
    assert twitter.get_news_feed(1) == [6, 5]
    twitter.unfollow(1, 2)
    assert twitter.get_news_feed(1) == [5]
    print("ok")
