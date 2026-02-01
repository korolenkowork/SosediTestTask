from django.db import models

from shared.base_model import BaseModel


class Collection(BaseModel):
    name = models.CharField(max_length=255)
    picture = models.CharField(max_length=255)
    active_from = models.DateTimeField(max_length=255, null=True, blank=True)
    active_to = models.DateTimeField(max_length=255, null=True, blank=True)
    sort = models.CharField(max_length=255, default="500")
    bitrix_elements_id = models.IntegerField()

    class Meta:
        ordering = ["sort", "id"]
