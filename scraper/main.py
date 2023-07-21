import aiohttp
import asyncio
import functools
from sanic import Sanic
from sanic.response import json
from redis import asyncio as aioredis
import json as _json


app = Sanic(__name__)

REDIS_CONFIG = {
    'host': "redis_db",
    'port': 6379,
    'db': 0,
    'password': None,
}


API_URL = 'https://search.imdbot.workers.dev/'
SKIP_KEYS = {'#IMDB_IV'}

ENSUNER_RESOURCES = {
    'session': lambda: aiohttp.ClientSession(),
    'redis': lambda: aioredis.Redis(**REDIS_CONFIG)
}

def ensurer(resource):
    def __wrapper__(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            if not hasattr(app.ctx, resource):
                handler = ENSUNER_RESOURCES.get(resource, lambda: None)
                attr = await handler() if asyncio.iscoroutinefunction(handler) else handler()
                setattr(app.ctx, resource, attr)
            return await func(*args, **kwargs)
        return wrapped
    return __wrapper__


def reformat_key(key):
    return key[1::].lower()

@ensurer('session')
@ensurer('redis')
async def search_imdb(query):
    results = []
    cached_byes = await app.ctx.redis.get(query)
    if cached_byes:
        cached = _json.loads(cached_byes)
        return cached

    async with app.ctx.session.get(API_URL, params={'q': query}) as resp:
        if resp.status == 200:
            response = await resp.json()
    if 'ok' in response and response['ok']:
        results = response['description']
    results = [{reformat_key(k): v for k, v in result.items() if k not in SKIP_KEYS} for result in results]
    data = {
        'success': bool(results),
        'query': query,
        'results': results,
    }

    if results:
        await app.ctx.redis.set(query, _json.dumps(results))
        await app.ctx.redis.expire(query, 60 * 60 * 24 * 7) # une semaine
    return data


@app.route('/search')
async def search(request):
    query = request.args.get('q')
    if not query:
        return json({'error': 'Missing query parameter'}, status=400)
    results = await search_imdb(query)
    return json(results)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4242)
