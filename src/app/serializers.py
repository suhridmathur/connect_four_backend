from django.core.validators import MinValueValidator, MaxValueValidator

from .mongo import BoardService, MoveService

from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class MoveSerializer(serializers.Serializer):
    token = serializers.CharField()
    player_one = serializers.ListField()
    player_two = serializers.ListField()


class BoardSerializer(serializers.Serializer):
    token = serializers.CharField()
    board = serializers.ListField()
    winner = serializers.CharField(required=False)


class NewMoveSerializer(serializers.Serializer):
    column = serializers.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(6)]
    )
    token = serializers.CharField()

    def validate(self, data):
        token = data.get("token")
        column = data.get("column")

        board_service = BoardService()
        board_json = board_service.get_board(token)
        board = board_json.get("board")

        if board[5][column] is not None:
            raise ValidationError(f"Invalid Move! Column {column} is already full")

        if board_json.get("winner", None):
            raise ValidationError("Game is already finished.")
        return data

    def create(self, data):
        """
        Updates board and add move into moves collection
        """
        token = data.get("token")
        column = data.get("column")

        move_service = MoveService()
        moves_json = move_service.get_moves(token)

        player_one_moves = moves_json.get("player_one")
        player_two_moves = moves_json.get("player_two")

        if len(player_one_moves) == len(player_two_moves):
            player_one_moves.append(column)
            current_player = 1
        else:
            player_two_moves.append(column)
            current_player = 2

        board_service = BoardService()
        board_json = board_service.get_board(token)
        board = board_json.get("board")

        for row in board:
            if row[column] is None:
                row[column] = current_player
                break
        board_service.update(token, board_json)
        move_service.update(token, moves_json)
        return column, board


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()