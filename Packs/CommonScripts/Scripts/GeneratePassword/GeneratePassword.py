import demistomock as demisto
from CommonServerPython import *
from CommonServerUserPython import *

import random
import secrets
import string

DEFAULT_MIN = 0
DEFAULT_MAX = 10

LOWERCASE_CHARS = string.ascii_lowercase
UPPERCASE_CHARS = string.ascii_uppercase
DIGITS = string.digits
SYMBOLS = "!@#$%^&*()[]+:\"?_><=';/-.,\\|"


def randomize_number_in_range(min_val: int, max_val: int) -> int:
    n = max(max_val - min_val, 0)
    return secrets.randbelow(n + 1) + min_val


def print_char_values(pw):
    ascii_values = [ord(char) for char in pw]
    ascii_string = ', '.join(str(value) for value in ascii_values)
    demisto.debug(f"ASCII for password = {ascii_string}")


def generate_password(args: Dict[str, Any]) -> CommandResults:
    is_debug = argToBoolean(args.get('debug'))
    min_lowercase = arg_to_number(args.get('min_lcase')) or DEFAULT_MIN
    max_lowercase = arg_to_number(args.get('max_lcase')) or DEFAULT_MAX
    min_uppercase = arg_to_number(args.get('min_ucase')) or DEFAULT_MIN
    max_uppercase = arg_to_number(args.get('max_ucase')) or DEFAULT_MAX
    min_digits = arg_to_number(args.get('min_digits')) or DEFAULT_MIN
    max_digits = arg_to_number(args.get('max_digits')) or DEFAULT_MAX
    min_symbols = arg_to_number(args.get('min_symbols')) or DEFAULT_MIN
    max_symbols = arg_to_number(args.get('max_symbols')) or DEFAULT_MAX

    # randomize the amount of characters we get as per parameters
    num_upper = randomize_number_in_range(min_uppercase, max_uppercase)
    num_lower = randomize_number_in_range(min_lowercase, max_lowercase)
    num_digits = randomize_number_in_range(min_digits, max_digits)
    num_symbols = randomize_number_in_range(min_symbols, max_symbols)

    if num_upper + num_lower + num_digits + num_symbols == 0:
        raise DemistoException("error: insane password. No character length.")

    # start with a blank password
    pw = []

    # iterate through each character class and add
    for _ in range(num_upper):
        pw.append(secrets.choice(UPPERCASE_CHARS))
    for _ in range(num_lower):
        pw.append(secrets.choice(LOWERCASE_CHARS))
    for _ in range(num_digits):
        pw.append(secrets.choice(DIGITS))
    for _ in range(num_symbols):
        pw.append(secrets.choice(SYMBOLS))

    # randomize our new password string
    rpw = ''.join(random.sample(pw, len(pw)))

    if is_debug:
        print_char_values(rpw)

    return CommandResults(
        outputs_prefix="NEW_PASSWORD",
        outputs=rpw,
        readable_output=tableToMarkdown('Newly Generated Password', {'password': rpw})
    )


def main():  # pragma: no cover
    try:
        args = demisto.args()
        return_results(generate_password(args))
    except Exception as e:
        return_error(str(e))


if __name__ in ('__builtin__', 'builtins'):  # pragma: no cover
    main()