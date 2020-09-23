def has_won(board, column):
    """
    Returns True if game has been won in
    current column, else returns False
    """
    max_row_index = None
    for row_index, row in enumerate(board):
        if row[column] is not None:
            max_row = row_index
            break

    # Check Horizontally for cell (max_row_index, column)
    for current_column in range(0, 4):
        if (
            (board[row_index][current_column] is not None)
            and (
                board[row_index][current_column] == board[row_index][current_column + 1]
            )
            and (
                board[row_index][current_column] == board[row_index][current_column + 2]
            )
            and (
                board[row_index][current_column] == board[row_index][current_column + 3]
            )
        ):
            return board[row_index][current_column], True

    # Check Vertically for cell (max_row_index, column)
    for current_row in range(0, 3):
        if (
            (board[current_row][column] is not None)
            and (board[current_row][column] == board[current_row + 1][column])
            and (board[current_row][column] == board[current_row + 2][column])
            and (board[current_row][column] == board[current_row + 3][column])
        ):
            return board[current_row][column], True

    # Check Left Inclined Diagonal for cell (max_row_index, column)
    for current_row in range(0, 2):
        for current_column in range(3, 7):
            if (
                (board[current_row][current_column] is not None)
                and (
                    board[current_row][current_column]
                    == board[current_row + 1][current_column - 1]
                )
                and (
                    board[current_row][current_column]
                    == board[current_row + 2][current_column - 2]
                )
                and (
                    board[current_row][current_column]
                    == board[current_row + 3][current_column - 3]
                )
            ):
                return board[current_row][current_column], True

    # Check Right Inclined Diagonal for cell (max_row_index, column)
    for current_row in range(0, 4):
        for current_column in range(0, 3):
            if (
                (board[current_row][current_column] is not None)
                and (
                    board[current_row][current_column]
                    == board[current_row + 1][current_column + 1]
                )
                and (
                    board[current_row][current_column]
                    == board[current_row + 2][current_column + 2]
                )
                and (
                    board[current_row][current_column]
                    == board[current_row + 3][current_column + 3]
                )
            ):
                return board[current_row][current_column], True

    return None, False
