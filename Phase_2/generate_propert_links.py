from models import PropertyLinks, Suburbs
from database_worker import DataBase
import asyncio
from loguru import logger


async def start():
    logger.info('START')
    base = DataBase()
    suburb_rows = base.get_all_rows(classname=Suburbs)
    logger.info('QUERY: OK')
    for row in suburb_rows:
        suburb_id = row.id
        suburb = row.suburb
        state = row.state
        postcode = row.postcode

        convert = lambda x: x.lower().strip().replace(' ', '+')

        url_buy = f'https://www.realestate.com.au/buy/in-{convert(suburb)},+{state.lower()}+{postcode}/list-1'
        url_rent = f'https://www.realestate.com.au/rent/in-{convert(suburb)},+{state.lower()}+{postcode}/list-1'
        url_sold = f'https://www.realestate.com.au/sold/in-{convert(suburb)},+{state.lower()}+{postcode}/list-1'

        await base.save_row(
            {
                'saburb_id': suburb_id,
                'url_buy': url_buy,
                'url_rent': url_rent,
                'url_sold': url_sold,
            },
            PropertyLinks
        )

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())