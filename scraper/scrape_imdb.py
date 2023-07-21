import aiohttp
import asyncio
from bs4 import BeautifulSoup


BASE_API = 'https://api.graphql.imdb.com'

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
}


async def get_imdb_info(session, search_term):
    search_headers = headers.copy()
    search_headers['content-type'] = 'application/json'
    search_headers['x-imdb-client-name'] = 'imdb-web-next-localized'
    search_headers['x-imdb-client-rid'] =  'GMWB2HTY5ST7XP8RVKAT'
    search_headers['x-imdb-user-country'] = 'US'
    search_headers['x-imdb-user-language'] = 'en-US'
    search_headers[ 'x-imdb-weblab-treatment-overrides'] = '{"IMDB_DESKTOP_SEARCH_ALGORITHM_UPDATES_577300":"T1"}'

    params = {
        "operationName": 'RVI_Items',
        "variables": {
            "count": 15,
            "locale": "en-US"
        },
        "extensions": {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": "06ef5eeaad7b4dfef53d3d3dfe78693efb8826f806b4f006a2dcc485e258b9fd"
            }
        }
    }
    async with session.post(BASE_API, json=params, headers=headers) as response:
        if response.status == 200:
            data = await response.json()
            print(data)
        else:
            return None

async def main():
    async with aiohttp.ClientSession() as session:
        imdb_id = await get_imdb_info(session, 'the matrix')
        print(imdb_id)

run = asyncio.run(main())
