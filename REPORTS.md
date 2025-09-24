# Automated Reports
## Coverage Report
```text
Name                     Stmts   Miss  Cover   Missing
------------------------------------------------------
core/BackgammonGame.py      57      2    96%   64-65
core/Checker.py             52     12    77%   13-17, 24-25, 29, 31, 34, 50, 68
core/Dice.py                63      0   100%
core/__init__.py             6      0   100%
core/board.py               63      6    90%   28, 42, 65, 78, 80, 95
core/player.py              27      0   100%
test/test_Game.py           58      9    84%   21-26, 49-53, 110
test/test_board.py          67      1    99%   122
test/test_checker.py        42      4    90%   52-54, 75
test/test_dice.py          121      2    98%   177, 182
test/test_player.py         49      1    98%   85
------------------------------------------------------
TOTAL                      605     37    94%

```
## Pylint Report
```text
************* Module test
test/__init__.py:1:0: F0010: error while code parsing: Unable to load file test/__init__.py:
[Errno 2] No such file or directory: 'test/__init__.py' (parse-error)
************* Module core
core/__init__.py:7:0: C0304: Final newline missing (missing-final-newline)
core/__init__.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module core.BackgammonGame
core/BackgammonGame.py:35:0: C0301: Line too long (108/100) (line-too-long)
core/BackgammonGame.py:88:0: C0303: Trailing whitespace (trailing-whitespace)
core/BackgammonGame.py:93:0: C0303: Trailing whitespace (trailing-whitespace)
core/BackgammonGame.py:97:0: C0304: Final newline missing (missing-final-newline)
core/BackgammonGame.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/BackgammonGame.py:1:0: C0103: Module name "BackgammonGame" doesn't conform to snake_case naming style (invalid-name)
core/BackgammonGame.py:21:12: W0612: Unused variable 'i' (unused-variable)
************* Module core.player
core/player.py:3:0: C0303: Trailing whitespace (trailing-whitespace)
core/player.py:15:0: C0303: Trailing whitespace (trailing-whitespace)
core/player.py:44:0: C0303: Trailing whitespace (trailing-whitespace)
core/player.py:77:0: C0303: Trailing whitespace (trailing-whitespace)
core/player.py:80:0: C0304: Final newline missing (missing-final-newline)
core/player.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/player.py:1:0: R0902: Too many instance attributes (9/7) (too-many-instance-attributes)
************* Module core.Checker
core/Checker.py:9:0: C0325: Unnecessary parens after '=' keyword (superfluous-parens)
core/Checker.py:40:0: C0303: Trailing whitespace (trailing-whitespace)
core/Checker.py:44:0: C0303: Trailing whitespace (trailing-whitespace)
core/Checker.py:49:0: C0325: Unnecessary parens after 'not' keyword (superfluous-parens)
core/Checker.py:64:0: C0303: Trailing whitespace (trailing-whitespace)
core/Checker.py:69:0: C0303: Trailing whitespace (trailing-whitespace)
core/Checker.py:71:0: C0304: Final newline missing (missing-final-newline)
core/Checker.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/Checker.py:1:0: C0103: Module name "Checker" doesn't conform to snake_case naming style (invalid-name)
core/Checker.py:1:0: C0115: Missing class docstring (missing-class-docstring)
core/Checker.py:12:4: C0116: Missing function or method docstring (missing-function-docstring)
core/Checker.py:19:4: C0116: Missing function or method docstring (missing-function-docstring)
core/Checker.py:23:4: C0116: Missing function or method docstring (missing-function-docstring)
core/Checker.py:27:4: C0116: Missing function or method docstring (missing-function-docstring)
core/Checker.py:57:4: C0116: Missing function or method docstring (missing-function-docstring)
************* Module core.Dice
core/Dice.py:79:0: C0303: Trailing whitespace (trailing-whitespace)
core/Dice.py:86:0: C0303: Trailing whitespace (trailing-whitespace)
core/Dice.py:99:0: C0304: Final newline missing (missing-final-newline)
core/Dice.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/Dice.py:1:0: C0103: Module name "Dice" doesn't conform to snake_case naming style (invalid-name)
************* Module core.board
core/board.py:16:68: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:29:0: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:33:0: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:37:0: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:39:37: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:40:47: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:43:0: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:52:0: C0301: Line too long (107/100) (line-too-long)
core/board.py:64:0: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:86:0: C0303: Trailing whitespace (trailing-whitespace)
core/board.py:95:0: C0304: Final newline missing (missing-final-newline)
core/board.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/board.py:7:8: C0104: Disallowed name "bar" (disallowed-name)

-----------------------------------
Your code has been rated at 0.00/10


```
