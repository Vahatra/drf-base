from django.contrib.auth import get_user_model
from factory import Faker
from factory.django import DjangoModelFactory, Password


class UserFactory(DjangoModelFactory):
    username = Faker("user_name")
    author_pseudonym = Faker("name")
    password = Password(
        Faker(
            "password",
            length=42,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True,
        )
    )

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]
