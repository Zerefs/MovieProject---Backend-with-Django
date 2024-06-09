from movieapp import models as db
from api.settings import serializers as sr
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.contrib.auth import login as django_login, logout as django_logout


class RegisterUserApiView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    serializer_class = sr.RegisterUserSerializer

    # def get_user(self, id):
    #     try:
    #         return db.User.objects.get(id=id)
    #     except db.User.DoesNotExist:
    #         return None

    # def get(self, request, id=None, *args, **kwargs):
    #     if id is not None:
    #         table_user = self.get_user(id=id)
    #         if table_user is None:
    #             return Response(
    #                 {
    #                     "status": status.HTTP_404_NOT_FOUND,
    #                     "message": "Data doesn't exist",
    #                     "data": None,
    #                 },
    #                 status=status.HTTP_404_NOT_FOUND,
    #             )
    #         serializer = self.serializer_class(table_user)
    #         return Response(
    #             {
    #                 "status": status.HTTP_200_OK,
    #                 "message": "Successfully fetched data",
    #                 "data": serializer.data,
    #             },
    #             status=status.HTTP_200_OK,
    #         )
    #     else:
    #         table_user = db.User.objects.all()
    #         serializer = self.serializer_class(table_user, many=True)
    #         return Response(
    #             {
    #                 "status": status.HTTP_200_OK,
    #                 "message": "Successfully fetched data",
    #                 "data": serializer.data,
    #             },
    #             status=status.HTTP_200_OK,
    #         )

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": status.HTTP_201_CREATED,
                "message": "You have successfully registered",
                "data": {
                    "username": serializer.data.get("username"),
                    "first_name": serializer.data.get("first_name"),
                    "last_name": serializer.data.get("last_name"),
                    "date_birth": serializer.data.get("date_birth"),
                    "phone_number": serializer.data.get("phone_number"),
                    "email": serializer.data.get("email"),
                },
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Invalid data",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class LoginUserApiView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    serializer_class = sr.LoginUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        django_login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        user_phone_number_serializer = str(user.phone_number)
        return JsonResponse(
            {
                "status": status.HTTP_201_CREATED,
                "message": "You have successfully logged in",
                "user": str(request.user),
                "auth": str(request.auth),
                "data": {
                    "username": user.username,
                    "phone_number": user_phone_number_serializer,
                    "email": user.email,
                    "token": token.key,
                },
            }
        )


class LogoutUserApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request):
        try:
            token = Token.objects.get(user=request.user)
        except Token.DoesNotExist:
            token = None

        django_logout(request)

        if token:
            token.delete()

        return Response(
            {"status": status.HTTP_200_OK, "message": "Successfully logged out"},
            status=status.HTTP_200_OK,
        )


class UserProfileApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = sr.ProfileSerializer

    def get_user_profile(self, id):
        try:
            return db.Profile.objects.get(id=id)
        except db.Profile.DoesNotExist:
            return None

    def get(self, request, id=None, *args, **kwargs):
        if id is not None:
            table_user_profile = self.get_user_profile(id=id)
            if table_user_profile is None:
                return Response(
                    {
                        "status": status.HTTP_404_NOT_FOUND,
                        "message": "Profile not found",
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = self.serializer_class(table_user_profile)
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": "Successfully fetched data",
                    "data": {
                        "id": serializer.data.get("id"),
                        "user": serializer.data.get("user"),
                        "bio": serializer.data.get("bio"),
                        "avatar": serializer.data.get("avatar"),
                        "join_at": serializer.data.get("join_at"),
                    },
                },
                status=status.HTTP_200_OK,
            )
        # else:
        #     table_user_profile = db.Profile.objects.all()
        #     serializer = self.serializer_class(table_user_profile, many=True)
        #     return Response(
        #         {
        #             "status": status.HTTP_200_OK,
        #             "message": "Successfully fetched data",
        #             "data": [
        #                 {
        #                     "id": profile_data.get("id"),
        #                     "user": profile_data.get("user"),
        #                     "bio": profile_data.get("bio"),
        #                     "avatar": profile_data.get("avatar"),
        #                     "join_at": profile_data.get("join_at"),
        #                 }
        #                 for profile_data in serializer.data
        #             ],
        #         },
        #         status=status.HTTP_200_OK,
        #     )

    def put(self, request, id, *args, **kwargs):
        user_profile_instance = self.get_user_profile(id=id)
        if not user_profile_instance:
            return Response(
                {"status": status.HTTP_404_NOT_FOUND, "message": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.serializer_class(
            instance=user_profile_instance, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": "Profile updated successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Invalid data",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
