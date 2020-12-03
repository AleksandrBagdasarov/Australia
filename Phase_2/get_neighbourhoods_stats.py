from fetcher import request
from models import Suburbs, InvestorMetrics
import asyncio
from database_worker import DataBase
import urllib
import json
from loguru import logger
from config import RANDOM_PROXIES


API_URL = 'https://investor-api.realestate.com.au/v2/states/{}/suburbs/{}.json?embed=suburb_geo'
SUPLY_AND_DEMAND_URL = 'https://investor-api.realestate.com.au/v2/states/{}/suburbs/{}/postcodes/2026/supply_demand.json'


class PhaseTwo:

    def __init__(self):
        self.base = DataBase()
        logger.info('self.base = DataBase()')

    async def get_data_from_phase_one(self):
        suburb_rows = DataBase().get_rows(Suburbs, 10)
        logger.info('suburb_rows = DataBase().get_all_rows(Suburbs)')

        task = [self.get_response_from_realestate_api(row.id,
                                                      row.postcode,
                                                      row.suburb,
                                                      API_URL.format(
                                                          urllib.parse.quote(row.state.lower()),
                                                          urllib.parse.quote(row.suburb.lower()))
                                                      ) for row in suburb_rows]
        logger.info('await asyncio.wait(task)')
        await asyncio.wait(task)
        # for row in suburb_rows:
        #     row_id = row.id
        #     postcode = row.postcode
        #     suburb = row.suburb
        #     suburb_for_url = urllib.parse.quote(suburb.lower())
        #     state = row.state
        #     state_for_url = urllib.parse.quote(state.lower())
        #     url = API_URL.format(state_for_url, suburb_for_url)
        #     await InvestorMetrics.get_response_from_realestate_api(row_id, postcode, suburb, url)

    async def get_response_from_realestate_api(self, row_id: int, postcode: str, suburb: str, url: str) -> None:
        r = await request('GET', url, proxies=RANDOM_PROXIES())
        json_response = json.loads(r.text)
        first_key = f'{suburb.upper()}-{postcode}'
        house = json_response.get(first_key).get('property_types').get('HOUSE').get('bedrooms')
        unit = json_response.get(first_key).get('property_types').get('UNIT').get('bedrooms')
        logger.info('Create task for HOUSE')
        task = [self.save_investor_metrics('HOUSE', bedrooms, row_id, investor_metrics) for bedrooms, investor_metrics in house.items()]
        logger.info('await asyncio.wait(task)')
        await asyncio.wait(task)
        logger.info('Create task for UNIT')
        task = [self.save_investor_metrics('UNIT', bedrooms, row_id, investor_metrics) for bedrooms, investor_metrics in unit.items()]
        logger.info('await asyncio.wait(task)')
        await asyncio.wait(task)

    async def save_investor_metrics(self, property_type: str, bedrooms: str, row_id, investor_metrics: dict) -> None:
        row = {
            'saburb': row_id,
            'property_types': property_type,
            'bedrooms': bedrooms,
            'median_sold_price': investor_metrics.get('median_sold_price'),
            'median_sold_price_five_years_ago': investor_metrics.get('median_rental_price'),
            "rental_yield": investor_metrics.get('rental_yield'),
            "annual_growth": investor_metrics.get('annual_growth'),
            "rental_demand": investor_metrics.get('rental_demand'),
            "rental_properties": investor_metrics.get('rental_properties'),
            "sold_properties": investor_metrics.get('sold_properties'),
            "sold_properties_five_years_ago": investor_metrics.get('sold_properties_five_years_ago')
        }
        await self.base.save_row(row, InvestorMetrics)
        logger.info(f'await self.base.save_row({row_id}, InvestorMetrics)')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(PhaseTwo().get_data_from_phase_one())
