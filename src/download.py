"""Download input for one Advent of Code puzzle if possible

Uses https://pypi.org/project/advent-of-code-data/ if it's available.
Otherwise, does nothing.
"""

# Standard library imports
import pathlib
import sys


# Third party imports
try:
    from aocd.models import Puzzle
except ImportError:
    pypi_url = "https://pypi.org/project/advent-of-code-data/"
    print(f"Install {pypi_url} to autodownload input files")
    raise SystemExit()

try:
    from tomli_w import dump
except ImportError:
    pypi_url = "https://pypi.org/project/tomli-w/"
    print(f"Install {pypi_url} into local advent of code environment \
        to dump python objects into TOML")
    raise SystemExit()

YEAR = int(sys.argv[1])
DAY = int(sys.argv[2])
PUZZLE = Puzzle(year=YEAR, day=DAY)
YEAR_PATH = pathlib.Path(__file__).parent / str(YEAR)


def main():
    """
    Main function for downloading Advent of Code input data.
    Reads year and day from the command line, then calls input_dump() and examples_dump().
    """
    try:
        # Read year and day from command line
        input_dump()
        examples_dump()
    except Exception as err:
        # Catch exceptions so that Copier doesn't clean up directories
        print(f"Download of input failed: {err}")
        raise SystemExit()


def input_dump():
    """
    Download input for the Advent of Code puzzle and save it to a TOML file.
    """
    # Download input
    output_path = next(YEAR_PATH.glob(f"{DAY:02d}*")) / "INPUT.toml"
    with open(output_path, "wb") as f:
        dump(
            # value is a list of strings
            {"input_data": PUZZLE.input_data.strip().split()},
            f,
        )


def _compose_toml():
    """
    Compose a TOML representation of examples from the Advent of Code puzzle.
    """
    array = [
        {key: value for key, value in example._asdict().items() if value is not None}
        for example in PUZZLE.examples
    ]

    return {f"example-{_+1}": example for _, example in enumerate(array)}


def examples_dump():
    """
    Download examples for the Advent of Code puzzle and save them to a TOML file.
    """
    output_path = next(YEAR_PATH.glob(f"{DAY:02d}*")) / "EXAMPLES.toml"
    with open(output_path, "wb") as f:
        dump(_compose_toml(), f)


if __name__ == "__main__":
    main()
