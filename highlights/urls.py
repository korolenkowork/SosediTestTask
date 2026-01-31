from django.urls.conf import path

from highlights.endpoints import GetHighlightsEndpoint

urlpatterns = [
    path('', GetHighlightsEndpoint.as_view(), name='get_highlights'),
]
