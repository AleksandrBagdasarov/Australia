from fetcher import request
from parsel import Selector
import asyncio
from loguru import logger
from database_worker import DataBase
import re
from models import Suburbs, Suburbs_exception


START_URLS = (
    # 'https://www.realestate.com.au/neighbourhoods/sitemap_vic.xml',
    # 'https://www.realestate.com.au/neighbourhoods/sitemap_nsw.xml',
    # 'https://www.realestate.com.au/neighbourhoods/sitemap_qld.xml',
    # 'https://www.realestate.com.au/neighbourhoods/sitemap_wa.xml',
    # 'https://www.realestate.com.au/neighbourhoods/sitemap_tas.xml',
    # 'https://www.realestate.com.au/neighbourhoods/sitemap_sa.xml',
    # 'https://www.realestate.com.au/neighbourhoods/sitemap_act.xml',
    # 'https://www.realestate.com.au/neighbourhoods/sitemap_nt.xml',
)


async def start(url):
    logger.info(f'START FOR {url}')
    r = await request('GET', url)
    with open('../test.html', 'w') as f:
        f.write(r.text)
    tree = Selector(r.text)
    links = tree.xpath('//loc/text()').extract()
    links_without_duplicate = set(links)
    for link in links_without_duplicate:
        try:
            state = re.search(r'\w+$', link).group().upper()
            postcode = re.search(r'-\d+-', link).group().strip('-')
            suburb = re.sub(r'-\d+-\w+$', '', link).split('/')[-1].replace('-', ' ').title()
            data = {
                'suburb_url': link,
                'suburb': suburb,
                'state': state,
                'postcode': postcode,
            }
            await DataBase(1).save_row(data, Suburbs)
        except Exception as e:
            data = {
                'suburb_url': link
            }
            await DataBase(1).save_row(data, Suburbs_exception)
            logger.debug(f'{e}')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start(START_URLS[0]))

