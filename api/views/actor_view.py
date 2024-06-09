from movieapp import models as db
from api.settings import serializers as sr
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status


class ActorListApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = sr.ActorSerializer

    def get_actor(self, id):
        try:
            return db.Actor.objects.get(id=id)
        except db.Actor.DoesNotExist:
            return None

    def get(self, request, id=None, *args, **kwargs):
        if id is not None:
            table_actor = self.get_actor(id=id)
            if table_actor is None:
                return Response(
                    {
                        "status": status.HTTP_404_NOT_FOUND,
                        "message": "No data found",
                        "data": None,
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = self.serializer_class(table_actor)
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": "Successfully fetched data",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            table_actor = db.Actor.objects.all()
            serializer = self.serializer_class(table_actor, many=True)
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
        actor_instance = self.get_actor(id=id)
        if not actor_instance:
            return Response(
                {
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": "Data doesn't exist",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.serializer_class(
            instance=actor_instance, data=request.data, partial=True
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
        actor_instance = self.get_actor(id=id)
        if not actor_instance:
            return Response(
                {
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": "Data doesn't exist",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        actor_instance.delete()
        return Response(
            {
                "status": status.HTTP_204_NO_CONTENT,
                "message": "Data deleted successfully",
            },
            status=status.HTTP_204_NO_CONTENT,
        )
