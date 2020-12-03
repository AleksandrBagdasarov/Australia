from fetcher import request
from models import Suburbs, SuburbsStats
import asyncio
from database_worker import DataBase
import urllib
import json


API_URL = 'https://investor-api.realestate.com.au/v2/states/{}/suburbs/{}.json?embed=suburb_geo'
SUPLY_AND_DEMAND_URL = 'https://investor-api.realestate.com.au/v2/states/{}/suburbs/{}/postcodes/2026/supply_demand.json'


async def get_data_from_phase_one():
    suburb_rows = DataBase().get_all_rows(Suburbs)
    for row in suburb_rows:
        row_id = row.id
        postcode = row.postcode
        suburb = row.suburb
        suburb_for_url = urllib.parse.quote(suburb.lower())
        state = row.state
        state_for_url = urllib.parse.quote(state.lower())
        url = API_URL.format(state_for_url, suburb_for_url)
        await get_response_from_realestate_api(row_id, postcode, suburb, url)


async def get_response_from_realestate_api(row_id: int, postcode: str, suburb: str, url: str) -> None:
    first_key = f'{suburb.upper()}-{postcode}'
    r = await request('GET', url)
    json_response = json.loads(r.text)
    house = json_response.get(first_key).get('property_types').get('HOUSE').get('bedrooms')
    unit = json_response.get(first_key).get('property_types').get('UNIT').get('bedrooms')
    print(house)

async def get_main_data():
    pass



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_data_from_phase_one())
