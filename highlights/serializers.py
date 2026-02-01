from rest_framework import serializers

from highlights import models
from highlights.service import HighlightsService
from shared.bitrix_cli.banners import BannerTypeEnum


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Collection
        fields = 'name', 'picture', 'active_from', 'active_to', 'sort'

class BannerSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    preview_picture = serializers.CharField(max_length=255)
    banner_area = serializers.CharField(max_length=255)
    url = serializers.CharField(max_length=255)
    button_text = serializers.CharField(max_length=255, required=False)
    button_link = serializers.CharField(max_length=255, required=False)
    active_from = serializers.DateTimeField()
    active_to = serializers.DateTimeField()
    sort = serializers.CharField(max_length=255)

class HighlightSerializer(serializers.ModelSerializer):
    """
    Used for single highlight serialization
    """
    class Meta:
        model = models.Collection
        fields = 'name', 'picture', 'active_from', 'active_to', 'sort', 'elements'

    elements = BannerSerializer(many=True)


class MobileMultipleHighlightsSerializer(serializers.ModelSerializer):
    """
    Used for multiple highlights serialization
    """
    class Meta:
        model = models.Collection
        fields = 'name', 'picture', 'active_from', 'active_to', 'sort', 'elements'

    elements = serializers.SerializerMethodField()

    def get_elements(self, obj):
        banners = HighlightsService().get_banners(
            obj.id,
            _type=BannerTypeEnum.MOBILE
        )
        return BannerSerializer(banners, many=True).data
