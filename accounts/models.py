from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Własny model od początku ułatwi późniejszą rozbudowę kont klientów."""

    class Meta(AbstractUser.Meta):
        verbose_name = "użytkownik"
        verbose_name_plural = "użytkownicy"
