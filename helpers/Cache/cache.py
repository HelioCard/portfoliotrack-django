from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter

class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    pass

session = CachedLimiterSession(
    limiter=Limiter(RequestRate(2, Duration.SECOND*1)),  # max 2 requests per 1 second(S)
    bucket_class=MemoryQueueBucket,
    backend=SQLiteCache("yfinance.cache"),
    expire_after=3600,

)

session.cache.delete(expired=True)