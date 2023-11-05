# mypy: disable-error-code="django-manager-missing,misc"
# https://github.com/typeddjango/django-stubs/issues/1023
# https://github.com/typeddjango/django-stubs/issues/471
from django.contrib.auth.models import AbstractUser

from myapp.core.models import CoreModel


class User(AbstractUser, CoreModel):
    """
    Default custom user model.
    """
