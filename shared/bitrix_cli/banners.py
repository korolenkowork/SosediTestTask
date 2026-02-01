import enum
from datetime import datetime
from typing import Optional

import requests
from django.core.cache import cache
from pydantic import BaseModel as PydanticBaseModel
from pydantic import field_validator, ValidationInfo
import pydantic

class BannerItem(PydanticBaseModel):
    preview_picture: str
    id: str
    name: str
    banner_area: str
    url: Optional[str] = None
    button_text: Optional[str] = None
    button_link: Optional[str] = None
    active_from: Optional[datetime] = None
    active_to: Optional[datetime] = None
    sort: str

    @field_validator("preview_picture", mode="after")
    @classmethod
    def add_base_url(
            cls,
            value: Optional[str],
            info: ValidationInfo,
    ) -> Optional[str]:
        if not value:
            return value

        base_url = info.context.get("base_url") if info.context else None
        if base_url and value.startswith("/"):
            return f"{base_url}{value}"
        return value

class BannerTypeEnum(enum.StrEnum):
    DESKTOP = "desktop"
    MOBILE = "mobile"

class BitrixBannersApiCli:
    cache_key = "bitrix:banners:"

    def __init__(self, client):
        self.cli = client

    def get_banners(self, _id, _type: BannerTypeEnum):
        cache_key = f"{self.cache_key}{_id}"
        data = cache.get(cache_key)

        if data is None:
            url = f"{self.cli.base_url}/local/api/banners.php?id={_id}"
            response = requests.get(url)
            data = response.json()
            cache.set(cache_key, data, self.cli.cache_timeout)

        # Serialize banners too needed type
        if _type == BannerTypeEnum.DESKTOP:
            for banner in data:
                if banner.get("picture_desktop", None) is None:
                    continue

                banner["preview_picture"] = banner["picture_desktop"]
                del banner["picture_desktop"]
                if banner.get("picture_phone", None):
                    del banner["picture_phone"]

        if _type == BannerTypeEnum.MOBILE:
            for banner in data:
                if banner.get("picture_phone", None) is None:
                    continue

                banner["preview_picture"] = banner["picture_phone"]
                del banner["picture_phone"]
                if banner.get("picture_desktop", None):
                    del banner["picture_desktop"]

        banners = []
        for banner in data:
            try:
                _banner = BannerItem.model_validate(banner, context={"base_url": self.cli.base_url})
                banners.append(_banner)
            except pydantic.ValidationError:
                continue
        return banners
