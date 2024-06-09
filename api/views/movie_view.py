from movieapp import models as db
from api.settings import serializers as sr
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from api.settings.paginators import CustomPagination
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter


class MoviePaginator(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    queryset = db.Movie.objects.all()
    serializer_class = sr.MovieSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["genres", "release_date"]
    ordering_fields = ["title"]
    search_fields = ["title"]


class MovieListApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = sr.MovieSerializer
    def get_movie(self, id):
        try:
            return db.Movie.objects.get(id=id)
        except db.Movie.DoesNotExist:
            return None

    def get(self, request, id=None, *args, **kwargs):
        if id is not None:
            table_movie = self.get_movie(id=id)
            if table_movie is None:
                return Response(
                    {
                        "status": status.HTTP_404_NOT_FOUND,
                        "message": "Data doesn't exist",
                        "data": None,
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = self.serializer_class(table_movie)
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": "Successfully fetched data",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            movies = db.Movie.objects.all()
            serializer = self.serializer_class(movies, many=True)
            
            return Response({
                    "status": status.HTTP_200_OK,
                    "message": "Successfully fetched data",
                    "data": serializer.data,
                }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        movie_genre = request.data.get("genres")
        movie_production = request.data.get("production_studio")
        movie_actor = request.data.get("actors")

        if isinstance(movie_genre, str):
            list_movie_genre = [
                int(pk)
                for pk in movie_genre.replace("[", "").replace("]", "").split(",")
            ]

        if isinstance(movie_production, str):
            list_movie_production = [
                int(pk)
                for pk in movie_production.replace("[", "").replace("]", "").split(",")
            ]

        if isinstance(movie_actor, str):
            list_movie_actor = [
                int(pk)
                for pk in movie_actor.replace("[", "").replace("]", "").split(",")
            ]

        data = {
            "title": request.data.get("title"),
            "synopsis": request.data.get("synopsis"),
            "release_date": request.data.get("release_date"),
            "genres": list_movie_genre,
            "language": request.data.get("language"),
            "rating": request.data.get("rating"),
            "country": request.data.get("country"),
            "duration": request.data.get("duration"),
            "status": request.data.get("status"),
            "director": request.data.get("director"),
            "actor": list_movie_actor,
            "poster": request.data.get("poster"),
            "backdrop": request.data.get("backdrop"),
            "trailer": request.data.get("trailer"),
            "source": request.data.get("source"),
            "production_studio": list_movie_production,
            "adults": request.data.get("adults"),
        }

        serializer = self.serializer_class(data=data)
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
        movie_instance = self.get_movie(id=id)
        if not movie_instance:
            return Response(
                {
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": "Data doesn't exist",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        movie_genre = request.data.get("genres")
        movie_production = request.data.get("production_studio")
        movie_actor = request.data.get("actors")

        if isinstance(movie_genre, str):
            list_movie_genre = [
                int(pk)
                for pk in movie_genre.replace("[", "").replace("]", "").split(",")
            ]

        if isinstance(movie_production, str):
            list_movie_production = [
                int(pk)
                for pk in movie_production.replace("[", "").replace("]", "").split(",")
            ]

        if isinstance(movie_actor, str):
            list_movie_actor = [
                int(pk)
                for pk in movie_actor.replace("[", "").replace("]", "").split(",")
            ]
        data = {
            "title": request.data.get("title"),
            "synopsis": request.data.get("synopsis"),
            "release_date": request.data.get("release_date"),
            "genres": list_movie_genre,
            "language": request.data.get("language"),
            "rating": request.data.get("rating"),
            "pendapatan_film": request.data.get("pendapatan_film"),
            "country": request.data.get("country"),
            "duration": request.data.get("duration"),
            "status": request.data.get("status"),
            "director": request.data.get("director"),
            "actors": list_movie_actor,
            "poster": request.data.get("poster"),
            "backdrop": request.data.get("backdrop"),
            "trailer": request.data.get("trailer"),
            "source": request.data.get("source"),
            "production_studio": list_movie_production,
            "adults": request.data.get("adults"),
        }

        serializer = self.serializer_class(
            instance=movie_instance, data=data, partial=True
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
        movie_instance = self.get_movie(id=id)
        if not movie_instance:
            return Response(
                {
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": "Data doesn't exist",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        movie_instance.delete()
        return Response(
            {
                "status": status.HTTP_204_NO_CONTENT,
                "message": "Data deleted successfully",
            },
            status=status.HTTP_204_NO_CONTENT,
        )
