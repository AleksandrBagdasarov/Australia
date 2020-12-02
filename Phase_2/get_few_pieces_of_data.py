from fetcher import request
from models import Suburbs, SuburbsStats
import asyncio
from database_worker import DataBase

API_URL = 'https://investor-api.realestate.com.au/v2/states/nsw/suburbs/bondi%20beach.json?embed=suburb_geo'
SUPLY_AND_DEMAND_URL = 'https://investor-api.realestate.com.au/v2/states/nsw/suburbs/bondi%20beach/postcodes/2026/supply_demand.json'


async def start():
    suburbs = DataBase.get_all_rows(Suburbs)
    for suburb in suburbs:
        url = suburb.suburb_url

async def get_main_data():
    pass



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())