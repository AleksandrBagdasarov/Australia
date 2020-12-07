import requests
import json
from fetcher import request
from database_worker import DataBase
from models import Suburbs, SoldPropertyData
from loguru import logger
from time import sleep
from sqlalchemy import and_
from config import RANDOM_PROXIES
import urllib
import asyncio


# def test(suburb: str, state: str, postcode: str, page: int):
#     URL = "https://services.realestate.com.au/services/listings/search?query={%22channel%22:%22sold%22,%22filters%22:{%22surroundingSuburbs%22:%22false%22,%22geoPrecision%22:%22address%22,%22excludeAddressHidden%22:%22false%22,%22localities%22:[{%22searchLocation%22:%22"
#     URL += f"{suburb},%20{state}%20{postcode}%22"
#     URL += "}]},%22pageSize%22:%22200%22,%20%22page%22:%22"
#     URL += f"{page}"
#     URL += "%22}"
#     payload = {}
#     headers = {
#         'authority': 'services.realestate.com.au',
#         'cache-control': 'max-age=0',
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
#     }
#
#     response = requests.request("GET", URL, headers=headers, data=payload)
#
#     json_response = json.loads(response.text)
#     next_url = json_response.get('_links').get('next').get('href')
#     results = json_response.get('tieredResults')[0].get('results')
#     for data in results:
#         agent_name = data.get('lister').get('name')
#         agent_pic_url = data.get('lister').get('mainPhoto')  # .get('uri')
#         agency_name = data.get('agency').get('name')
#         agency_logo_url = data.get('agency').get('logo')  # .get('images')[0].get('uri')
#         price = data.get('price').get('display')
#         address = data.get('address').get('streetAddress')
#         number_of_bedrooms = data.get('features').get('general').get('bedrooms')
#         number_of_bathrooms = data.get('features').get('general').get('bathrooms')
#         number_of_car_spaces = data.get('features').get('general').get('parkingSpaces')
#         sold_date = data.get('dateSold').get('display')
#         url_to_listing = data.get('_links').get('prettyUrl').get('href')
#         url_of_default_hero_image = data.get('mainImage').get('uri')
#
#         construction_status = data.get('constructionStatus')
#         property_type = data.get('propertyType')
#         property_type_group = data.get('propertyTypeGroup')
#         agency_web_site = data.get('agency').get('website')
#         print(agent_name, '\n', agent_pic_url, '\n', agency_name, '\n', agency_logo_url, '\n', price, '\n', address,
#               '\n', number_of_bedrooms, '\n', number_of_bathrooms, '\n', number_of_car_spaces, '\n', sold_date, '\n',
#               url_to_listing, '\n', url_of_default_hero_image)
#         print('-' * 100)
#
#     print(len(results))
#     print(next_url)


class CollectSoldPropertyData:
    HEADERS = {
        'authority': 'services.realestate.com.au',
        'cache-control': 'max-age=0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }

    def __init__(self):
        self.base = DataBase()

    async def start(self):
        for limit in range(10, 7060, 10):
            suburb_rows = self.base.get_rows(
                classname=Suburbs,
                row_limit=limit,
                filter_=and_(Suburbs.id < limit + 1, Suburbs.id > limit - 10))
            for row in suburb_rows:
                logger.info(f'Start: {row.id=}')

            task = [self.start_pagination(row) for row in suburb_rows]
            await asyncio.wait(task)
            for x in range(-3, 0):
                logger.info(f'sleep({str(x).strip("-")})')
                sleep(1)

    async def start_pagination(self, row):
        r = await request(
            'GET',
            url=self.generate_url(
                suburb=row.suburb,
                state=row.state,
                postcode=row.postcode,
                page=1),
            proxies=RANDOM_PROXIES(),
            headers=self.HEADERS
        )

        await self.parse(r, row.id)

    async def parse(self, response, suburb_id):
        json_response = json.loads(response.text)
        page_num = json_response.get('pagination').get('page')
        max_page_num = json_response.get('pagination').get('maxPageNumberAvailable')
        if page_num > max_page_num:
            logger.debug(f'{page_num} > {max_page_num}')
            return
        next_url = json_response.get('_links').get('next').get('href')
        results = json_response.get('tieredResults')[0].get('results')
        for data in results:
            agent_name=self.get_agent_name(data=data)
            dict_data = dict(
                suburb_id=suburb_id,
                agent_name=agent_name,
                agent_pic_url=self.join_domain_1000x750(self.get_agent_pic_url(data=data, agent_name=agent_name)),
                agency_name=data.get('agency').get('name'),
                agency_logo_url=self.join_domain(self.get_agency_logo_url(data=data)),
                price=data.get('price').get('display'),
                address=data.get('address').get('streetAddress'),
                number_of_bedrooms=data.get('features').get('general').get('bedrooms'),
                number_of_bathrooms=data.get('features').get('general').get('bathrooms'),
                number_of_car_spaces=data.get('features').get('general').get('parkingSpaces'),
                sold_date=data.get('dateSold').get('display'),
                url_to_listing=data.get('_links').get('prettyUrl').get('href'),
                url_of_default_hero_image=self.join_domain_1000x750(self.get_hero_image(data=data)),

                construction_status=data.get('constructionStatus'),
                property_type=data.get('propertyType'),
                property_type_group=data.get('propertyTypeGroup'),
                agency_web_site=data.get('agency').get('website'),
            )
            await self.save(dict_data=dict_data)
        if next_url:
            logger.info(next_url)
            r = await request(
                'GET',
                next_url,
                proxies=RANDOM_PROXIES(),
                headers=self.HEADERS)
            await self.parse(r, suburb_id)

    async def save(self, dict_data: dict):
        await self.base.save_row(
            dict_data,
            SoldPropertyData
        )

    @staticmethod
    def generate_url(suburb: str, state: str, postcode: str, page: int):
        url = "https://services.realestate.com.au/services/listings/search?query={%22channel%22:%22sold%22,%22filte" \
              "rs%22:{%22surroundingSuburbs%22:%22false%22,%22geoPrecision%22:%22address%22,%22excludeAddressHidden%" \
              "22:%22false%22,%22localities%22:[{%22searchLocation%22:%22"
        url += f"{urllib.parse.quote(suburb)},%20{state}%20{postcode}%22"
        url += "}]},%22pageSize%22:%22200%22,%20%22page%22:%22"
        url += f"{page}"
        url += "%22}"
        return url

    @staticmethod
    def get_agent_pic_url(data: dict, agent_name: str) -> str:
        if data.get('lister').get('mainPhoto'):
            return data.get('lister').get('mainPhoto').get('uri')

        if data.get('listers'):
            for profile in data.get('listers'):
                if profile.get('mainPhoto') and agent_name == profile.get('name'):
                    return profile.get('mainPhoto').get('uri')

    @staticmethod
    def get_agency_logo_url(data):
        if data.get('agency').get('logo'):
            if data.get('agency').get('logo').get('links'):
                agency_logo_url = data.get('agency').get('logo').get('links').get('default')
                return agency_logo_url

    @staticmethod
    def get_agent_name(data: dict) -> str:
        if data.get('lister').get('name') is not None:
            return data.get('lister').get('name')

        if data.get('listers'):
            for profile in data.get('listers'):
                if profile.get('name'):
                    return profile.get('name')


    @staticmethod
    def get_hero_image(data: dict) -> str:
        if data.get('mainImage'):
            return data.get('mainImage').get('uri')

    @staticmethod
    def join_domain_1000x750(uri: str) -> str:
        if uri:
            return 'https://i2.au.reastatic.net/1000x750' + uri

    @staticmethod
    def join_domain(uri: str) -> str:
        if uri:
            return 'https://i2.au.reastatic.net' + uri


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(CollectSoldPropertyData().start())
    # test('Beaconsfield', 'VIC', '3807', 2)
