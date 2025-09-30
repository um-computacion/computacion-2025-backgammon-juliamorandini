# Automated Reports
## Coverage Report
```text
Name                     Stmts   Miss  Cover   Missing
------------------------------------------------------
core/BackgammonGame.py      57      2    96%   67-68
core/Checker.py             52     12    77%   13-17, 24-25, 29, 31, 34, 50, 68
core/Dice.py                63      0   100%
core/__init__.py             6      0   100%
core/board.py               63      6    90%   30, 46, 73, 86, 88, 103
core/player.py              27      0   100%
test/test_Game.py           58      9    84%   24-29, 52-56, 122
test/test_board.py          67      1    99%   155
test/test_checker.py        42      4    90%   53-55, 77
test/test_dice.py          121      2    98%   178, 184
test/test_player.py         49      1    98%   87
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
************* Module core.Dice
core/Dice.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/Dice.py:1:0: C0103: Module name "Dice" doesn't conform to snake_case naming style (invalid-name)
************* Module core.BackgammonGame
core/BackgammonGame.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/BackgammonGame.py:1:0: C0103: Module name "BackgammonGame" doesn't conform to snake_case naming style (invalid-name)
core/BackgammonGame.py:22:12: W0612: Unused variable 'i' (unused-variable)
************* Module core.board
core/board.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/board.py:7:8: C0104: Disallowed name "bar" (disallowed-name)
************* Module core.player
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

-----------------------------------
Your code has been rated at 0.00/10


```
