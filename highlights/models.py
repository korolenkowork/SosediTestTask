from django.db import models

from shared.base_model import BaseModel


class Collection(BaseModel):
    name = models.CharField(max_length=255)
    picture = models.CharField(max_length=255)
    active_from = models.DateTimeField(max_length=255, null=True, blank=True)
    active_to = models.DateTimeField(max_length=255, null=True, blank=True)
    sort = models.CharField(max_length=255, default="asc")
    # elements =
    bitrix_elements_id = models.IntegerField()

    class Meta:
        ordering = ["sort", "id"]

# class Banner(models.Model):
#     name = models.CharField(max_length=255)
#     preview_picture = models.CharField(max_length=255)
#     banner_area = models.CharField(max_length=255)
#     url = models.CharField(max_length=255)
#     button_text = models.CharField(max_length=255, null=True, blank=True)
#     button_link = models.CharField(max_length=255, null=True, blank=True)
#     active_from = models.DateTimeField(max_length=255)
#     active_to = models.DateTimeField(max_length=255)
#     sort = models.IntegerField()