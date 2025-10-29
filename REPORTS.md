# Automated Reports
## Coverage Report
```text
Name                             Stmts   Miss  Cover   Missing
--------------------------------------------------------------
PygameUI.py                        279    175    37%   101-114, 119-120, 123-124, 147, 205-277, 281-414, 418, 422-505, 512-513, 517
cli/CLI.py                         121      6    95%   94, 102, 193-194, 239-240
cli/__init__.py                      0      0   100%
config.py                           35      0   100%
core/BackgammonGame.py              76      0   100%
core/Checker.py                     54      1    98%   123
core/Dice.py                        63      0   100%
core/__init__.py                     6      0   100%
core/board.py                       95      0   100%
core/player.py                      27      0   100%
pygame_ui/__init__.py                0      0   100%
pygame_ui/backgammon_board.py       46      0   100%
pygame_ui/board_interaction.py      71      0   100%
pygame_ui/board_renderer.py         55      0   100%
pygame_ui/button.py                 24      0   100%
pygame_ui/checker_renderer.py       74      0   100%
pygame_ui/dice_renderer.py          51      0   100%
test/test_Game.py                  302      1    99%   452
test/test_backgammon_board.py       90      4    96%   151-152, 225-226
test/test_board.py                 169      1    99%   307
test/test_boardinteraction.py      115      1    99%   249
test/test_boardrender.py           142      5    96%   226-227, 244-245, 249
test/test_button.py                 57      1    98%   154
test/test_checker.py               101      1    99%   195
test/test_checkerrender.py         152      4    97%   28-30, 324
test/test_cli.py                   166      1    99%   300
test/test_dice.py                  121      2    98%   178, 184
test/test_dicerender.py             67      1    99%   130
test/test_player.py                 48      1    98%   87
test/test_pygame.py                113      1    99%   258
--------------------------------------------------------------
TOTAL                             2720    206    92%

```
## Pylint Report
```text
************* Module computacion-2025-backgammon-juliamorandini.core
core/__init__.py:7:0: C0304: Final newline missing (missing-final-newline)
core/__init__.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module computacion-2025-backgammon-juliamorandini.core.Dice
core/Dice.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/Dice.py:1:0: C0103: Module name "Dice" doesn't conform to snake_case naming style (invalid-name)
************* Module computacion-2025-backgammon-juliamorandini.core.BackgammonGame
core/BackgammonGame.py:1:0: C0103: Module name "BackgammonGame" doesn't conform to snake_case naming style (invalid-name)
core/BackgammonGame.py:3:0: E0401: Unable to import 'core.board' (import-error)
core/BackgammonGame.py:4:0: E0401: Unable to import 'core.player' (import-error)
core/BackgammonGame.py:5:0: E0401: Unable to import 'core.Dice' (import-error)
core/BackgammonGame.py:53:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
************* Module computacion-2025-backgammon-juliamorandini.core.board
core/board.py:182:0: C0325: Unnecessary parens after 'not' keyword (superfluous-parens)
core/board.py:184:0: C0325: Unnecessary parens after 'not' keyword (superfluous-parens)
core/board.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/board.py:10:8: C0104: Disallowed name "bar" (disallowed-name)
************* Module computacion-2025-backgammon-juliamorandini.core.player
core/player.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/player.py:1:0: R0902: Too many instance attributes (9/7) (too-many-instance-attributes)
************* Module computacion-2025-backgammon-juliamorandini.core.Checker
core/Checker.py:100:0: C0325: Unnecessary parens after 'not' keyword (superfluous-parens)
core/Checker.py:1:0: C0103: Module name "Checker" doesn't conform to snake_case naming style (invalid-name)
core/Checker.py:3:0: W0611: Unused Optional imported from typing (unused-import)
************* Module computacion-2025-backgammon-juliamorandini.test.test_cli
test/test_cli.py:9:0: E0401: Unable to import 'cli.CLI' (import-error)
test/test_cli.py:16:0: E0401: Unable to import 'core.BackgammonGame' (import-error)
test/test_cli.py:244:36: W0613: Unused argument 'mock_input' (unused-argument)
test/test_cli.py:258:50: W0613: Unused argument 'mock_input' (unused-argument)
test/test_cli.py:276:43: W0613: Unused argument 'mock_input' (unused-argument)
test/test_cli.py:288:39: W0613: Unused argument 'mock_input' (unused-argument)
************* Module computacion-2025-backgammon-juliamorandini.test.test_checkerrender
test/test_checkerrender.py:19:0: R0903: Too few public methods (0/2) (too-few-public-methods)
test/test_checkerrender.py:33:0: E0401: Unable to import 'pygame_ui.checker_renderer' (import-error)
test/test_checkerrender.py:33:0: C0413: Import "from pygame_ui.checker_renderer import CheckerRenderer" should be placed at the top of the module (wrong-import-position)
************* Module computacion-2025-backgammon-juliamorandini.test.test_dicerender
test/test_dicerender.py:12:0: E0401: Unable to import 'pygame_ui.dice_renderer' (import-error)
test/test_dicerender.py:13:0: E0401: Unable to import 'config' (import-error)
************* Module computacion-2025-backgammon-juliamorandini.test.test_checker
test/test_checker.py:9:0: E0401: Unable to import 'core.Checker' (import-error)
************* Module computacion-2025-backgammon-juliamorandini.test.test_player
test/test_player.py:1:0: C0114: Missing module docstring (missing-module-docstring)
test/test_player.py:2:0: E0401: Unable to import 'core.player' (import-error)
test/test_player.py:5:0: C0115: Missing class docstring (missing-class-docstring)
************* Module computacion-2025-backgammon-juliamorandini.test.test_pygame
test/test_pygame.py:21:0: E0401: Unable to import 'PygameUI' (import-error)
test/test_pygame.py:22:0: E0401: Unable to import 'pygame_ui.backgammon_board' (import-error)
************* Module computacion-2025-backgammon-juliamorandini.test.test_button
test/test_button.py:12:0: E0401: Unable to import 'pygame_ui.button' (import-error)
test/test_button.py:7:0: C0411: standard import "unittest.mock.patch" should be placed before third party import "pygame" (wrong-import-order)
************* Module computacion-2025-backgammon-juliamorandini.test.test_boardrender
test/test_boardrender.py:14:0: E0401: Unable to import 'pygame_ui.board_renderer' (import-error)
************* Module computacion-2025-backgammon-juliamorandini.test.test_backgammon_board
test/test_backgammon_board.py:16:0: E0401: Unable to import 'pygame_ui.backgammon_board' (import-error)
test/test_backgammon_board.py:45:8: C0103: Attribute name "MockBoard" doesn't conform to snake_case naming style (invalid-name)
test/test_backgammon_board.py:46:8: C0103: Attribute name "MockDice" doesn't conform to snake_case naming style (invalid-name)
test/test_backgammon_board.py:47:8: C0103: Attribute name "MockBoardRenderer" doesn't conform to snake_case naming style (invalid-name)
test/test_backgammon_board.py:48:8: C0103: Attribute name "MockCheckerRenderer" doesn't conform to snake_case naming style (invalid-name)
test/test_backgammon_board.py:49:8: C0103: Attribute name "MockDiceRenderer" doesn't conform to snake_case naming style (invalid-name)
test/test_backgammon_board.py:19:0: R0902: Too many instance attributes (17/7) (too-many-instance-attributes)
test/test_backgammon_board.py:10:0: C0411: standard import "unittest.mock.patch" should be placed before third party import "pygame" (wrong-import-order)
************* Module computacion-2025-backgammon-juliamorandini.test.test_boardinteraction
test/test_boardinteraction.py:244:0: C0301: Line too long (112/100) (line-too-long)
test/test_boardinteraction.py:13:0: E0401: Unable to import 'pygame_ui.board_interaction' (import-error)
test/test_boardinteraction.py:14:0: E0401: Unable to import 'config' (import-error)
test/test_boardinteraction.py:108:4: C0103: Method name "setUpClass_for_clicks" doesn't conform to snake_case naming style (invalid-name)
test/test_boardinteraction.py:8:0: C0411: standard import "unittest.mock.patch" should be placed before third party import "pygame" (wrong-import-order)
************* Module computacion-2025-backgammon-juliamorandini.test.test_dice
test/test_dice.py:1:0: C0114: Missing module docstring (missing-module-docstring)
test/test_dice.py:3:0: E0401: Unable to import 'core.Dice' (import-error)
test/test_dice.py:35:4: C0116: Missing function or method docstring (missing-function-docstring)
test/test_dice.py:55:4: C0116: Missing function or method docstring (missing-function-docstring)
test/test_dice.py:67:4: C0116: Missing function or method docstring (missing-function-docstring)
test/test_dice.py:6:0: R0904: Too many public methods (22/20) (too-many-public-methods)
************* Module computacion-2025-backgammon-juliamorandini.test.test_Game
test/test_Game.py:1:0: C0103: Module name "test_Game" doesn't conform to snake_case naming style (invalid-name)
test/test_Game.py:4:0: E0401: Unable to import 'core.BackgammonGame' (import-error)
test/test_Game.py:7:0: R0904: Too many public methods (55/20) (too-many-public-methods)
************* Module computacion-2025-backgammon-juliamorandini.test.test_board
test/test_board.py:9:0: E0401: Unable to import 'core.board' (import-error)
test/test_board.py:1:0: R0801: Similar lines in 2 files
==computacion-2025-backgammon-juliamorandini.test.test_boardrender:[28:35]
==computacion-2025-backgammon-juliamorandini.test.test_checkerrender:[43:50]
        mock_config = self.patcher.start()

        self.addCleanup(self.patcher.stop)

        mock_config.BOARD_X = 10
        mock_config.BOARD_Y = 10
        mock_config.BORDER_THICKNESS = 5 (duplicate-code)

-----------------------------------
Your code has been rated at 9.25/10


```
