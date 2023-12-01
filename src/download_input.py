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


def download(year, day):
    """Get input and write it to input.txt inside the puzzle folder
    
    Get example(s) and answer(s)"""
    puzzle = Puzzle(year=year, day=day)

    # Download input
    year_path = pathlib.Path(__file__).parent / str(year)
    output_path = next(year_path.glob(f"{day:02d}*")) / "input.txt"
    output_path.write_text(puzzle.input_data)

    # Download example data
    for _, example in enumerate(puzzle.examples):
        match example:
            case example:
                if example.input_data is not None:
                    output_path = output_path.with_stem(f"example{_}input")
                    output_path.write_text(example.input_data)
                if example.answer_a is not None:
                    output_path = output_path.with_stem(f"example{_}answerA")
                    output_path.write_text(example.answer_a)
                if example.answer_b is not None:
                    output_path = output_path.with_stem(f"example{_}answerB")
                    output_path.write_text(example.answer_b)
                if example.extra is not None:
                    output_path = output_path.with_stem(f"example{_}extra")
                    output_path.write_text(example.extra)

    # Add README with link to puzzle text
    readme_path = output_path.with_name("README.md")
    readme_path.write_text(
        f"# {puzzle.title}\n\n"
        f"**Advent of Code: Day {day}, {year}**\n\n"
        f"See {puzzle.url}\n"
    )


if __name__ == "__main__":
    try:
        # Read year and day from command line
        download(year=int(sys.argv[1]), day=int(sys.argv[2]))
    except Exception as err:
        # Catch exceptions so that Copier doesn't clean up directories
        print(f"Download of input failed: {err}")
        raise SystemExit()
