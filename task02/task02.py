from itertools import cycle
from random import randint, shuffle
from typing import Tuple


def new_game():
    with open('logo.txt', encoding='utf8') as logo:
        print(logo.read())

    initial_input = ""
    while initial_input.lower() not in ("x", "o", "q"):
        initial_input = input("Choose your side: X or O. Type Q to exit. ").lower()
    if initial_input == "q":
        quit()

    return main(initial_input)


def main(initial_input: str):
    turn_funcs = cycle((human_move, pc_move))
    if initial_input == "o":
        next(turn_funcs)
    signs = cycle(("X", "O"))
    field = [[" "] * 10 for _ in range(10)]
    legal_moves = {(i, j) for i in range(10) for j in range(10)}
    field_print(field)
    while True:
        sign = next(signs)
        turn_func = next(turn_funcs)
        row, col = turn_func(legal_moves, sign, field)

        field[row][col] = sign
        field_print(field)

        if check_lose(row, col, sign, field):
            print(f"{sign} loses the match! Cell {row + 1, col + 1}")
            break

        if not legal_moves:
            print(f"It's a draw!")
            break


def pc_move(legal_moves: set, sign: str, field) -> Tuple:
    """PC plays random not loosing move, if available."""
    shuffled_legal_moves = list(legal_moves)
    shuffle(shuffled_legal_moves)
    for r, c in shuffled_legal_moves:
        field[r][c] = sign
        if not check_lose(r, c, sign, field):
            field[r][c] = " "
            legal_moves.discard((r, c))
            return r, c

        field[r][c] = " "
    return legal_moves.pop()


def human_move(legal_moves: set, *args, **kwargs) -> Tuple:
    """Get input and validate.
    Return 0-indexed coordinates"""
    while True:
        try:
            x, y = map(int, input("Enter row and column. Space separated. ").split())
            # uncomment line below for automated random human input
            # x, y = randint(1, 10), randint(1, 10)
        except ValueError as e:
            print(e)
        else:
            if not (0 < x < 11 and 0 < y < 11):
                print("Out of boundaries. Try again.")
            elif (x - 1, y - 1) not in legal_moves:
                print("Illegal move. Try again.")
            else:
                legal_moves.discard((x - 1, y - 1))
                return x - 1, y - 1


def check_lose(row: int, col: int, sign: str, field) -> bool:
    """Return True if current row+col looses with given sign, False otherwise."""
    return (
        # check horizontal
        any(
            [
                field[row][i: i + 5].count(sign) == 5
                for i in range(col - 5, col + 1)
                if 0 <= i and i + 5 < 10
            ]
        )
        # check vertical
        or any(
            [
                [field[i][col] for i in range(r, r + 5)].count(sign) == 5
                for r in range(row - 5, row + 1)
                if 0 <= r and r + 5 < 10
            ]
        )
        # check lines parallel to main diagonal
        or any(
            [
                [field[i][j] for i, j in zip(range(r, r + 5), range(c, c + 5))].count(
                    sign
                )
                == 5
                for r, c in zip(range(row - 4, row + 1), range(col - 4, col + 1))
                if c >= 0 <= r and r + 5 < 11 > c + 5
            ]
        )
        # check lines parallel to anti-diagonal
        or any(
            [
                [
                    field[i][j] for i, j in zip(range(r, r + 5), range(c, c - 5, -1))
                ].count(sign)
                == 5
                for r, c in zip(range(row - 4, row + 1), range(col + 4, col - 1, -1))
                if r >= 0 and r + 5 < 11 and c - 5 >= -1 and c < 10
            ]
        )
    )


def field_print(field) -> None:
    """Game field printer with borders."""
    underline = f"  {'-' * (10 * 4 + 1)}"
    print(" " * 4, end="")
    print(*range(1, 10 + 1), sep=" | ")
    print(underline)
    for n, row in enumerate(field, 1):
        print(f"{n}|".rjust(3), end=" ")
        print(*row, sep=" | ", end=" |\n")
        print(underline)
    print()


if __name__ == "__main__":
    while True:
        new_game()
