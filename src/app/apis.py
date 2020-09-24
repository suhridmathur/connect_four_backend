import uuid

from app.mongo import MoveService, BoardService
from app.serializers import MoveSerializer, BoardSerializer, NewMoveSerializer, TokenSerializer
from app.service import has_won

from drf_yasg.utils import swagger_auto_schema

from rest_framework.views import APIView
from rest_framework.response import Response


class NewGame(APIView):
    @swagger_auto_schema(responses={200: TokenSerializer})
    def get(self, request, *args, **kwargs):
        """
        Returns a token for a particular game, and
        creates moves and a gameboard for a game
        """
        token = uuid.uuid4()

        moves_data_dict = {
            "token": str(token),
            "player_one": [],
            "player_two": [],
        }
        # Create Move
        move_service = MoveService()
        move_service.insert(moves_data_dict)

        # Create GameBoard
        board_data_dict = {"token": str(token), "board": [[None] * 7] * 6}
        board_service = BoardService()
        board_service.insert(board_data_dict)
        return Response({"token": token})


class Moves(APIView):
    @swagger_auto_schema(responses={200: MoveSerializer})
    def get(self, request, token):
        """
        Get moves for a particular game using token
        """
        move_service = MoveService()
        moves = move_service.get_moves(token)

        serializer = MoveSerializer(data=moves)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)

    def post(self, request, token):
        """
        1. Checks if move is valid
        2. Insert move into move collection if valid move
        3. Updates Game Board
        4. Finds if someone has won the game
        """
        request.data["token"] = token
        serializer = NewMoveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        column, board = serializer.save()
        winner, victory = has_won(board, column)
        if victory:
            board_service = BoardService()
            board_json = board_service.get_board(token)
            board_json["winner"] = winner
            board_service.update(token, board_json)
            return Response(f"Player {winner} won the game!")
        return Response("Valid Move")


class Board(APIView):
    """
    Board API, which returns the current state of
    a board.
    """
    @swagger_auto_schema(responses={200: BoardSerializer})
    def get(self, request, token):
        board_service = BoardService()
        board = board_service.get_board(token)

        serializer = BoardSerializer(data=board)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)
