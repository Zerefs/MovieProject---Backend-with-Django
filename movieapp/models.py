from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
from django.db.models import JSONField


class User(AbstractUser):
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    date_of_birth = models.DateField(blank=False, null=False)
    phone_number = PhoneNumberField(blank=False, null=False, unique=True)
    email = models.EmailField(max_length=150, blank=False, null=False, unique=True)
    is_normal_user = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "date_of_birth",
        "phone_number",
        "email",
    ]

    def __str__(self):
        return (
            self.username
            + " ~ "
            + ("Super user" if self.is_superuser else "Ordinary user")
        )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(blank=True, null=True, upload_to="avatars/")
    join_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Genre(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=10512, blank=False, null=False, unique=True)
    image = models.ImageField(blank=True, null=True, upload_to="actors/")

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)
    image = models.ImageField(blank=True, null=True, upload_to="directors/")

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class ProductionStudio(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    STATUS_MOVIE = (("Released", "Released"), ("Unreleased", "Unreleased"))

    title = models.CharField(max_length=255, blank=False, null=False, unique=True)
    release_date = models.DateField(blank=True, null=True)
    synopsis = models.TextField(blank=True)
    genres = models.ManyToManyField(Genre, blank=True)
    duration = models.CharField(
        max_length=10, blank=True, null=False
    )  # disesuaikan max_length-nya
    language = models.ForeignKey(
        Language, on_delete=models.SET_NULL, blank=True, null=True
    )
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, blank=True, null=True
    )
    rating = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    director = models.ForeignKey(
        Director, on_delete=models.SET_NULL, blank=True, null=True
    )
    actors = models.ManyToManyField(Actor, blank=True)
    poster = models.ImageField(blank=True, null=True, upload_to="posters/")
    backdrop = models.ImageField(
        blank=True, null=True, upload_to="backdrops/"
    )
    trailer = models.CharField(max_length=255, blank=True, null=False)
    source = models.CharField(max_length=255, blank=True, null=False)
    production_studio = models.ManyToManyField(ProductionStudio, blank=True)
    status = models.CharField(
        choices=STATUS_MOVIE, max_length=12, blank=False, null=False
    )
    adults = models.BooleanField(blank=True, null=True)
    favorit_users = JSONField(default=list,)

    def __str__(self):
        return self.title

    def add_favorit(self, user_id):
        if user_id not in self.favorit_users:
            self.favorit_users.append(user_id)
            self.save()

    def remove_favorit(self, user_id):
        if user_id in self.favorit_users:
            self.favorit_users.remove(user_id)
            self.save()

    def is_favorit(self, user_id):
        return user_id in self.favorit_users


class Review(models.Model):
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="user_reviews"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} review on {self.movie.title}"
