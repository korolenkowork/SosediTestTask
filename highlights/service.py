from datetime import datetime

from django.utils import timezone

from highlights import repository
from shared import BitrixApiCli
from shared.bitrix_cli.banners import BannerTypeEnum

class HighlightsService:
    repository = repository.CollectionRepository()
    bitrix_api = BitrixApiCli()

    # Can't optimize those for use DRF build-in pagination :(
    # def get_highlights(
    #         self, _type: BannerTypeEnum,
    # ):
    #     collections = self.get_collections()
    #     for collection in collections:
    #         collection.elements = self.get_banners(collection.bitrix_elements_id, _type)
    #     return collections
    #
    # def get_active_highlights(
    #         self, _type: BannerTypeEnum,
    # ):
    #     collections = self.get_active_collections()
    #     for collection in collections:
    #         collection.elements = self.get_active_banners(collection.bitrix_elements_id, _type)
    #     return collections

    def get_highlight(self, _id, _type: BannerTypeEnum):
        collection = self.repository.filter(pk=_id).only(
            "name", "picture", "active_from", "active_to", "sort",
        ).first()
        collection.elements = self.get_active_banners(collection.bitrix_elements_id, _type)
        return collection

    def get_active_highlight(self, _id, _type: BannerTypeEnum):
        now = timezone.now()
        collection = self.repository.filter(
            pk=_id,
            active_from__lte=now,
            active_to__gte=now,
        ).only(
            "name", "picture", "active_from", "active_to", "sort",
        ).first()
        collection.elements = self.get_active_banners(collection.bitrix_elements_id, _type)
        return collection

    def get_collections(self):
        return self.repository.get_all().only(
            "name", "picture", "active_from", "active_to", "sort", "bitrix_elements_id"
        )

    def get_active_collections(self):
        now = timezone.now()
        return self.repository.filter(
            active_from__lte=now,
            active_to__gte=now,
        ).only(
            "name", "picture", "active_from", "active_to", "sort",
        )

    def get_active_collection(self, _id, _type: BannerTypeEnum):
        now = timezone.now()
        collection = self.repository.get_by_id(
            _id,
            active_from__lte=now,
            active_to__gte=now,
        ).only(
            "name", "picture", "active_from", "active_to", "sort",
        )

        collection.elements = self.get_active_banners(collection.bitrix_elements_id, _type)

    def get_banners(self, _id, _type: BannerTypeEnum):
        return self.bitrix_api.banners.get_banners(_id, type)

    def get_active_banners(self, _id, _type: BannerTypeEnum):
        data = self.bitrix_api.banners.get_banners(_id, type)
        now = datetime.now()

        for banner in data[::-1]:
            if banner.active_from and banner.active_from > now:
                data.remove(banner)
            if banner.active_to and banner.active_to < now:
                data.remove(banner)

        return data

