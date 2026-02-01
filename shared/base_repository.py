from typing import Optional


class BaseRepository:
    model = None
    base_filters = {"is_deleted": False}

    def get_all(self):
        return self.model.objects.filter(**self.base_filters)

    def filter(self, **filters):
        return self.model.objects.filter(**self.base_filters, **filters)

    def create(self, **kwargs):
        return self.model.objects.create(**kwargs)

    def update(self, instance, **kwargs):
        return self.model.objects.filter(pk=instance.pk, **self.base_filters).update(**kwargs)

    def delete(self, instance):
        return self.model.objects.filter(pk=instance.pk, **self.base_filters).update(is_deleted=True)