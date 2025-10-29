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

### Ejecutar Tests y Generar Reportes

1. Para ejecutar todos los tests y generar reporte de cobertura:
```bash
coverage run -m unittest discover -s test
coverage report
```

2. Para generar un reporte más detallado en HTML:
```bash
coverage run -m unittest discover -s test
coverage html
```

3. Para ver los tests que fallan o tienen errores:
```bash
python -m unittest discover -v -s test
```

4. Para generar todos los reportes (incluyendo pylint):
```bash
python generate_reports.py
```

### Ver Resultados

- El reporte de cobertura se mostrará en la terminal después de ejecutar `coverage report`
- El reporte HTML se generará en el directorio `htmlcov/`
- Los reportes generados por `generate_reports.py` se guardarán en:
  - `coverage_report.txt`: Reporte de cobertura
  - `pylint_report.txt`: Reporte de análisis de código
  - `cobertura.xml`: Reporte en formato XML

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
  - dice: Dice
  - dice_values: List[int]
  - moves_made: int
  - game_over: bool
- **Methods**:
  - roll_dice() -> List[int]
  - move_checker(from_point: int, to_point: int) -> bool
  - next_turn() -> None
  - is_game_over() -> bool
  - add_to_bar() -> None
  - must_move_from_bar() -> bool
  - can_bear_off() -> bool

#### Board
- **Attributes**:
  - points: Dict[int, List[Checker]]
  - bar: Dict[str, int]
  - borne_off: Dict[str, int]
- **Methods**:
  - initialize_board() -> None
  - move_checker(from_point: int, to_point: int) -> bool
  - can_bear_off(color: str) -> bool
  - is_valid_move(from_point: int, to_point: int) -> bool
  - get_point_content(point: int) -> List[Checker]
  - remove_from_point(point: int) -> Checker
  - add_to_point(point: int, checker: Checker) -> None

#### Checker
- **Attributes**:
  - color: str
  - position: Union[int, str]
  - is_on_bar: bool
  - is_borne_off: bool
- **Methods**:
  - move_to(point: int) -> bool
  - can_move_to(point: int, board: Board) -> bool
  - send_to_bar() -> None
  - bear_off() -> None

#### Dice
- **Attributes**:
  - values: List[int]
  - moves_available: List[int]
- **Methods**:
  - roll() -> List[int]
  - get_available_moves() -> List[int]
  - use_move(value: int) -> bool
  - reset_moves() -> None

#### Player
- **Attributes**:
  - color: str
  - name: str
- **Methods**:
  - get_color() -> str
  - get_name() -> str

### UI Classes

#### PygameUI (Game Interface)
- **Attributes**:
  - game: BackgammonGame
  - board: BackgammonBoard
  - screen: pygame.Surface
  - clock: pygame.time.Clock
  - running: bool
  - selected_point: Optional[int]
  - buttons: List[Button]
- **Methods**:
  - run() -> None
  - handle_events() -> None
  - update() -> None
  - draw() -> None
  - handle_click(pos: Tuple[int, int]) -> None
  - reset_game() -> None

#### BackgammonBoard (UI Board)
- **Attributes**:
  - game: BackgammonGame
  - board_renderer: BoardRenderer
  - checker_renderer: CheckerRenderer
  - dice_renderer: DiceRenderer
  - interaction: BoardInteraction
  - selected_point: Optional[int]
- **Methods**:
  - draw(surface: pygame.Surface) -> None
  - handle_click(pos: Tuple[int, int]) -> None
  - update() -> None
  - reset() -> None

#### BoardRenderer
- **Attributes**:
  - _inner_left: int
  - _inner_right: int
  - _inner_top: int
  - _inner_bottom: int
  - _point_width: int
- **Methods**:
  - draw(surface: pygame.Surface) -> None
  - _draw_border(surface: pygame.Surface) -> None
  - _draw_board_background(surface: pygame.Surface) -> None
  - _draw_points(surface: pygame.Surface) -> None
  - _draw_single_point(surface: pygame.Surface, point: int) -> None
  - _draw_bar(surface: pygame.Surface) -> None

#### CheckerRenderer
- **Attributes**:
  - _inner_left: int
  - _inner_top: int
  - _inner_bottom: int
  - _point_width: int
- **Methods**:
  - draw(surface: pygame.Surface, board: Board) -> None
  - _draw_single_checker(surface: pygame.Surface, x: int, y: int, color: str) -> None
  - _draw_point_checkers(surface: pygame.Surface, point: int, checkers: List[Checker]) -> None
  - _draw_bar_checkers(surface: pygame.Surface, bar: Dict[str, int]) -> None
  - _draw_borne_off_checkers(surface: pygame.Surface, borne_off: Dict[str, int]) -> None

#### DiceRenderer
- **Attributes**:
  - None
- **Methods**:
  - draw(surface: pygame.Surface, dice_values: List[int]) -> None
  - _draw_die(surface: pygame.Surface, x: int, y: int, value: int) -> None
  - _draw_dot(surface: pygame.Surface, x: int, y: int) -> None

#### BoardInteraction
- **Attributes**:
  - _board: BackgammonBoard
  - _selected_point: Optional[int]
  - _mouse_pos: Tuple[int, int]
- **Methods**:
  - handle_event(event: pygame.event.Event) -> None
  - handle_mouse_motion(pos: Tuple[int, int]) -> None
  - handle_click(pos: Tuple[int, int]) -> None
  - get_clicked_point(pos: Tuple[int, int]) -> Optional[int]

#### Button
- **Attributes**:
  - rect: pygame.Rect
  - text: str
  - color: Tuple[int, int, int]
  - hover_color: Tuple[int, int, int]
  - is_hovered: bool
  - callback: Callable
- **Methods**:
  - draw(surface: pygame.Surface) -> None
  - handle_event(event: pygame.event.Event) -> None
  - handle_mouse_motion(pos: Tuple[int, int]) -> None

### CLI Classes

#### BackgammonCLI
- **Attributes**:
  - game: BackgammonGame
  - running: bool
- **Methods**:
  - run() -> None
  - print_board() -> None
  - handle_command(command: str) -> None
  - get_input() -> str
  - process_move_command(args: List[str]) -> None
  - print_help() -> None

## Relationship Map

### Core Components
```
BackgammonGame ─┬─> Board ─────┬─> Checker
                ├─> Dice       └─> Dict[points]
                └─> Player
```

### UI Components
```
PygameUI ─────┬─> BackgammonGame
              └─> BackgammonBoard ─┬─> BoardRenderer
                                  ├─> CheckerRenderer
                                  ├─> DiceRenderer
                                  └─> BoardInteraction

Button <─── PygameUI
```

### CLI Components
```
BackgammonCLI ─┬─> BackgammonGame
               └─> Board
```

### Interaction Flow
```
User Input ─┬─> PygameUI ───> BoardInteraction ───> BackgammonGame
            └─> CLI ────────> Command Parser ────> BackgammonGame
```

## Testing Coverage

Para ver la cobertura de tests detallada:
```bash
python -m pytest --cov=. --cov-report=term-missing
```