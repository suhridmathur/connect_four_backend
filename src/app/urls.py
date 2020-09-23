from django.urls import path
from app.apis import NewGame, Moves, Board

urlpatterns = [
    path("api/v1/new/", NewGame.as_view(), name="new_game"),
    path("api/v1/moves/<str:token>/", Moves.as_view(), name="moves"),
    path("api/v1/board/<str:token>/", Board.as_view(), name="board"),
]
