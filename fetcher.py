'''
This file makes asynchronous requests
To use this script, import the request function,
example of use "response = await request('GET', https://example.com)"
'''

import asyncio

import httpx
from httpx import Response
from loguru import logger


DEFAULT_HEADERS = {
  'authority': 'www.realestate.com.au',
  'cache-control': 'max-age=0',
  'dnt': '1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'sec-fetch-site': 'none',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-user': '?1',
  'sec-fetch-dest': 'document',
  'accept-language': 'ru,ru-RU;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6',
  'cookie': 'search_bedroom=all; search_property_type=house; search_channel=buy; search_drag_position=1; reauid=17f95568be3900002560c75f65020000ea070000; Country=UA; AMCVS_341225BE55BBF7E17F000101%40AdobeOrg=1; _gid=GA1.3.672220649.1606901800; s_vi=[CS]v1|2FE3B0138515811E-6000082685D55CDE[CE]; s_ecid=MCMID%7C50673403711262848240820956556905343738; AMCV_341225BE55BBF7E17F000101%40AdobeOrg=-330454231%7CMCIDTS%7C18599%7CMCMID%7C50673403711262848240820956556905343738%7CMCAAMLH-1607506599%7C6%7CMCAAMB-1607506599%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1606908999s%7CNONE%7CMCAID%7C2FE3B0138515811E-6000082685D55CDE%7CvVersion%7C3.1.2; s_cc=true; KP_UID=fd090057-8cc4-4617-6aa2-4b0eec162216; _readc=ap-southeast-1; JSESSIONID=D2B380BF8F125BA3D745B6889280C1AA; AWSELB=BD21ABD912FD962534A86FF37C471AF8CEA612D2DA2EA79D0C4C2C0C12582F925E886BFF2BB607515787BA3BFAD1466B91E84AC8C2DE168C5E7C67D28B4D50BC2C1536034B; AWSELBCORS=BD21ABD912FD962534A86FF37C471AF8CEA612D2DA2EA79D0C4C2C0C12582F925E886BFF2BB607515787BA3BFAD1466B91E84AC8C2DE168C5E7C67D28B4D50BC2C1536034B; s_sq=%5B%5BB%5D%5D; QSI_HistorySession=https%3A%2F%2Fwww.realestate.com.au%2Fneighbourhoods%2Fbondi-beach-2026-nsw~1606905962114%7Chttps%3A%2F%2Fwww.realestate.com.au%2Fneighbourhoods%2Fbondi-2026-nsw~1606906375988%7Chttps%3A%2F%2Fwww.realestate.com.au%2Fneighbourhoods%2Fabbotsford-3067-vic~1606906488948%7Chttps%3A%2F%2Fwww.realestate.com.au%2Fneighbourhoods%2Fnorth-bondi-2026-nsw~1606906756381; utag_main=v_id:017622cf97b90002bb6f53e7af8403073002106b00bd0$_sn:2$_ss:0$_st:1606908557974$vapi_domain:realestate.com.au$dc_visit:2$ses_id:1606905880277%3Bexp-session$_pn:9%3Bexp-session$dc_event:11%3Bexp-session$dc_region:ap-southeast-2%3Bexp-session; _ga_F962Q8PWJ0=GS1.1.1606905855.2.1.1606906773.0; _ga=GA1.1.805465356.1606901799; KP_UIDz=DJ%2FCpm0PhqNMjWjSKy%2BJ7w%3D%3D%3A%3AXqGSm2hIuYD03JAP4dDfBBjWnDzkZxrMoqgLfUK9tGaEt1GBAu4hzfIyefRIwlshBSVdw7HfXyzeNshoqcKfSkwphrETyJ2tCytpVj9Vl6F451YnuL%2BSswSBAABIkglN0rzVwM08qSq%2BPif0oGtppFSt46P%2F%2Bt4IbvWnDwTX%2BknZbEFSFTgEAlPuZEulcqsFt0tce34xtO4eWWr069nBDDU%2Fa2RGqqD5P%2BrGAWKPFK0pOLsSQhMf8IAMgcoBZsOa52FvTzBxgp9pFYYEE20TKolOdSLQuu1YbRCNQXfk7he0fEnZypTHJPTrgaA0dNDfV6L2Zs42FnAFLdAbjWMcTc%2FHpjllG1a9S8luHN4%2FG2vvk7QosMCYkSEsJZnUTbpim2aSQOxkvafefS%2B5lVm%2BBigZa99j1BixpAaK%2B091MO6JAXm8%2FIuB5mJMW%2BPNFY4Uk0qqzkoqUogXqqrTqV%2B%2Bl4tUUg4paxE4NWnmxEyO9OirY9rDhGwZGBy8kO9S5SbrH9F6KxwJNbWbFffBTS1duwQu060QIZiN04CQy%2FHj3ko%3D; KP_UID=fd090057-8cc4-4617-6aa2-4b0eec162216; KP_UIDz=N3D9eZ4hnR2nEcx9SmtvDw%3D%3D%3A%3AbCUID1EdW2BxX3Zn5sXSDdqszNSkMhVOnTgAi%2FJOjb9fbRcu7bOSbV0NZ2MP5xBlk3plXGnmpdrI8CuHSJXad0b0k77amxmfjzQFZnID6ChOVDJMq3wIw%2FZtZnyy2v7Hv9eja7cd8HcUwFrfwhd9xXAdESCOCloep9pWWUDRCY8v2YqaxWTewDBpeMlZXyMwq0RJpeP2%2Bbbc3Gp2DY4atkPTxcV3rVfeZEfyfneG5Q93Ib0ZdXTl2RhawGiPCHMnead5hysUkIM30DBgHxS16PZjJbGhoUgGD%2Br3uiqxrFmygg%2FjytlTUyts9RKHAvbu%2Bv%2F2sgsccU%2B6fHIdzUFazbsTSmzXslOoMNZZYVR9AYz8XY7gmy87frqIwhVx0klimbyfctbVwsNuBTNLps3pevxtP%2FAckz15R8jjg74SdGPCd3JgLKB2GJka98aBtaXPP0%2BemPQ9WQnriAOHagQ%2Bfnht4wJTFzPN%2BGPDkhEfuavC7kJRZcWF2q33IYKpcyX%2BNbS8lX2VLwPnvaVZznJMORlXmz6o3%2Bwy%2F%2Fr2SFhS1ec%3D; Country=UA'
}


async def request(method: str,
                  url: str,
                  allow_status_codes: list = (200, 404),
                  retries: int = 10,
                  proxies: str = None,
                  timeout: int = 90,
                  headers: dict = DEFAULT_HEADERS,
                  **kwargs) -> Response:
    for _ in range(retries + 1):
        logger.info(f'{method}: {url}')
        if proxies:
            async with httpx.AsyncClient(verify=False, timeout=timeout, headers=headers) as client:
                response = await client.request(method, url, **kwargs)
        else:
            async with httpx.AsyncClient(proxies=proxies, verify=False, timeout=timeout, headers=headers) as client:
                response = await client.request(method, url, **kwargs)
        try:
            assert response.status_code in allow_status_codes
            return response

        except AssertionError:
            logger.debug(f'{method}: {url} {response.status_code}')
            await asyncio.sleep(3)
