from django.urls.conf import path

from highlights import endpoints

urlpatterns = [
    path('', endpoints.GetHighlightsEndpoint.as_view(), name='get_highlights'),
    path('<int:id>/', endpoints.GetHighlightEndpoint.as_view(), name='get_highlight_endpoint'),
    path('collections/', endpoints.GetCollectionsEndpoint.as_view(), name='get_collections_endpoint'),
    path('collections/<int:id>/', endpoints.GetCollectionBannersEndpoint.as_view(), name='get_collection_banners_endpoint'),
]
