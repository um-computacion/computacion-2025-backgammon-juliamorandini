# Backgammon Game Project

Alumno: Julia Morandini Monteverdi

## Descripción

Este proyecto implementa un juego de Backgammon completo con dos interfaces: una interfaz de línea de comandos (CLI) y una interfaz gráfica usando Pygame.

## Prerrequisitos

- Python 3.11 o superior
- pip (gestor de paquetes de Python)
- Entorno virtual de Python (recomendado)

### Paquetes Requeridos

```bash
pygame==2.6.0
pytest==7.4.3
pytest-cov==4.1.0
coverage==7.3.2
```
## Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Modo Juego

### Interfaz Gráfica (Pygame)

Para iniciar el juego con la interfaz gráfica:
```bash
python PygameUI.py
```

#### Controles del Juego
- **Click Izquierdo**: Seleccionar/mover fichas
- **Tecla N**: Siguiente turno
- **Tecla R**: Reiniciar juego
- **Tecla ESPACIO**: Lanzar dados

#### Interfaz Visual
- Tablero principal con 24 puntos numerados
- Bar central para fichas capturadas
- Indicadores de turno y dados
- Botones interactivos para acciones del juego

### Interfaz de Línea de Comandos (CLI)

Para iniciar el juego en modo texto:
```bash
python -m cli.CLI
```

#### Comandos CLI
- `roll`: Lanzar dados
- `move [from] [to]`: Mover ficha
- `quit`: Salir del juego
- `help`: Ver comandos disponibles

## Modo Testing

### Ejecutar Tests
```bash
# Ejecutar todos los tests
python -m pytest

# Ejecutar tests con cobertura
python -m pytest --cov=.

# Generar reporte de cobertura HTML
python -m pytest --cov=. --cov-report=html
```

### Generar Reportes
```bash
# Generar todos los reportes
python generate_reports.py
```

## Estructura del Proyecto

### Core (Lógica del Juego)
- **BackgammonGame.py**: Motor principal del juego
- **board.py**: Lógica del tablero
- **Checker.py**: Manejo de fichas
- **Dice.py**: Lógica de dados
- **player.py**: Gestión de jugadores

### Interfaces
- **CLI.py**: Interfaz de línea de comandos
- **PygameUI.py**: Interfaz gráfica

### Pygame UI Components
- **backgammon_board.py**: Renderizado del tablero
- **board_interaction.py**: Manejo de interacciones
- **board_renderer.py**: Renderizado de componentes
- **checker_renderer.py**: Renderizado de fichas
- **dice_renderer.py**: Renderizado de dados
- **button.py**: Componentes de botones

## UML Class Reference

### Core Classes

#### BackgammonGame
- **Attributes**:
  - board: Board
  - current_player: str
  - dice_values: List[int]
  - moves_made: int
- **Methods**:
  - roll_dice()
  - move_checker(from_point, to_point)
  - next_turn()
  - is_game_over()

#### Board
- **Attributes**:
  - points: Dict[int, List[Checker]]
  - bar: Dict[str, int]
  - borne_off: Dict[str, int]
- **Methods**:
  - move_checker(from_point, to_point)
  - can_bear_off(color)
  - is_valid_move(from_point, to_point)

#### Checker
- **Attributes**:
  - color: str
  - position: Union[int, str]
  - is_on_bar: bool
  - is_borne_off: bool
- **Methods**:
  - move_to(point)
  - can_move_to(point, board)
  - send_to_bar()
  - bear_off()

### UI Classes

#### PygameUI
- **Attributes**:
  - game: BackgammonGame
  - board: BackgammonBoard
  - screen: pygame.Surface
- **Methods**:
  - handle_events()
  - update()
  - draw()

#### BackgammonBoard
- **Attributes**:
  - board_renderer: BoardRenderer
  - checker_renderer: CheckerRenderer
  - dice_renderer: DiceRenderer
- **Methods**:
  - draw()
  - handle_click(pos)
  - update()

## Relationship Map

- BackgammonGame ─┬─> Board
                  ├─> Dice
                  └─> Player

- Board ─────────┬─> Checker
                 └─> Point

- PygameUI ─────┬─> BackgammonGame
                └─> BackgammonBoard

- BackgammonBoard ─┬─> BoardRenderer
                   ├─> CheckerRenderer
                   └─> DiceRenderer

## Testing Coverage

Para ver la cobertura de tests detallada:
```bash
python -m pytest --cov=. --cov-report=term-missing
```