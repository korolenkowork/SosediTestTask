from shared.base_repository import BaseRepository
from highlights import models


class CollectionRepository(BaseRepository):
    model = models.Collection