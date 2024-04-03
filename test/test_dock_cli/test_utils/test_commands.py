import pytest
from dock_cli.utils.commands import run, getoutput

def test_run_with_valid_args(mock_subprocess_run):
    args = ['echo', 'Hello, World!']
    result = run(args)
    assert result is None
    mock_subprocess_run.assert_called_once_with(args, check=True)

def test_run_with_invalid_args(mock_subprocess_run):
    with pytest.raises(TypeError) as excinfo:
        run('this is a string, not a list')
    assert str(excinfo.value) == 'Expected args to be a list'
    mock_subprocess_run.assert_not_called()

def test_getoutput_with_valid_args(mock_subprocess_run):
    mock_subprocess_run.return_value.stdout = 'Hello, World!'
    args = ['echo', 'Hello, World!']
    result = getoutput(args)
    assert result == 'Hello, World!'
    mock_subprocess_run.assert_called_once_with(args, check=True, capture_output=True, text=True)

def test_getoutput_with_invalid_args(mock_subprocess_run):
    with pytest.raises(TypeError) as excinfo:
        getoutput('this is a string, not a list')
    assert str(excinfo.value) == 'Expected args to be a list'
    mock_subprocess_run.assert_not_called()
