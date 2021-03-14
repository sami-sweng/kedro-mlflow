import shutil

import mlflow
import pytest
from cookiecutter.main import cookiecutter
from kedro import __version__ as kedro_version
from kedro.framework.cli.cli import TEMPLATE_PATH

from kedro_mlflow.framework.cli.cli import TEMPLATE_FOLDER_PATH
from kedro_mlflow.framework.cli.cli_utils import write_jinja_template


@pytest.fixture(autouse=True)
def cleanup_mlflow_after_runs():
    # A test function will be run at this point
    yield
    while mlflow.active_run():
        mlflow.end_run()


@pytest.fixture
def kedro_project(tmp_path):
    # TODO : this is also an integration test since this depends from the kedro version
    config = {
        "output_dir": tmp_path,
        "kedro_version": kedro_version,
        "project_name": "This is a fake project",
        "repo_name": "fake-project",
        "python_package": "fake_project",
        "include_example": True,
    }

    cookiecutter(
        str(TEMPLATE_PATH),
        output_dir=config["output_dir"],
        no_input=True,
        extra_context=config,
    )

    shutil.rmtree(
        tmp_path / "fake-project" / "src" / "tests"
    )  # avoid conflicts with pytest

    return tmp_path / "fake-project"


@pytest.fixture
def kedro_project_with_mlflow_conf(tmp_path, kedro_project):
    write_jinja_template(
        src=TEMPLATE_FOLDER_PATH / "mlflow.yml",
        is_cookiecutter=False,
        dst=tmp_path / "fake-project" / "conf" / "local" / "mlflow.yml",
        python_package="fake_project",
    )

    return tmp_path / "fake-project"
