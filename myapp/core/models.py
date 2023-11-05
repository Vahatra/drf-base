from model_utils.fields import UUIDField
from model_utils.models import TimeStampedModel


class CoreModel(TimeStampedModel):
    """
    Base model.
    """

    id = UUIDField(primary_key=True, version=4, editable=False)

    class Meta:
        abstract = True
        default_permissions = ()
