class Checker:

    def __init__(self, color: str, position: int) -> None:
        if color not in ['white', 'black']:
            raise ValueError("Color must be 'white' or 'black'")

        self.color = color
        self.position = position
        self.is_on_bar = (position == 'bar')
        self.is_borne_off = False

    def move_to(self, new_position: int) -> bool:
        if 0 <= new_position <= 23:
            self.position = new_position
            self.is_on_bar = False
            return True
        return False

    def send_to_bar(self) -> None:
        self.position = 'bar'
        self.is_on_bar = True

    def bear_off(self) -> None:
        self.position = 'off'
        self.is_borne_off = True

    def can_bear_off(self, all_home: bool) -> bool:
        if not all_home:
            return False
        if not isinstance(self.position, int):
            return False
        if self.color == 'white':
            return self.position >= 18
        return self.position <= 5

    def is_point_blocked(self, point, board):
        """Check if a point is blocked by opponent"""
        if point not in board or not board[point]:
            return False
            
        # Verificar si hay 2 o más fichas del oponente
        opponent_color = 'black' if self.color == 'white' else 'white'
        opponent_count = sum(1 for checker in board[point] if checker.color == opponent_color)
        
        return opponent_count >= 2

    def can_move_to(self, point, board):
        """Check if can move to point."""
        if not (0 <= point < 24):
            return False
        # Si la ficha está en la barra
        if self.is_on_bar or self.position == 'bar':
            # Solo puede entrar si el punto NO está bloqueado
            return not self.is_point_blocked(point, board)
        return not self.is_point_blocked(point, board) # Para fichas normales en el tablero

    def move(self, point, board):
        if self.can_move_to(point, board):
            old_position = self.position
            self.position = point
            self.is_on_bar = False  # Ya no está en la barra
            if old_position != 'bar' and old_position in board: # Mover la ficha en el tablero
                board[old_position] = [c for c in board[old_position] if c != self]
            
            if point in board:
                board[point].append(self)
            else:
                board[point] = [self]
                
            return True
        return False