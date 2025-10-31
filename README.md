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


## Testing Coverage

Para ver la cobertura de tests detallada:
```bash
python -m pytest --cov=. --cov-report=term-missing
```