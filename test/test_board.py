import unittest
from core.board import Board


class TestBackgammonBoard(unittest.TestCase):

    def setUp(self):
        # Suponemos que tienes una clase Board con un método reset() para inicializar el tablero
        self.board = Board()
        self.board.reset()

    def test_board_has_24_points(self):
        self.assertEqual(len(self.board.points), 24, "El tablero debe tener 24 puntos.")

    def test_initial_setup(self):
        """Test initial board setup"""
        # Expected setup based on YOUR Board.reset() method
        expected_setup = {
            0: ["B", "B"],  # 2 black pieces at point 1
            5: ["W"] * 5,  # 5 white pieces at point 6
            7: ["W"] * 3,  # 3 white pieces at point 8
            11: ["W"] * 5,  # 5 white pieces at point 12
            12: ["B"] * 5,  # 5 black pieces at point 13
            16: ["B"] * 3,  # 3 black pieces at point 17
            18: ["B"] * 5,  # 5 black pieces at point 19
            23: ["W", "W"],  # 2 white pieces at point 24
        }

        for point, expected_checkers in expected_setup.items():
            with self.subTest(point=point):
                self.assertEqual(
                    self.board.points[point],
                    expected_checkers,
                    f"Point {point+1} should have {expected_checkers}",
                )

    def test_no_mixed_checkers_on_point(self):
        # Intentar poner fichas de ambos colores en un punto debe fallar
        self.board.points[0] = ["W", "B"]
        self.assertFalse(
            self.board.is_valid(),
            "No puede haber fichas de ambos colores en el mismo punto.",
        )

    def test_move_checker(self):
        """Test moving a checker"""
        # Setup: Place a black piece at point 0 (since that's our initial setup)
        self.board.points[0] = ["B"]  # Single black piece for testing

        # Move black piece from point 0 to point 1
        result = self.board.move_checker(0, 1, "B")

        # Verify the move was successful
        self.assertTrue(result)
        self.assertEqual(len(self.board.points[0]), 0)  # Point 0 should be empty
        self.assertEqual(
            self.board.points[1], ["B"]
        )  # Point 1 should have the black piece

    def test_capture_checker(self):
        # Simula una captura: un punto con una sola ficha del oponente
        self.board.points[5] = ["B"]
        self.board.points[4] = ["W"]
        self.board.move_checker(4, 5, "W")
        self.assertEqual(
            self.board.bar["B"],
            1,
            "La ficha negra debe estar en la barra tras ser capturada.",
        )
        self.assertEqual(self.board.points[5], ["W"])

    def test_illegal_move(self):
        # No se puede mover a un punto con 2 o más fichas del oponente
        self.board.points[5] = ["B", "B"]
        self.assertFalse(
            self.board.is_valid_move(
                4, 5, "W"
            ),  # CORREGIDO: is_legal_move -> is_valid_move
            "No se puede mover a un punto bloqueado.",
        )

    def test_cannot_move_from_empty_point(self):
        # No se puede mover ficha desde un punto vacío
        self.board.points[10] = []
        self.assertFalse(
            self.board.is_valid_move(
                10, 12, "W"
            ),  # CORREGIDO: is_legal_move -> is_valid_move
            "No se puede mover desde un punto vacío.",
        )

    def test_cannot_move_opponent_checker(self):
        # No se puede mover ficha del oponente
        self.board.points[8] = ["B"]
        self.assertFalse(
            self.board.is_valid_move(
                8, 10, "W"
            ),  # CORREGIDO: is_legal_move -> is_valid_move
            "No se puede mover ficha del oponente.",
        )

    def test_bar_priority(self):
        # Si hay fichas en la barra, deben entrar antes de mover otras fichas
        self.board.bar["W"] = 1
        self.assertFalse(
            self.board.is_valid_move(
                0, 2, "W"
            ),  # CORREGIDO: is_legal_move -> is_valid_move
            "Debe ingresar ficha desde la barra antes de mover otras.",
        )

    def test_bear_off_only_when_all_in_home(self):
        """Test bear off functionality - VERSIÓN CORREGIDA"""
        # Solo se puede sacar fichas si todas están en el home
        self.board.points = [[] for _ in range(24)]
        self.board.points[18] = ["W"] * 15  # Todas en home
        result = self.board.bear_off("W", 18)
        self.assertTrue(result, "Debe poder sacar fichas del home")

        # Verificar que la ficha fue removida
        self.assertEqual(len(self.board.points[18]), 14)
        self.assertEqual(self.board.borne_off["W"], 1)

    def test_bear_off(self):
        """Test basic bear off functionality."""
        # Simula sacar una ficha
        self.board.points = [[] for _ in range(24)]
        self.board.points[18] = ["W"]

        # Bear off debería funcionar
        result = self.board.bear_off("W", 18)
        self.assertTrue(result, "Bear off debería retornar True")
        self.assertEqual(
            self.board.points[18], [], "La ficha debe ser removida del punto."
        )
        self.assertEqual(
            self.board.borne_off["W"], 1, "La ficha debe estar en la zona de borne."
        )

    def test_bear_off_invalid(self):
        """Test invalid bear off attempts."""
        # Intentar sacar de punto vacío
        self.board.points = [[] for _ in range(24)]
        result = self.board.bear_off("W", 18)
        self.assertFalse(result, "No debería poder sacar de punto vacío")

        # Intentar sacar ficha oponente
        self.board.points[10] = ["B"]
        result = self.board.bear_off("W", 10)
        self.assertFalse(result, "No debería poder sacar ficha oponente")

    def test_blocked_entry_from_bar(self):
        # No puede entrar desde la barra si el punto está bloqueado
        self.board.bar["W"] = 1
        self.board.points[0] = ["B", "B"]
        self.assertFalse(
            self.board.can_enter_from_bar("W", 0),
            "No puede entrar si el punto está bloqueado.",
        )


if __name__ == "__main__":
    unittest.main()
