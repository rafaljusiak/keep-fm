from django.db import models


class ModelMixin(models.Model):
    """Mixin used for all keep.fm models, that tracks update/create operations dates."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
