import time

from app.knowledge.cache import CacheEntry, RetrievalCache


def test_cache_entry_without_ttl_does_not_expire():
    entry = CacheEntry(
        key="x",
        value="result",
        created_at=0,
    )

    assert not entry.is_expired(now=10_000)


def test_cache_entry_expires_after_ttl():
    entry = CacheEntry(
        key="x",
        value="result",
        created_at=100,
        ttl_seconds=10,
    )

    assert not entry.is_expired(now=109)
    assert entry.is_expired(now=110)


def test_cache_key_is_deterministic():
    first = RetrievalCache.make_key(
        "  find authentication  ",
        {"language": "python", "top_k": 5},
    )

    second = RetrievalCache.make_key(
        "find authentication",
        {"top_k": 5, "language": "python"},
    )

    assert first == second


def test_different_queries_have_different_keys():
    first = RetrievalCache.make_key("authentication")
    second = RetrievalCache.make_key("database")

    assert first != second


def test_cache_set_and_get():
    cache = RetrievalCache()

    cache.set("query-1", ["result-a"])

    assert cache.get("query-1") == ["result-a"]
    assert len(cache) == 1


def test_cache_miss_returns_none():
    cache = RetrievalCache()

    assert cache.get("missing") is None


def test_cache_delete():
    cache = RetrievalCache()

    cache.set("query-1", "result")

    assert cache.delete("query-1")
    assert cache.get("query-1") is None
    assert not cache.delete("query-1")


def test_cache_clear():
    cache = RetrievalCache()

    cache.set("a", 1)
    cache.set("b", 2)

    cache.clear()

    assert len(cache) == 0
    assert cache.get("a") is None


def test_expired_entry_is_removed():
    cache = RetrievalCache(default_ttl_seconds=0)

    cache.set("query", "result")

    time.sleep(0.01)

    assert cache.get("query") is None
    assert len(cache) == 0
