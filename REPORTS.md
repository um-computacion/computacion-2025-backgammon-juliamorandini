# Automated Reports
## Coverage Report
```text
Name                     Stmts   Miss  Cover   Missing
------------------------------------------------------
cli/CLI.py                  73      8    89%   65-67, 90, 123-124, 128-129
cli/__init__.py              0      0   100%
core/BackgammonGame.py      57      6    89%   69-70, 94-95, 99-100
core/Checker.py             54     11    80%   36-41, 65, 67, 70, 101, 123
core/Dice.py                63      0   100%
core/__init__.py             6      0   100%
core/board.py               65      8    88%   43, 56, 90, 103, 121, 123, 136, 143
core/player.py              27      0   100%
test/test_Game.py           50      1    98%   80
test/test_board.py          67      1    99%   163
test/test_checker.py        44      1    98%   79
test/test_cli.py            74      1    99%   110
test/test_dice.py          121      2    98%   178, 184
test/test_player.py         49      1    98%   87
------------------------------------------------------
TOTAL                      750     40    95%

```
## Pylint Report
```text
************* Module core
core/__init__.py:7:0: C0304: Final newline missing (missing-final-newline)
core/__init__.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module core.Dice
core/Dice.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/Dice.py:1:0: C0103: Module name "Dice" doesn't conform to snake_case naming style (invalid-name)
************* Module core.BackgammonGame
core/BackgammonGame.py:1:0: C0103: Module name "BackgammonGame" doesn't conform to snake_case naming style (invalid-name)
************* Module core.board
core/board.py:139:0: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:12:8: C0104: Disallowed name "bar" (disallowed-name)
************* Module core.player
core/player.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/player.py:1:0: R0902: Too many instance attributes (9/7) (too-many-instance-attributes)
************* Module core.Checker
core/Checker.py:100:0: C0325: Unnecessary parens after 'not' keyword (superfluous-parens)
core/Checker.py:1:0: C0103: Module name "Checker" doesn't conform to snake_case naming style (invalid-name)
core/Checker.py:3:0: W0611: Unused Optional imported from typing (unused-import)
************* Module test.test_cli
test/test_cli.py:77:0: C0303: Trailing whitespace (trailing-whitespace)
test/test_cli.py:29:40: W0613: Unused argument 'mock_input' (unused-argument)
test/test_cli.py:35:42: W0613: Unused argument 'mock_input' (unused-argument)
test/test_cli.py:59:49: W0613: Unused argument 'mock_input' (unused-argument)
test/test_cli.py:70:49: W0613: Unused argument 'mock_input' (unused-argument)
test/test_cli.py:80:52: W0613: Unused argument 'mock_input' (unused-argument)
test/test_cli.py:90:49: W0613: Unused argument 'mock_input' (unused-argument)
test/test_cli.py:101:49: W0613: Unused argument 'mock_input' (unused-argument)
************* Module test.test_player
test/test_player.py:1:0: C0114: Missing module docstring (missing-module-docstring)
test/test_player.py:5:0: C0115: Missing class docstring (missing-class-docstring)
test/test_player.py:90:0: W0105: String statement has no effect (pointless-string-statement)
************* Module test.test_dice
test/test_dice.py:1:0: C0114: Missing module docstring (missing-module-docstring)
test/test_dice.py:35:4: C0116: Missing function or method docstring (missing-function-docstring)
test/test_dice.py:55:4: C0116: Missing function or method docstring (missing-function-docstring)
test/test_dice.py:67:4: C0116: Missing function or method docstring (missing-function-docstring)
test/test_dice.py:6:0: R0904: Too many public methods (22/20) (too-many-public-methods)
************* Module test.test_Game
test/test_Game.py:1:0: C0103: Module name "test_Game" doesn't conform to snake_case naming style (invalid-name)
test/test_Game.py:82:0: W0105: String statement has no effect (pointless-string-statement)
************* Module test.test_board
test/test_board.py:1:0: C0114: Missing module docstring (missing-module-docstring)
test/test_board.py:5:0: C0115: Missing class docstring (missing-class-docstring)
test/test_board.py:12:4: C0116: Missing function or method docstring (missing-function-docstring)
test/test_board.py:37:4: C0116: Missing function or method docstring (missing-function-docstring)
test/test_board.py:60:4: C0116: Missing function or method docstring (missing-function-docstring)
test/test_board.py:72:4: C0116: Missing function or method docstring (missing-function-docstring)
test/test_board.py:82:4: C0116: Missing function or method docstring (missing-function-docstring)
test/test_board.py:92:4: C0116: Missing function or method docstring (missing-function-docstring)
test/test_board.py:102:4: C0116: Missing function or method docstring (missing-function-docstring)
test/test_board.py:152:4: C0116: Missing function or method docstring (missing-function-docstring)

-----------------------------------
Your code has been rated at 9.39/10


```
