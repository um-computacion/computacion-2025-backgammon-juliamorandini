import unittest
from core.BackgammonGame import (
    Game,
)  # Asumiendo que la clase Game está en un archivo game.py


class TestBackgammonGame(unittest.TestCase):
    def setUp(self):
        """Configuración inicial para cada test"""
        self.game = Game()  # Use Game instead of BackgammonGame

    def test_initial_board_setup(self):
        """Test para verificar la configuración inicial del tablero"""
        board = self.game.get_board()
        # Verificar posiciones iniciales de las fichas
        self.assertEqual(board[0], (-2))  # 2 fichas negras en posición 0
        self.assertEqual(board[23], (2))  # 2 fichas blancas en posición 23
        self.assertEqual(board[11], (5))  # 5 fichas blancas en posición 11
        self.assertEqual(board[12], (-5))  # 5 fichas negras en posición 12

    def test_valid_dice_moves(self):
        """Test para verificar movimientos según los dados"""
        # Proporcionar el argumento dice_values que falta
        dice_values = [3, 4]
        valid_moves = self.game.get_valid_moves(dice_values)
        self.assertIsInstance(valid_moves, list)
        # Verificar que todos los movimientos son válidos (<= 6)
        for move in valid_moves:
            self.assertLessEqual(move, 6)

    def test_invalid_move(self):
        """Test para verificar movimientos inválidos"""
        # Simular un movimiento inválido
        result = self.game.make_move(1, 8)  # movimiento demasiado largo
        self.assertFalse(result)

    def test_hitting_blot(self):
        """Test capturing opponent's single piece"""
        # Set up the board properly
        self.game.board.reset()  # Clear board

        # Place pieces for capture scenario
        if self.game.current_player == "white":
            # White player's turn - place white piece at point 3, black piece at point 5
            self.game.board.points[3] = ["W"]  # White piece to move
            self.game.board.points[5] = ["B"]  # Single black piece (vulnerable)

            # Make capturing move (white moves from 3 to 5)
            result = self.game.make_move(3, 5)
        else:
            # Black player's turn - place black piece at point 3, white piece at point 5
            self.game.board.points[3] = ["B"]  # Black piece to move
            self.game.board.points[5] = ["W"]  # Single white piece (vulnerable)

            # Make capturing move (black moves from 3 to 5)
            result = self.game.make_move(3, 5)

        # Verify the capture worked
        self.assertTrue(result, "Move should be successful")
        self.assertEqual(
            self.game.get_opponent_bar_pieces(),
            1,
            "Opponent should have 1 piece on bar",
        )

        # Additional verification
        self.assertEqual(
            len(self.game.board.points[5]), 1, "Target point should have 1 piece"
        )
        self.assertEqual(
            self.game.board.points[5][0],
            "W" if self.game.current_player == "white" else "B",
            "Target point should have mover's piece",
        )

    def test_bearing_off(self):
        """Test para verificar las reglas de salida de fichas"""
        # Configurar situación de bearing off
        self.game.setup_bearing_off_scenario()
        # Intentar sacar una ficha
        result = self.game.bear_off(23)
        self.assertTrue(result)

    def test_double_dice(self):
        """Test para verificar el manejo de dados dobles"""
        self.game.set_dice([6, 6])
        # Verificar que se permiten 4 movimientos
        moves_allowed = self.game.get_available_moves()
        self.assertEqual(len(moves_allowed), 4)

    def test_blocked_position(self):
        """Test para verificar posiciones bloqueadas"""
        # Crear un bloqueo (más de 2 fichas del oponente)
        self.game.set_piece(10, -3)
        # Intentar mover a una posición bloqueada
        result = self.game.make_move(8, 10)
        self.assertFalse(result)

    def test_winner_detection(self):
        """Test para verificar la detección del ganador"""
        # Configurar un escenario de victoria
        self.game.setup_winning_scenario()
        # Verificar si hay un ganador
        self.assertTrue(self.game.check_winner())

    def test_valid_dice_moves(self):
        """Test para verificar movimientos según los dados"""
        self.game.set_dice([3, 4])
        # Verificar que solo se permiten movimientos de 3 y 4 espacios
        valid_moves = self.game.get_valid_moves()
        self.assertTrue(all(move in [3, 4] for move in valid_moves))

    def test_bar_piece_movement(self):
        """Test para verificar el movimiento obligatorio de fichas en la barra"""
        # Poner una ficha en la barra
        self.game.add_to_bar()
        # Verificar que solo se permiten movimientos desde la barra
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
