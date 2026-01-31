import logging

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from highlights import serializers
from highlights.service import HighlightsService
from shared.bitrix_cli.banners import BannerTypeEnum

class GetHighlightsEndpoint(generics.ListAPIView):
    serializer_class = serializers.HighlightsSerializer
    service = HighlightsService()

    def get_queryset(self):
        return self.service.get_highlights(_type=BannerTypeEnum.MOBILE)