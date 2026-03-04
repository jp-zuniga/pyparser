set quiet := true

# ---------------------------------------------------------

[private]
default:
    @just --list --list-heading "" --list-prefix ""

# ---------------------------------------------------------

[group("git")]
pre-commit:
    @just fix
    @just fmt
    @just check
    @just test

# ---------------------------------------------------------

[group("uv")]
[private]
run-frozen *cmd:
    uv run --frozen {{ cmd }}

[group("uv")]
shell *args="":
    @just run-frozen "python {{ args }}"

[group("uv")]
sync:
    uv sync --frozen

# ---------------------------------------------------------

[group("uv-ruff")]
fix:
    @just run-frozen "ruff check --fix --unsafe-fixes"

[group("uv-ruff")]
fmt *args="":
    @just run-frozen "ruff format {{ args }}"

[group("uv-ruff")]
lint:
    @just run-frozen "ruff check --unsafe-fixes"
    @just fmt "--check"

[group("uv-ty")]
check *args="":
    @just run-frozen "ty check --no-progress {{ args }}"

[group("uv-test")]
test *args="":
    @just run-frozen "pytest {{ args }}"
