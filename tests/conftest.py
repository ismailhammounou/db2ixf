# coding: utf-8
"""Conftest pytest module, see pytest doc"""
import shutil
from pathlib import Path
from pytest import fixture


@fixture(scope="function")
def test_output_dir(request, pytestconfig):
    """
    Fixture that creates an output directory for each test.

    The output directory is created in the `target/test` directory
    with the name of the test function.

    Parameters
    ----------
    request : pytest.FixtureRequest
        The pytest request object.
    pytestconfig : _pytest.config.Config
        The pytest configuration object.

    Yields
    ------
    pathlib.Path
        The path to the created output directory.
    """

    # Get the name of the test function
    test_name = request.node.name

    # Handling unsupported naming by other tools/packages
    test_name = test_name.replace("[", "-").replace("]", "").strip()

    # Get the root directory of the project
    root_dir = Path(pytestconfig.rootpath)

    # Create the output directory path
    output_dir = root_dir / "target" / "test" / test_name

    # Create the output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Provide the output directory path as the fixture value
    yield output_dir

    # Clean up the output directory after the test completes
    # shutil.rmtree(output_dir)


@fixture(scope="session")
def test_delete_test_dir(pytestconfig):
    """Fixture to delete test directory at the beginning of a test session.

    Parameters
    ----------
    pytestconfig : _pytest.config.Config
        The pytest configuration object.
    """
    # Get the root directory of the project
    root_dir = Path(pytestconfig.rootpath)

    output_dir = root_dir / "target" / "test"

    shutil.rmtree(output_dir)
