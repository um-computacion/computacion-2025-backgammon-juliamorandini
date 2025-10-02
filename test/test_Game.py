"""Test module for BackgammonGame class."""

import unittest
from core.BackgammonGame import Game


class TestBackgammonGame(unittest.TestCase):
    """Test cases for BackgammonGame."""

    def setUp(self):
        """Set up test fixtures."""
        self.game = Game()

    def test_initial_board_setup(self):
        """Test initial board configuration."""
        board = self.game.get_board()
        self.assertEqual(board[0], -2)  # 2 black pieces
        self.assertEqual(board[23], 2)  # 2 white pieces
        self.assertEqual(board[11], 5)  # 5 white pieces
        self.assertEqual(board[12], -5)  # 5 black pieces

    def test_valid_moves(self):
        """Test valid moves based on dice values."""
        self.game.set_dice([3, 4])
        moves = self.game.get_available_moves()
        self.assertEqual(len(moves), 2)
        self.assertEqual(moves, [3, 4])

    def test_invalid_move(self):
        """Test invalid move detection."""
        result = self.game.make_move(1, 8)  # Too long move
        self.assertFalse(result)

    def test_hitting_blot(self):
        """Test capturing opponent's single piece."""
        self.game.board.reset()

        # Setup capture scenario
        self.game.board.points[3] = ["W"]
        self.game.board.points[5] = ["B"]

        result = self.game.make_move(3, 5)

        self.assertTrue(result)
        self.assertEqual(self.game.board.bar["B"], 1)
        self.assertEqual(len(self.game.board.points[5]), 1)
        self.assertEqual(self.game.board.points[5][0], "W")

    def test_bearing_off(self):
        """Test bearing off rules."""
        self.game.setup_bearing_off_scenario()
        result = self.game.bear_off(23)
        self.assertTrue(result)

    def test_double_dice(self):
        """Test handling of double dice."""
        self.game.set_dice([6, 6])
        moves = self.game.get_available_moves()
        self.assertEqual(len(moves), 4)
        self.assertEqual(moves, [6, 6, 6, 6])

    def test_blocked_position(self):
        """Test blocked position detection."""
        self.game.set_piece(10, -3)
        result = self.game.make_move(8, 10)
        self.assertFalse(result)

    def test_winner_detection(self):
        """Test winner detection."""
        self.game.setup_winning_scenario()
        self.assertTrue(self.game.check_winner())

    def test_bar_piece_movement(self):
        """Test mandatory bar piece movement."""
        self.game.add_to_bar()
        self.assertTrue(self.game.must_move_from_bar())


if __name__ == "__main__":
    unittest.main()

"""Este conjunto de tests verifica las siguientes reglas del Backgammon:

Configuración inicial correcta del tablero
Validación de movimientos permitidos
Captura de fichas solitarias (blots)
Reglas de salida de fichas (bearing off)
Manejo de dados dobles
Bloqueo de posiciones
Detección de ganador
Movimientos válidos según los dados
Movimiento obligatorio desde la barra
Para implementar estos tests, necesitarías una clase Game con los siguientes métodos:

get_board()
make_move()
set_piece()
get_bar_pieces()
bear_off()
set_dice()
get_available_moves()
check_winner()
get_valid_moves()
add_to_bar()
must_move_from_bar()
setup_bearing_off_scenario()
setup_winning_scenario()"""
