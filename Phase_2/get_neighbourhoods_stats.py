from fetcher import request
from models import Suburbs, InvestorMetrics, Polygons, Suburbs_exception, InvestorMetricsExceptions, SuburbStateRatio
import asyncio
from database_worker import DataBase
import urllib
import json
from loguru import logger
from config import RANDOM_PROXIES
from sqlalchemy import and_
from time import sleep

API_URL = 'https://investor-api.realestate.com.au/v2/states/{}/suburbs/{}.json?embed=suburb_geo'
SUPLY_AND_DEMAND_URL = 'https://investor-api.realestate.com.au/v2/states/{}/suburbs/{}/postcodes/{}/supply_demand.json'


class PhaseTwo:

    def __init__(self):
        self.base = DataBase()
        logger.info('self.base = DataBase()')

    async def start(self):
        for limit in range(10, 7060, 10):
            suburb_rows = self.base.get_rows(classname=Suburbs,
                                             row_limit=limit,
                                             filter_=and_(Suburbs.id < limit + 1, Suburbs.id > limit - 10))
            for row in suburb_rows:
                logger.info(f'Start: {row.id=}')

            # await self.get_data_from_phase_one(suburb_rows)
            task = [self.get_suburb_state_ratio(row) for row in suburb_rows]
            await asyncio.wait(task)
            for x in range(-2, 0):
                logger.info(f'sleep({str(x).strip("-")})')
                sleep(1)

    async def get_data_from_phase_one(self, suburb_rows):
        task = [self.get_response_from_realestate_api(row.id,
                                                      row.postcode,
                                                      row.suburb,
                                                      API_URL.format(
                                                          urllib.parse.quote(row.state.lower()),
                                                          urllib.parse.quote(row.suburb.lower()))
                                                      ) for row in suburb_rows]
        logger.info('await asyncio.wait(task)')
        await asyncio.wait(task)

    async def get_suburb_state_ratio(self, row):
        url = SUPLY_AND_DEMAND_URL.format(
            urllib.parse.quote(row.state.lower()),
            urllib.parse.quote(row.suburb.lower()),
            row.postcode
        )
        r = await request('GET', url, proxies=RANDOM_PROXIES())

        if r.status_code == 404:
            logger.info(f'{404}, {url}')
            return
        json_response = json.loads(r.text)
        await self.base.save_row(
            {
                'saburb_id': row.id,
                'visits_per_property_of_suburb': json_response.get('suburb_ratio'),
                'average_of_State': json_response.get('state_ratio'),
                'url_api': url,
            },
            SuburbStateRatio
        )

    async def get_response_from_realestate_api(self, row_id: int, postcode: str, suburb: str, url: str) -> None:
        r = await request('GET', url, proxies=RANDOM_PROXIES())
        if r.status_code == 404:
            logger.info(f'{404}, {url}')
            await self.except_404_save(row_id)
        try:
            json_response = json.loads(r.text)
        except Exception as e:
            logger.debug(e)
            return

        first_key = f'{suburb.upper()}-{postcode}'
        try:
            house, unit, polygon, metro = PhaseTwo.parse_json_response(json_response.get(first_key))

            logger.info('Ceate task for POLYGON')
            polygon_task = [self.base.save_row(
                {
                    'saburb_id': row_id,
                    'polygon': str(polygon),
                },
                Polygons
            )]
            logger.info('await asyncio.wait(polygon_task)')
            await asyncio.wait(polygon_task)

            if house:
                logger.info('Create task for HOUSE')
                house_task = [self.save_investor_metrics(
                    'HOUSE', bedrooms, metro, row_id, investor_metrics.get('investor_metrics')
                )
                    for bedrooms, investor_metrics in house.get('bedrooms').items()]
                logger.info('await asyncio.wait(house_task)')
                await asyncio.wait(house_task)

            if unit:
                logger.info('Create task for UNIT')
                unit_task = [self.save_investor_metrics(
                    'UNIT', bedrooms, metro, row_id, investor_metrics.get('investor_metrics')
                )
                    for bedrooms, investor_metrics in unit.get('bedrooms').items()]
                logger.info('await asyncio.wait(unit_task)')
                await asyncio.wait(unit_task)

        except Exception as e:
            logger.debug(e)
            await self.base.save_row(
                {
                    'saburb_id': row_id,
                    'url': url,
                    'exception': str(e),

                },
                InvestorMetricsExceptions
            )

    @staticmethod
    def parse_json_response(json_response) -> tuple:
        house = json_response.get('property_types').get('HOUSE')
        unit = json_response.get('property_types').get('UNIT')
        polygon = json_response.get('polygon')
        metro = json_response.get('details').get('metro')

        return house, unit, polygon, metro

    async def save_investor_metrics(self, property_type: str, bedrooms: str,
                                    metro: str, row_id, investor_metrics: dict) -> None:
        row = {
            'saburb_id': row_id,
            'property_types': property_type,
            'bedrooms': bedrooms,
            'median_sold_price': investor_metrics.get('median_sold_price'),
            'median_sold_price_five_years_ago': investor_metrics.get('median_sold_price_five_years_ago'),
            "median_rental_price": investor_metrics.get('median_rental_price'),
            "rental_yield": investor_metrics.get('rental_yield'),
            "annual_growth": investor_metrics.get('annual_growth'),
            "rental_demand": investor_metrics.get('rental_demand'),
            "rental_properties": investor_metrics.get('rental_properties'),
            "sold_properties": investor_metrics.get('sold_properties'),
            "sold_properties_five_years_ago": investor_metrics.get('sold_properties_five_years_ago'),
            'metro': metro,
        }
        await self.base.save_row(row, InvestorMetrics)

    async def except_404_save(self, row_id):
        row = {
            'saburb_id': row_id,
            'property_types': None,
            'bedrooms': None,
            'median_sold_price': None,
            'median_sold_price_five_years_ago': None,
            "median_rental_price": None,
            "rental_yield": None,
            "annual_growth": None,
            "rental_demand": None,
            "rental_properties": None,
            "sold_properties": None,
            "sold_properties_five_years_ago": None,
            'metro': None,
        }
        await self.base.save_row(row, InvestorMetrics)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(PhaseTwo().start())
