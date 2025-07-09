import sys
import typer
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Iterable

from typing_extensions import Annotated
from .core import process_urls, ProcessingMode

app = typer.Typer(
    name="url-refiner",
    help="A robust and elegant tool to process and deduplicate URLs.",
    add_completion=False,
    rich_markup_mode="markdown"
)


def _read_urls_from_source(input_file: Optional[str]) -> Iterable[str]:
    """
    Yields URLs from the specified source, using a generator for memory efficiency.
    """
    if input_file:
        input_path = Path(input_file)
        file_to_read = None

        if input_path.is_file():
            file_to_read = input_path
        else:
            inputs_dir = Path("Inputs")
            path_in_inputs_dir = inputs_dir / input_path.name
            if path_in_inputs_dir.is_file():
                file_to_read = path_in_inputs_dir

        if file_to_read:
            try:
                with open(file_to_read, "r", encoding="utf-8") as f:
                    for line in f:
                        stripped_line = line.strip()
                        if stripped_line:
                            yield stripped_line
            except IOError as e:
                typer.secho(f"Error: Could not read file '{file_to_read}'. Reason: {e}", fg=typer.colors.RED, err=True)
                raise typer.Exit(code=1)
        else:
            typer.secho(f"Error: Input file not found at '{input_path}' or within the 'Inputs' directory.", fg=typer.colors.RED, err=True)
            raise typer.Exit(code=1)

    elif not sys.stdin.isatty():
        for line in sys.stdin:
            stripped_line = line.strip()
            if stripped_line:
                yield stripped_line
    else:
        typer.echo("No input file provided via --input and no data from stdin. Use --help for more info.", err=True)
        raise typer.Exit(code=1)


def _write_urls_to_output(urls: List[str], stats: dict, save_to_file: bool):
    """
    Writes the processed URLs to the destination (file or stdout).
    """
    if not urls:
        typer.secho("Warning: No unique URLs were produced.", fg=typer.colors.YELLOW)
        return

    output_string = "\n".join(urls)

    if save_to_file:
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        file_name = f"refined_{timestamp}.txt"
        file_path = output_dir / file_name
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(output_string + "\n")
            typer.secho(
                f"Success! Processed {stats['total_input']} URLs. Found {stats['duplicates_removed']} duplicates. "
                f"Saved {stats['total_output']} unique URLs to '{file_path}'.",
                fg=typer.colors.GREEN
            )
        except IOError as e:
            typer.secho(f"Error: Could not write to file '{file_path}'. Reason: {e}", fg=typer.colors.RED, err=True)
            raise typer.Exit(code=1)
    else:
        print(output_string)


@app.command()
def run(
    input_file: Annotated[
        Optional[str],
        typer.Option(
            "--input",
            "-i",
            help="Path to input file. If not found, checks in 'Inputs/' dir. If omitted, reads from stdin.",
            rich_help_panel="Input & Output"
        ),
    ] = None,

    save_to_file: Annotated[
        bool,
        typer.Option(
            "--output",
            "-o",
            help="Save the output to a timestamped file in the 'output' directory.",
            rich_help_panel="Input & Output"
        ),
    ] = False,
    
    value: Annotated[
        str, 
        typer.Option("--value", "-v", help="Value to use for replacing or appending.", rich_help_panel="Processing")
    ] = "FUZZ",
    
    mode: Annotated[
        ProcessingMode, 
        typer.Option("--mode", "-m", case_sensitive=False, help="Processing mode.", rich_help_panel="Processing")
    ] = ProcessingMode.REPLACE,
    
    exclude_params: Annotated[
        Optional[List[str]], 
        typer.Option("--exclude", "-e", help="Query parameters to exclude from processing.", rich_help_panel="Filtering")
    ] = None,
    
    ignore_path: Annotated[
        bool, 
        typer.Option("--ignore-path", help="Ignore URL path for deduplication.", rich_help_panel="Filtering")
    ] = False
):
    """
    Refines a list of URLs by modifying query parameters and removing duplicates.
    """
    try:
        url_source = _read_urls_from_source(input_file)
        
        config = {
            "value": value,
            "mode": mode.value,
            "ignore_path": ignore_path,
            "exclude_params": exclude_params or []
        }
        
        # Process the stream directly without loading all into memory
        result = process_urls(url_source, config)
        
        if not result["data"] and result["stats"]["total_input"] == 0:
            typer.secho("Warning: Input is empty. No URLs to process.", fg=typer.colors.YELLOW, err=True)
            raise typer.Exit()
            
        _write_urls_to_output(result["data"], result["stats"], save_to_file=save_to_file)

    except typer.Exit:
        raise
    except Exception as e:
        typer.secho(f"An unexpected error occurred: {type(e).__name__} - {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)