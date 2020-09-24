from django.conf.urls import url
from django.urls import path

from app.apis import NewGame, Moves, Board

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Connect Four APIs",
        default_version="v1",
        contact=openapi.Contact(email="contact@suhridmathur.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    url(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    url(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
    path("api/v1/new/", NewGame.as_view(), name="new_game"),
    path("api/v1/moves/<str:token>/", Moves.as_view(), name="moves"),
    path("api/v1/board/<str:token>/", Board.as_view(), name="board"),
]
