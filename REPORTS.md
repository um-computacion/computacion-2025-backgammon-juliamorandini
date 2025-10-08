# Automated Reports
## Coverage Report
```text
Name                     Stmts   Miss  Cover   Missing
------------------------------------------------------
core/BackgammonGame.py      57      6    89%   69-70, 94-95, 99-100
core/Checker.py             54     11    80%   36-41, 65, 67, 70, 101, 123
core/Dice.py                63      0   100%
core/__init__.py             6      0   100%
core/board.py               65      8    88%   43, 56, 90, 103, 121, 123, 136, 143
core/player.py              27      0   100%
test/test_Game.py           50      1    98%   80
test/test_board.py          67      1    99%   163
test/test_checker.py        44      1    98%   79
test/test_dice.py          121      2    98%   178, 184
test/test_player.py         49      1    98%   87
------------------------------------------------------
TOTAL                      603     31    95%

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

-----------------------------------
Your code has been rated at 0.00/10


```
