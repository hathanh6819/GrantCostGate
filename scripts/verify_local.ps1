$ErrorActionPreference = 'Stop'
$env:PYTHONIOENCODING = 'utf-8'
python -m genvm_linter.cli check contracts\grant_cost_gate.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m genvm_linter.cli check contracts\ecfr_source_probe.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q -p no:cacheprovider
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
