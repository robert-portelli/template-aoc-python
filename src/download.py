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


YEAR = int(sys.argv[1])
DAY = int(sys.argv[2])
PUZZLE = Puzzle(year=YEAR, day=DAY)
YEAR_PATH = pathlib.Path(__file__).parent / str(YEAR)


def main():
    try:
        # Read year and day from command line
        input_dump()
        examples_dump()
    except Exception as err:
        # Catch exceptions so that Copier doesn't clean up directories
        print(f"Download of input failed: {err}")
        raise SystemExit()


def input_dump():
    # Download input
    output_path = next(YEAR_PATH.glob(f"{DAY:02d}*")) / "INPUT.toml"
    # output_path.write_text(puzzle.input_data)
    with open(output_path, "wb") as f:
        dump(
            # value is a list of strings
            {"input": PUZZLE.input_data.strip().split()},
            f,
        )


def _compose_toml():
    array = [
        {key: value for key, value in example._asdict().items() if value is not None}
        for example in PUZZLE.examples
    ]

    return {f"example-{_+1}": example for _, example in enumerate(array)}


def examples_dump():
    output_path = next(YEAR_PATH.glob(f"{DAY:02d}*")) / "EXAMPLES.toml"
    with open(output_path, "wb") as f:
        dump(_compose_toml(), f)


if __name__ == "__main__":
    main()
