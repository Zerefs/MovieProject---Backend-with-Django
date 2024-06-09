from django.urls import path
from api.views.user_view import *
from api.views.actor_view import *
from api.views.director_view import *
from api.views.language_view import *
from api.views.genre_view import *
from api.views.country_view import *
from api.views.production_studio_view import *
from api.views.movie_view import *

app_name = "api"

urlpatterns = [
    # user
    path("MovieGuideX/User/Register", RegisterUserApiView.as_view()),
    path("MovieGuideX/User/Register/<int:id>", RegisterUserApiView.as_view()),
    path("MovieGuideX/User/Login", LoginUserApiView.as_view()),
    path("MovieGuideX/User/Logout", LogoutUserApiView.as_view()),
    path("MovieGuideX/Users/Profile", UserProfileApiView.as_view()),
    path("MovieGuideX/User/Profile/<int:id>", UserProfileApiView.as_view()),
    # movie
    path("MovieGuideX/Movies", MovieListApiView.as_view()),
    path("MovieGuideX/Movie/<int:id>", MovieListApiView.as_view()),
    path("MovieGuideX/Movies/", MoviePaginator.as_view()),
    # actor
    path("MovieGuideX/Actors", ActorListApiView.as_view()),
    path("MovieGuideX/Actor/<int:id>", ActorListApiView.as_view()),
    # director
    path("MovieGuideX/Directors", DirectorListApiView.as_view()),
    path("MovieGuideX/Director/<int:id>", DirectorListApiView.as_view()),
    # language
    path("MovieGuideX/Languages", LanguageListApiView.as_view()),
    path("MovieGuideX/Language/<int:id>", LanguageListApiView.as_view()),
    # genre
    path("MovieGuideX/Genres", GenreListApiView.as_view()),
    path("MovieGuideX/Genre/<int:id>", GenreListApiView.as_view()),
    # country
    path("MovieGuideX/Countrys", CountryListApiView.as_view()),
    path("MovieGuideX/Country/<int:id>", CountryListApiView.as_view()),
    # production
    path("MovieGuideX/Productions", ProductionStudioListApiView.as_view()),
    path("MovieGuideX/Production/<int:id>", ProductionStudioListApiView.as_view()),
]
