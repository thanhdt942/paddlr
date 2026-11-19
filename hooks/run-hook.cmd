:; # Unix shell interpreter
:; SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
:; if command -v python3 >/dev/null 2>&1; then
:;   exec python3 "$SCRIPT_DIR/$1.py" "${@:2}"
:; else
:;   exec python "$SCRIPT_DIR/$1.py" "${@:2}"
:; fi
@echo off
set SCRIPT_DIR=%~dp0
python "%SCRIPT_DIR%%1.py" %2 %3 %4 %5 %6 %7 %8 %9
