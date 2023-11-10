"""Check functions for attempts"""

from werkzeug.exceptions import NotFound, abort


def guessed_is_digit(guessed_number):
    """Checks if guessed input is a digit and returns error if not."""

    if not guessed_number.isdigit():
        return abort(400, "Not a valid number")


def check_spaces_vs_guessed_length(guessed_number, spaces):
    """Checks if spaces match the length of the number guessed. Returns an error if they dont match."""

    if len(guessed_number) != spaces:
        return abort(400, f"Guess must be {spaces} numbers long!")


def check_is_draw(attempts_count, attempts_max):
    """Checks to see if we have reached a draw by the number of attempts reaching the max allowed."""

    if attempts_count > attempts_max:
        return abort(200, "No winner. Looks like we have a draw!")
