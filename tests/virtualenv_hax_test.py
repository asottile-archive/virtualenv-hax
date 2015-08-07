from __future__ import absolute_import
from __future__ import unicode_literals

import os
import subprocess

import pytest

from virtualenv_hax import main


def assert_valid_virtualenv(path):
    assert os.path.exists(path.strpath)
    assert os.path.exists(path.join('bin/python').strpath)
    assert os.path.exists(path.join('bin/pip').strpath)


def test_simplest_case(tmpdir):
    venv_dir = tmpdir.join('venv')
    main((venv_dir.strpath,))
    assert_valid_virtualenv(venv_dir)


def strategy_python_dash_m(venv1_dir, venv2_dir):
    subprocess.check_call((
        venv1_dir.join('bin/python').strpath, '-m', 'virtualenv_hax',
        '-ppython3.4',
        venv2_dir.strpath,
    ))


def strategy_executable(venv1_dir, venv2_dir):
    subprocess.check_call((
        venv1_dir.join('bin/virtualenv-hax').strpath,
        '-ppython3.4',
        venv2_dir.strpath,
    ))


@pytest.mark.parametrize(
    'strat', (strategy_python_dash_m, strategy_executable)
)
def test_py27_with_future_installed_installing_python3_venv(tmpdir, strat):
    venv1_dir = tmpdir.join('venv27')
    venv2_dir = tmpdir.join('venv')
    subprocess.check_call(('virtualenv', venv1_dir.strpath, '-ppython2.7'))
    # Install the problem package and us
    subprocess.check_call((
        venv1_dir.join('bin/pip').strpath, 'install', 'future', '.',
    ))
    # Attempt to make a virtualenv
    strat(venv1_dir, venv2_dir)
    assert_valid_virtualenv(venv2_dir)
