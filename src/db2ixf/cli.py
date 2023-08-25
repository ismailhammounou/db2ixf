# coding=utf-8
"""CLI application of the IXF parser"""
import logging
import typer
from db2ixf import IXFParser
from db2ixf._version import version_tuple as vt
from db2ixf.logger import logger
from pathlib import Path
from typing import Annotated, Union, Optional

__version__ = f'{vt[0]}.{vt[1]}.{vt[2]}'

# Define the mapping between verbose levels and logging levels
VERBOSE_MAPPING = {
    0: logging.WARNING,
    1: logging.INFO,
    2: logging.DEBUG
}

app = typer.Typer(
    name='db2ixf',
    rich_markup_mode="markdown",
    epilog='Made with heart :D'
)


@app.command(epilog='Made with heart :D')
def json(
        file: Annotated[Path,
                        typer.Argument(
                            help='Path to the ixf FILE.',
                            exists=True,
                            dir_okay=False,
                            resolve_path=True,
                            rich_help_panel='Required Arguments',
                        )],
        output: Annotated[Union[Path, None],
                          typer.Argument(
                              help='Path to the `json` OUTPUT file.',
                              dir_okay=False,
                              readable=False,
                              resolve_path=True,
                              rich_help_panel='Optional Arguments',
                          )] = None,
        verbose: Annotated[int,
                           typer.Option(
                               '--verbose',
                               '-v',
                               metavar='',
                               help='Counter for verbosity level.',
                               count=True,
                           )] = 0,
):
    """
    Parse ixf ``FILE`` and convert it to a **json** ``OUTPUT``.
    """
    if output is None:
        output = Path.cwd()
        filename = file.name.lower().removesuffix('.ixf') + '.json'
        output /= filename

    if verbose > 2:
        logger.setLevel(VERBOSE_MAPPING[2])
    else:
        logger.setLevel(VERBOSE_MAPPING[verbose])

    logger.info(f'IXF file: {file}')
    logger.info(f'JSON file: {output}')

    parser = IXFParser(file)
    parser.to_json(output)
    raise typer.Exit()


@app.command(epilog='Made with heart :D')
def csv(
        file: Annotated[Path,
                        typer.Argument(
                            help='Path to the ixf FILE.',
                            exists=True,
                            dir_okay=False,
                            resolve_path=True,
                            rich_help_panel='Required Arguments',
                        )],
        output: Annotated[Union[Path, None],
                          typer.Argument(
                              help='Path to the `csv` OUTPUT file.',
                              dir_okay=False,
                              readable=False,
                              resolve_path=True,
                              rich_help_panel='Optional Arguments',
                          )] = None,
        sep: Annotated[Union[str, None],
                       typer.Option(
                           '--sep',
                           '-s',
                           help='Separator/Delimiter of the csv file.',
                           rich_help_panel='Command Options',
                       )] = '|',
        verbose: Annotated[int,
                           typer.Option(
                               '--verbose',
                               '-v',
                               metavar='',
                               help='Counter for verbosity level.',
                               count=True,
                           )] = 0,
):
    """
    Parse ixf ``FILE`` and convert it to a **csv** ``OUTPUT``.
    """
    if output is None:
        output = Path.cwd()
        filename = file.name.lower().removesuffix('.ixf') + '.csv'
        output /= filename

    if sep is None:
        sep = '|'

    if verbose > 2:
        logger.setLevel(VERBOSE_MAPPING[2])
    else:
        logger.setLevel(VERBOSE_MAPPING[verbose])

    logger.info(f'IXF file: {file}')
    logger.info(f'CSV file: {output}')
    logger.info(f'CSV file separator/delimiter: {sep}')

    parser = IXFParser(file)
    parser.to_csv(output, str(sep))
    raise typer.Exit()


@app.command(epilog='Made with heart :D')
def parquet(
        file: Annotated[Path,
                        typer.Argument(
                            help='Path to the ixf FILE.',
                            exists=True,
                            dir_okay=False,
                            resolve_path=True,
                            rich_help_panel='Required Arguments',
                        )],
        output: Annotated[Union[Path, None],
                          typer.Argument(
                              help='Path to the `parquet` OUTPUT file.',
                              dir_okay=False,
                              readable=False,
                              resolve_path=True,
                              rich_help_panel='Optional Arguments',
                          )] = None,
        version: Annotated[Union[str, None],
                           typer.Option(
                               '--version',
                               help='Parquet version. Please look '
                                    'at pyarrow documentation.',
                               rich_help_panel='Command Options',
                           )] = '2.4',
        batch_size: Annotated[Union[int, None],
                              typer.Option(
                                  '--batch-size',
                                  '-s',
                                  help='Size of the batch: number of '
                                       'rows to extract before writing '
                                       'to the parquet file, It is used '
                                       'for memory optimization.',
                                  rich_help_panel='Command Options',
                              )] = 1000,
        verbose: Annotated[int,
                           typer.Option(
                               '--verbose',
                               '-v',
                               metavar='',
                               help='Counter for verbosity level.',
                               count=True,
                           )] = 0,
):
    """
    Parse ixf ``FILE`` and convert it to a **parquet** ``OUTPUT``.
    """
    if output is None:
        output = Path.cwd()
        filename = file.name.lower().removesuffix('.ixf') + '.parquet'
        output /= filename

    if version is None:
        version = '2.4'

    if batch_size is None:
        batch_size = 1000

    if verbose > 2:
        logger.setLevel(VERBOSE_MAPPING[2])
    else:
        logger.setLevel(VERBOSE_MAPPING[verbose])

    logger.info(f'IXF file: {file}')
    logger.info(f'PARQUET file: {output}')
    logger.info(f'PARQUET version: {version}')
    logger.info(f'Batch size: {batch_size}')

    parser = IXFParser(file)
    parser.to_parquet(output, int(batch_size), str(version))
    raise typer.Exit()


def version_callback(value: bool):
    if value:
        print(f"{__version__}")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
        ctx: typer.Context,
        version: Annotated[Optional[bool],
                           typer.Option(
                               '--version',
                               '-v',
                               help='Show the version of the CLI.',
                               callback=version_callback,
                               is_eager=True,
                           )] = None
):
    """
    A command-line tool (**CLI**) for parsing and converting IXF (IBM DB2
    Import/Export Format) files to various formats such as JSON, CSV, and
    Parquet. Easily parse and convert IXF files to meet your data processing
    needs.
    """
    cli = ctx.info_name
    cmd = ctx.invoked_subcommand

    if cmd is None:
        cmd = 'No command is given'

    logger.info('-------------------------------------------------------------')
    logger.info(f"{cli} is about to execute command: {cmd}")
    logger.info('-------------------------------------------------------------')


if __name__ == '__main__':
    app()
