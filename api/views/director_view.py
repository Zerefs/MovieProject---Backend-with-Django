from movieapp import models as db
from api.settings import serializers as sr
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions, status


class DirectorListApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = sr.DirectorSerializer
    def get_director(self, id):
        try:
            return db.Director.objects.get(id=id)
        except db.Director.DoesNotExist:
            return None

    def get(self, request, id=None, *args, **kwargs):
        if id is not None:
            table_director = self.get_director(id=id)
            if table_director is None:
                return Response(
                    {
                        "status": status.HTTP_404_NOT_FOUND,
                        "message": "Data doesn't exist",
                        "data": None,
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = self.serializer_class(table_director)
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": "Successfully fetched data",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            table_director = db.Director.objects.all()
            serializer = self.serializer_class(table_director, many=True)
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
                    "data": serializer.data,
                    "message": "Data successfully created",
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
        director_instance = self.get_director(id=id)
        if not director_instance:
            return Response(
                {"status": status.HTTP_404_NOT_FOUND, "message": "Data doesn't exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.serializer_class(
            instance=director_instance, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "data": serializer.data,
                    "message": "Data updated successfully",
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
        director_instance = self.get_director(id=id)
        if not director_instance:
            return Response(
                {"status": status.HTTP_404_NOT_FOUND, "message": "Data doesn't exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        director_instance.delete()
        return Response(
            {
                "status": status.HTTP_204_NO_CONTENT,
                "message": "Data deleted successfully",
            },
            status=status.HTTP_204_NO_CONTENT,
        )
