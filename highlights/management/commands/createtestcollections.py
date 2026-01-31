import datetime

from django.core.management import BaseCommand

from highlights.models import Collection


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument("collections_count", type=int)

    def handle(self, *args, **options):
        for i in range(options['collections_count']):
            Collection.objects.create(
                name=f"Collection {i}",
                picture=f"https://picsum.photos/200/300?random={i}",
                active_from=datetime.datetime.now(),
                active_to=datetime.datetime.now() + datetime.timedelta(days=30),
                sort="asc",
                bitrix_elements_id=130
            )

        self.stdout.write(self.style.SUCCESS("Collections successfully created!"))