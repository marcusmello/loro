# pylint:disable=missing-module-docstring
# pylint:disable=missing-function-docstring

def case_variations(string: str):
    return [
        string,
        string.capitalize(),
        string.upper(),
        string.lower(),
        string.swapcase(),
        string.casefold(),
    ]
