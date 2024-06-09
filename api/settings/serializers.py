from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from movieapp import models as db


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.Genre
        fields = "__all__"


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.Director
        fields = "__all__"


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.Actor
        fields = "__all__"


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = db.Country
        fields = "__all__"


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.Language
        fields = "__all__"


class ProductionStudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.ProductionStudio
        fields = "__all__"


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.Movie
        fields = "__all__"


class RegisterUserSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True, validators=[UniqueValidator(queryset=db.User.objects.all())]
    )
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    date_of_birth = serializers.DateField(required=True)
    phone_number = PhoneNumberField(
        required=True, validators=[UniqueValidator(queryset=db.User.objects.all())]
    )
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=db.User.objects.all())]
    )
    password = serializers.CharField(
        required=True, validators=[validate_password], style={"input_type": "password"}
    )
    confirm_password = serializers.CharField(
        required=True, write_only=True, validators=[validate_password]
    )

    class Meta:
        model = db.User
        fields = [
            "username",
            "date_of_birth",
            "phone_number",
            "email",
            "first_name",
            "last_name",
            "is_normal_user",
            "is_superuser",
            "is_staff",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Password do not match.")
        return attrs

    def create(self, validated_data):
        if not validated_data.get("email"):
            raise serializers.ValidationError("Email is required.")

        if not validated_data.get("phone_number"):
            raise serializers.ValidationError("Phone number is required.")

        user = db.User.objects.create(
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            phone_number=validated_data["phone_number"],
            date_of_birth=validated_data["date_of_birth"],
            is_superuser=False,
            is_staff=False,
            is_normal_user=True,
        )

        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, allow_blank=True)
    password = serializers.CharField(required=True, allow_blank=True)

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                if user.is_normal_user:
                    user.last_login = timezone.now()
                    user.save(update_fields=["last_login"])
                    data["user"] = user
                else:
                    raise ValidationError(
                        "Your account does not have permission to log in."
                    )
            else:
                raise ValidationError("Invalid username or password.")
        else:
            raise ValidationError("Please provide both username and password")

        return data


class LogoutUserSerializer(serializers.Serializer):
    def validate(self, data):

        return data


class UserSerializer(serializers.ModelSerializer):
    # favorite_movies = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = db.User
        fields = [
            "id",
            "username",
            "email",
            "phone_number",
            "date_of_birth",
            "is_normal_user",
            "is_staff",
            "is_superuser",
            "first_name",
            "last_name",
        ]


class ProfileSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField()

    class Meta:
        model = db.Profile
        fields = "__all__"
