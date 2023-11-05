from dataclasses import asdict, dataclass

from faker import Faker

fake = Faker()


@dataclass
class UserFactory:
    username: str | None = None
    password: str | None = None

    def __post_init__(self):
        if self.username is None:
            self.username = fake.user_name()
        if self.password is None:
            self.password = fake.password(
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            )

    def create(self):
        return asdict(self)
