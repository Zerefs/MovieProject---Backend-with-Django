from movieapp import models as db
from api.settings import serializers as sr
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status


class LanguageListApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = sr.LanguageSerializer

    def get_language(self, id):
        try:
            return db.Language.objects.get(id=id)
        except db.Language.DoesNotExist:
            return None

    def get(self, request, id=None, *args, **kwargs):
        if id is not None:
            table_language = self.get_language(id=id)
            if table_language is None:
                return Response(
                    {
                        "status": status.HTTP_404_NOT_FOUND,
                        "message": "No data found",
                        "data": None,
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = self.serializer_class(table_language)
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": "Successfully fetched data",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            table_language = db.Language.objects.all()
            serializer = self.serializer_class(table_language, many=True)
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": "Successfully fetched data",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": status.HTTP_201_CREATED,
                    "message": "Data created successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Invalid data",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def put(self, request, id, *args, **kwargs):
        language_instance = self.get_language(id=id)
        if not language_instance:
            return Response(
                {
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": "Data doesn't exist",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.serializer_class(
            instance=language_instance, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": "Data updated successfully",
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

    def delete(self, request, id, *args, **kwargs):
        language_instance = self.get_language(id=id)
        if not language_instance:
            return Response(
                {
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": "Data doesn't exist",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        language_instance.delete()
        return Response(
            {
                "status": status.HTTP_204_NO_CONTENT,
                "message": "Data deleted successfully",
            },
            status=status.HTTP_204_NO_CONTENT,
        )
