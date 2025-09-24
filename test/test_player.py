import unittest
from core.player import Player

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player("Player 1", "white")
        self.opponent = Player("Player 2", "black")

    def test_player_initial_setup(self):
        """Test de la configuración inicial del jugador"""
        self.assertEqual(self.player.name, "Player 1")
        self.assertEqual(self.player.color, "white")
        self.assertEqual(self.player.points, 0)
        self.assertEqual(len(self.player.pieces), 15)

    def test_valid_move(self):
        """Test para verificar movimientos válidos"""
        # Simular una posición inicial
        self.player.current_position = 1
        dice_roll = 6
        # Verificar que el movimiento está dentro del tablero
        self.assertTrue(self.player.is_valid_move(dice_roll))

    def test_invalid_move(self):
        """Test para verificar movimientos inválidos"""
        # Simular una posición cerca del borde
        self.player.current_position = 23
        dice_roll = 6
        # Verificar que el movimiento fuera del tablero es inválido
        self.assertFalse(self.player.is_valid_move(dice_roll))

    def test_hit_opponent(self):
        """Test para verificar la captura de fichas del oponente"""
        # Simular una situación donde se puede capturar
        self.player.current_position = 5
        self.opponent.current_position = 5
        self.opponent.pieces_at_point = 1  # Add this line - vulnerable single piece
        self.assertTrue(self.player.can_hit_opponent(self.opponent))

    def test_bearing_off_conditions(self):
        """Test para verificar las condiciones de bearing off"""
        # Simular que todas las piezas están en el cuadrante home
        self.player.pieces_in_home_board = 15
        self.assertTrue(self.player.can_bear_off())
        
        # Simular que no todas las piezas están en el cuadrante home
        self.player.pieces_in_home_board = 10
        self.assertFalse(self.player.can_bear_off())

    def test_blocked_point(self):
        """Test para verificar puntos bloqueados"""
        # Simular un punto con 2 o más fichas del oponente
        self.opponent.current_position = 5  # Add this line
        self.opponent.pieces_at_point = 2
        self.assertTrue(self.player.is_point_blocked(5, self.opponent))

    def test_dice_roll_validation(self):
        """Test para validar tiradas de dados"""
        # Verificar que los dados estén entre 1 y 6
        dice1, dice2 = 3, 5
        self.assertTrue(1 <= dice1 <= 6 and 1 <= dice2 <= 6)

    def test_winner_conditions(self):
        """Test para verificar condiciones de victoria"""
        # Simular que todas las fichas han sido removidas
        self.player.pieces_removed = 15
        self.assertTrue(self.player.has_won())

    def test_bar_reentry(self):
        """Test para verificar la reentrada desde la barra"""
        # Simular una ficha en la barra
        self.player.pieces_on_bar = 1
        entry_point = 1
        # Verificar que la reentrada es válida
        self.assertTrue(self.player.can_reenter_from_bar(entry_point))

    def test_double_points(self):
        """Test para verificar puntos dobles"""
        # Simular un punto con múltiples fichas del mismo color
        self.player.pieces_at_point = 2
        self.assertTrue(self.player.is_point_secure())

if __name__ == '__main__':
    unittest.main()



"""esoecificaciones:
ste conjunto de pruebas verifica:

Configuración inicial del jugador
Validación de movimientos
Captura de fichas del oponente
Condiciones para bearing off
Puntos bloqueados
Validación de dados
Condiciones de victoria
Reentrada desde la barra
Puntos seguros (dobles)
Para que estos tests funcionen, necesitarías implementar los métodos correspondientes en la clase Players. Aquí hay una estructura básica de la clase que estos tests esperarían:

me dio la clase tambien hecha, la dejo aca como referencia para el futuro
class Players:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.points = 0
        self.pieces = [None] * 15
        self.current_position = 0
        self.pieces_in_home_board = 0
        self.pieces_on_bar = 0
        self.pieces_removed = 0
        self.pieces_at_point = 0

    def is_valid_move(self, dice_roll):
        # Implementar lógica para validar movimientos
        pass

    def can_hit_opponent(self, opponent):
        # Implementar lógica para verificar si se puede capturar
        pass

    def can_bear_off(self):
        # Implementar lógica para bearing off
        pass

    def is_point_blocked(self, point, opponent):
        # Implementar lógica para verificar puntos bloqueados
        pass

    def has_won(self):
        # Implementar lógica para verificar victoria
        pass

    def can_reenter_from_bar(self, entry_point):
        # Implementar lógica para reentrada desde la barra
        pass

    def is_point_secure(self):
        # Implementar lógica para verificar puntos seguros
        pass
"""