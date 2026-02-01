from django.http.response import Http404
from rest_framework import generics

from highlights import serializers
from highlights.service import HighlightsService
from shared.bitrix_cli.banners import BannerTypeEnum

class GetHighlightsEndpoint(generics.ListAPIView):
    serializer_class = serializers.MobileMultipleHighlightsSerializer
    service = HighlightsService()

    def get_queryset(self):
        return self.service.get_active_collections()

class GetHighlightEndpoint(generics.RetrieveAPIView):
    serializer_class = serializers.HighlightSerializer
    service = HighlightsService()
    lookup_field = "id"

    def get_object(self):
        obj = self.service.get_active_highlight(
            self.kwargs["id"],
            _type=BannerTypeEnum.MOBILE
        )
        if not obj:
            raise Http404("Highlight not active or not found")
        return obj

class GetCollectionsEndpoint(generics.ListAPIView):
    serializer_class = serializers.CollectionSerializer
    service = HighlightsService()

    def get_queryset(self):
        return self.service.get_active_collections()

class GetCollectionBannersEndpoint(generics.ListAPIView):
    serializer_class = serializers.BannerSerializer
    service = HighlightsService()

    def get_queryset(self):
        return self.service.get_active_banners(self.kwargs["id"], _type=BannerTypeEnum.MOBILE)
