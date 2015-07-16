
import redis
import msgpack
import hashlib

from findspire import settings

CONN = redis.StrictRedis(settings.REDIS_HOST, settings.REDIS_PORT, settings.REDIS_DB["escache"])


def fetch_from_cache(key):
	data = CONN.get(key)
	if data is not None:
		return msgpack.unpackb(data)
	return None

def cache_es_results(results, prefix, query, expiry, **kwds):
	key = generate_es_cache_key(prefix, query, **kwds)
	CONN.setex(key, expiry, msgpack.packb(results))
	return results

def generate_es_cache_key(prefix, query, **kwds):
	if isinstance(prefix, (list, tuple)):
		prefix = "/".join(map(unicode, prefix))

	obj = [query]
	for k, v in sorted(kwds.iteritems(), key=lambda x: x[0]):
		obj.append((k, v))
	return unicode(prefix) + "/" + hashlib.md5(msgpack.packb(obj)).hexdigest()

def cached_es_search(es_client, prefix, query, expiry, **kwds):
	key = generate_es_cache_key(prefix, query, **kwds)
	results = fetch_from_cache(key)
	if results is not None:
		return results, "hit"

	results = es_client.search(query, **kwds)
	cache_es_results(results, prefix, query, expiry, **kwds)
	return results, "miss"
