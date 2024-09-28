import os
import shlex
import subprocess
import venv
from pathlib import Path
from typing import List


def run_and_echo(cmd: str | List[str], verbose=True, **kw):
    if isinstance(cmd, str):
        cmd = shlex.split(cmd)
    if verbose:
        print("-->", *cmd)
    return subprocess.run(cmd, **kw)


def test_poetry_i_help(tmp_path: Path) -> None:
    root = Path(__file__).parent.resolve().parent
    dest = tmp_path / root.name
    dest.mkdir()
    os.chdir(dest)
    for name in ("pyproject.toml", "poetry.lock"):
        src, dst = root / name, dest / name
        dst.write_bytes(src.read_bytes())
    run_and_echo("poetry config virtualenvs.in-project true --local")
    venv.create(".venv", symlinks=True, with_pip=True)
    bin_path = dest / ".venv" / "bin"
    if not bin_path.exists():
        bin_path = bin_path.with_name("Scripts")  # Windows
    pip_path = bin_path / "pip"
    run_and_echo(f"{pip_path} install poetry")
    poetry_path = bin_path / "poetry"
    r = run_and_echo(f"{poetry_path} i --help", capture_output=True, verbose=False)
    assert r.returncode != 0
    run_and_echo(f"{pip_path} install -e {root}")
    r = run_and_echo(f"{poetry_path} i --help", capture_output=True, verbose=False)
    assert r.returncode == 0
    r2 = run_and_echo(
        f"{poetry_path} install --help", capture_output=True, verbose=False
    )
    i_help = r.stdout.decode()
    install_help = r2.stdout.decode()
    assert i_help.replace(" i [options]", " install [options]") == install_help
