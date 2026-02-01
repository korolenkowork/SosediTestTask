
from django.conf import settings

from shared.bitrix_cli.banners import BitrixBannersApiCli

class BitrixApiCli:
    base_url = settings.BITRIX_URL
    cache_timeout = settings.BITRIX_CACHE_TIMEOUT

    def __init__(self):
        self.banners = BitrixBannersApiCli(self)
        # self.other = BitrixOtherApiCli(self)

    def auth(self):
        pass
