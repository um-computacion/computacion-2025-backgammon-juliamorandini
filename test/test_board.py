import unittest
from core.board import Board


class TestBackgammonBoard(unittest.TestCase):
    """Test suite for Backgammon board functionality."""

    def setUp(self):
        """Set up test fixtures."""
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

    def test_move_checker_from_bar_white(self):
        """Test moving white checker from bar."""
        self.board.bar["W"] = 1
        # Try to enter at invalid point
        self.assertFalse(self.board.move_checker_from_bar(0, "W"))
        # Try to enter at valid point
        self.assertTrue(self.board.move_checker_from_bar(18, "W"))
        self.assertEqual(self.board.bar["W"], 0)
        self.assertEqual(self.board.points[18][-1], "W")

    def test_move_checker_from_bar_black(self):
        """Test moving black checker from bar."""
        self.board.bar["B"] = 1
        # Try to enter at invalid point
        self.assertFalse(self.board.move_checker_from_bar(18, "B"))
        # Try to enter at valid point
        self.assertTrue(self.board.move_checker_from_bar(0, "B"))
        self.assertEqual(self.board.bar["B"], 0)
        self.assertEqual(self.board.points[0][-1], "B")

    def test_move_checker_from_empty_bar(self):
        """Test attempting to move from empty bar."""
        self.assertFalse(self.board.move_checker_from_bar(18, "W"))
        self.assertFalse(self.board.move_checker_from_bar(0, "B"))

    def test_move_checker_to_blocked_point(self):
        """Test moving to blocked point."""
        self.board.points[18] = ["B", "B"]
        self.board.bar["W"] = 1
        self.assertFalse(self.board.move_checker_from_bar(18, "W"))

    def test_invalid_point_moves(self):
        """Test moves with invalid point numbers."""
        self.assertFalse(self.board.is_valid_move(-1, 5, "W"))
        self.assertFalse(self.board.is_valid_move(5, 24, "W"))
        self.assertFalse(self.board.is_valid_move(24, 5, "W"))

    def test_hit_opponent_from_bar(self):
        """Test hitting opponent's blot when entering from bar."""
        self.board.points[18] = ["B"]
        self.board.bar["W"] = 1
        self.assertTrue(self.board.move_checker_from_bar(18, "W"))
        self.assertEqual(self.board.bar["B"], 1)
        self.assertEqual(self.board.points[18], ["W"])

    def test_bear_off_with_pieces_outside(self):
        """Test bearing off when pieces are outside home."""
        # Test for White
        self.board.points = [[] for _ in range(24)]
        self.board.points[0] = ["W"]  # Piece outside home
        self.board.points[23] = ["W"]  # Piece in home
        self.assertFalse(self.board.bear_off("W", 23))

        # Test for Black
        self.board.points = [[] for _ in range(24)]
        self.board.points[23] = ["B"]  # Piece outside home
        self.board.points[0] = ["B"]  # Piece in home
        self.assertFalse(self.board.bear_off("B", 0))

    def test_can_bear_off_edge_cases(self):
        """Test edge cases for can_bear_off."""
        # Test with no pieces on board
        self.board.points = [[] for _ in range(24)]
        self.assertTrue(self.board.can_bear_off("W"))
        self.assertTrue(self.board.can_bear_off("B"))

        # Test with pieces on bar
        self.board.bar["W"] = 1
        self.assertFalse(self.board.can_bear_off("W"))
        self.board.bar["B"] = 1
        self.assertFalse(self.board.can_bear_off("B"))

    def test_move_checker_invalid_color(self):
        """Test moving checker with invalid color."""
        self.board.points[0] = ["X"]  # Invalid color
        self.assertFalse(self.board.move_checker(0, 1, "W"))

    def test_enter_from_bar_invalid_points(self):
        """Test entering from bar with invalid points."""
        self.board.bar["W"] = 1
        self.board.bar["B"] = 1

        # Test white entering at invalid points
        for point in range(18):
            self.assertFalse(self.board.move_checker_from_bar(point, "W"))

        # Test black entering at invalid points
        for point in range(6, 24):
            self.assertFalse(self.board.move_checker_from_bar(point, "B"))

    def test_point_manipulation(self):
        """Test direct point manipulation."""
        point = 0
        # Test adding checkers
        self.board.points[point] = ["W"]
        self.assertEqual(self.board.points[point], ["W"])

        # Test removing checkers
        self.board.points[point] = []
        self.assertEqual(self.board.points[point], [])

    def test_bar_manipulation(self):
        """Test bar counter manipulation."""
        self.board.bar["W"] = 2
        self.assertEqual(self.board.bar["W"], 2)
        self.board.bar["W"] = 0
        self.assertEqual(self.board.bar["W"], 0)

    def test_borne_off_manipulation(self):
        """Test borne off counter manipulation."""
        self.board.borne_off["B"] = 3
        self.assertEqual(self.board.borne_off["B"], 3)
        self.board.borne_off["B"] = 0
        self.assertEqual(self.board.borne_off["B"], 0)

    def test_move_checker_to_empty_point(self):
        """Test moving checker to empty point."""
        self.board.points[0] = ["W"]
        self.board.points[1] = []
        self.assertTrue(self.board.move_checker(0, 1, "W"))
        self.assertEqual(self.board.points[0], [])
        self.assertEqual(self.board.points[1], ["W"])

    def test_bar_entrance_with_hit(self):
        """Test entering from bar with hitting opponent's blot."""
        self.board.bar["W"] = 1
        self.board.points[18] = ["B"]
        self.assertTrue(self.board.move_checker_from_bar(18, "W"))
        self.assertEqual(self.board.bar["B"], 1)
        self.assertEqual(self.board.points[18], ["W"])
        self.assertEqual(self.board.bar["W"], 0)

    def test_board_state_validation(self):
        """Test board state validation."""
        # Valid state
        self.assertTrue(self.board.is_valid())

        # Invalid state - mixed colors
        self.board.points[0] = ["W", "B"]
        self.assertFalse(self.board.is_valid())

        # Empty point is valid
        self.board.points[0] = []
        self.assertTrue(self.board.is_valid())

    def test_initial_bar_and_borne_off(self):
        """Test initial bar and borne off states."""
        self.assertEqual(self.board.bar["W"], 0)
        self.assertEqual(self.board.bar["B"], 0)
        self.assertEqual(self.board.borne_off["W"], 0)
        self.assertEqual(self.board.borne_off["B"], 0)

    def test_can_enter_from_bar_empty_point(self):
        """Test entering from bar to empty point."""
        empty_point = 18
        self.board.points[empty_point] = []
        self.assertTrue(self.board.can_enter_from_bar("W", empty_point))

    def test_can_enter_from_bar_single_checker(self):
        """Test entering from bar with single checker present."""
        point = 18
        self.board.points[point] = ["W"]
        self.assertTrue(self.board.can_enter_from_bar("W", point))

        # Should also work with opponent's single checker
        self.board.points[point] = ["B"]
        self.assertTrue(self.board.can_enter_from_bar("W", point))

    def test_can_bear_off_with_all_pieces_home(self):
        """Test bearing off with all pieces in home board."""
        # Clear board
        self.board.points = [[] for _ in range(24)]

        # Put all white pieces in home board
        for i in range(18, 24):
            self.board.points[i] = ["W", "W"]

        self.assertTrue(self.board.can_bear_off("W"))

    def test_move_checker_validation(self):
        """Test move checker validation edge cases."""
        # Test invalid point numbers
        self.assertFalse(self.board.move_checker(-1, 5, "W"))
        self.assertFalse(self.board.move_checker(5, 24, "W"))

        # Test moving when pieces on bar
        self.board.bar["W"] = 1
        self.assertFalse(self.board.move_checker(5, 7, "W"))

    def test_bear_off_from_invalid_point(self):
        """Test bearing off from invalid points."""
        # Try to bear off from empty point
        self.assertFalse(self.board.bear_off("W", 18))

        # Try to bear off opponent's checker
        self.board.points[18] = ["B"]
        self.assertFalse(self.board.bear_off("W", 18))

        # Try to bear off when pieces on bar
        self.board.points[18] = ["W"]
        self.board.bar["W"] = 1
        self.assertFalse(self.board.bear_off("W", 18))


if __name__ == "__main__":
    unittest.main()
