from datetime import datetime

from highlights import repository
from shared import BitrixApiCli
from shared.bitrix_cli.banners import BannerTypeEnum

class HighlightsService:
    repository = repository.CollectionRepository()
    bitrix_api = BitrixApiCli()

    def get_highlights(
            self, _type: BannerTypeEnum,
    ):
        collections = self.get_collections()
        for collection in collections:
            collection.elements = self.get_banners(collection.bitrix_elements_id, _type)
        return collections

    def get_active_highlights(
            self, _type: BannerTypeEnum,
    ):
        collections = self.get_active_collections()
        for collection in collections:
            collection.elements = self.get_active_banners(collection.bitrix_elements_id, _type)
        return collections

    def get_collections(self):
        return self.repository.get_all().only(
            "name", "picture", "active_from", "active_to", "sort", "bitrix_elements_id"
        )

    def get_active_collections(self):
        return self.repository.filter(
            active_to="gte",
            active_from="lte",
        ).only(
            "name", "picture", "active_from", "active_to", "sort", "bitrix_elements_id"
        )

    def get_banners(self, _id, _type: BannerTypeEnum):
        return self.bitrix_api.banners.get_banners(_id, type)

    def get_active_banners(self, _id, _type: BannerTypeEnum):
        data = self.bitrix_api.banners.get_active_banners(_id, type)

        for banner in data:
            if banner["active_from"] > datetime.now().timestamp() or banner["active_to"] < datetime.now().timestamp():
                data.remove(banner)

        return data

