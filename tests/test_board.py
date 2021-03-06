import pytest

from utahchess import BLACK, WHITE
from utahchess.board import Board
from utahchess.piece import Pawn


@pytest.mark.parametrize(("y", "expected_color"), [(1, BLACK), (6, WHITE)])
@pytest.mark.parametrize(("x"), [0, 1, 2, 3, 4, 5, 6, 7])
def test_get_initial_pawns(x, y, expected_color):
    # when
    board = Board()
    result_piece_type = board[(x, y)].piece_type
    result_color = board[(x, y)].color

    # then
    assert result_color == expected_color
    assert result_piece_type == "Pawn"


@pytest.mark.parametrize(("y", "expected_color"), [(0, BLACK), (7, WHITE)])
@pytest.mark.parametrize(("x"), [0, 7])
def test_get_initial_rooks(x, y, expected_color):
    # when
    board = Board()
    result_piece_type = board[(x, y)].piece_type
    result_color = board[(x, y)].color

    # then
    assert result_color == expected_color
    assert result_piece_type == "Rook"


@pytest.mark.parametrize(("y", "expected_color"), [(0, BLACK), (7, WHITE)])
@pytest.mark.parametrize(("x"), [1, 6])
def test_get_initial_knights(x, y, expected_color):
    # when
    board = Board()
    result_piece_type = board[(x, y)].piece_type
    result_color = board[(x, y)].color

    # then
    assert result_color == expected_color
    assert result_piece_type == "Knight"


@pytest.mark.parametrize(("y", "expected_color"), [(0, BLACK), (7, WHITE)])
@pytest.mark.parametrize(("x"), [2, 5])
def test_get_initial_bishops(x, y, expected_color):
    # when
    board = Board()
    result_piece_type = board[(x, y)].piece_type
    result_color = board[(x, y)].color

    # then
    assert result_color == expected_color
    assert result_piece_type == "Bishop"


@pytest.mark.parametrize(("x", "y", "expected_color"), [(3, 0, BLACK), (3, 7, WHITE)])
def test_get_initial_queens(x, y, expected_color):
    # when
    board = Board()
    result_piece_type = board[(x, y)].piece_type
    result_color = board[(x, y)].color

    # then
    assert result_color == expected_color
    assert result_piece_type == "Queen"


@pytest.mark.parametrize(("x", "y", "expected_color"), [(4, 0, BLACK), (4, 7, WHITE)])
def test_get_initial_kings(x, y, expected_color):
    # when
    board = Board()
    result_piece_type = board[(x, y)].piece_type
    result_color = board[(x, y)].color

    # then
    assert result_color == expected_color
    assert result_piece_type == "King"


@pytest.mark.parametrize(
    ("from_position", "to_position"), [((0, 0), (1, 3)), ((1, 0), (2, 0))]
)
def test_move_piece(from_position, to_position):
    # when
    board = Board()
    piece_to_be_moved = board[from_position]
    new_board = board.move_piece(from_position=from_position, to_position=to_position)

    # then
    assert new_board[to_position].piece_type == piece_to_be_moved.piece_type
    assert new_board[to_position].color == piece_to_be_moved.color
    assert new_board[from_position] is None


@pytest.mark.parametrize(
    ("from_position", "to_position"), [((0, 0), (0, 1)), ((0, 0), (0, 3))]
)
def test_move_piece_with_occupied_to_position(from_position, to_position):
    # when
    board = Board()
    piece_to_be_moved = board[from_position]
    new_board = board.move_piece(from_position=from_position, to_position=to_position)

    # then
    assert new_board[to_position].piece_type == piece_to_be_moved.piece_type
    assert new_board[to_position].color == piece_to_be_moved.color
    assert new_board[from_position] is None


@pytest.mark.parametrize(
    ("from_position", "to_position"), [((2, 1), (2, 1)), ((6, 6), (6, 6))]
)
def test_move_piece_with_equal_from_and_to_position(from_position, to_position):
    # when
    board = Board()
    piece_to_be_moved = board[from_position]
    new_board = board.move_piece(from_position=from_position, to_position=to_position)

    # then
    assert new_board[to_position].piece_type == piece_to_be_moved.piece_type
    assert new_board[to_position].color == piece_to_be_moved.color
    assert new_board[from_position].piece_type == piece_to_be_moved.piece_type
    assert new_board[from_position].color == piece_to_be_moved.color
    assert board == new_board


def test_move_piece_doesnt_affect_copy():
    # given
    board1 = Board()
    board2 = board1.copy()

    # when
    board1 = board1.move_piece(from_position=(0, 0), to_position=(4, 4))

    # then
    assert board2[(4, 4)] is None


@pytest.mark.parametrize("position", [(4, 1), (1, 6), (6, 6), (7, 7), (3, 7)])
def test_delete_piece(position):
    # given
    board = Board()

    # when
    result = board.delete_piece(position=position)

    # then
    assert result[position] is None


def test_board_to_string():
    # given
    board = Board()

    # when
    result = board.to_string()

    # then
    expected = (
        """br-bn-bb-bq-bk-bb-bn-br\n"""
        """bp-bp-bp-bp-bp-bp-bp-bp\n"""
        """oo-oo-oo-oo-oo-oo-oo-oo\n"""
        """oo-oo-oo-oo-oo-oo-oo-oo\n"""
        """oo-oo-oo-oo-oo-oo-oo-oo\n"""
        """oo-oo-oo-oo-oo-oo-oo-oo\n"""
        """wp-wp-wp-wp-wp-wp-wp-wp\n"""
        """wr-wn-wb-wq-wk-wb-wn-wr"""
    )
    assert result == expected


def test_board_raises_valueerror():
    # given
    pieces = (Pawn(position=(0, 0), color=BLACK, is_in_start_position=False),)
    board_string = (
        """br-bn-bb-bq-bk-bb-bn-br\n"""
        """bp-bp-bp-bp-bp-bp-bp-bp\n"""
        """oo-oo-oo-oo-oo-oo-oo-oo\n"""
        """oo-oo-oo-oo-oo-oo-oo-oo\n"""
        """oo-oo-oo-oo-oo-oo-oo-oo\n"""
        """oo-oo-oo-oo-oo-oo-oo-oo\n"""
        """wp-wp-wp-wp-wp-wp-wp-wp\n"""
        """wr-wn-wb-wq-wk-wb-wn-wr"""
    )

    # when and then
    with pytest.raises(ValueError) as e:
        Board(pieces=pieces, board_string=board_string)
        assert (
            e == "Cannot create board when both pieces and board string are provided."
        )
