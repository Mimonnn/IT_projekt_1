# Uruchamiaj w PowerShell z głównego katalogu repozytorium.
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$projectPython = Join-Path $PSScriptRoot '.venv/Scripts/python.exe'
if (-not (Test-Path -LiteralPath $projectPython)) {
    throw 'Brak środowiska .venv. Wykonaj konfigurację opisaną w README.md.'
}
if (-not (Test-Path -LiteralPath (Join-Path $PSScriptRoot '.env'))) {
    throw 'Brak .env. Wykonaj konfigurację opisaną w README.md.'
}
# Ta kopia robocza ma przenośną bazę; na drugim komputerze może działać usługa PostgreSQL.
$localPgCtl = Join-Path $PSScriptRoot 'work/postgres/pgsql/bin/pg_ctl.exe'
$localPgData = Join-Path $PSScriptRoot 'work/pgdata-local'
if ((Test-Path -LiteralPath $localPgCtl) -and (Test-Path -LiteralPath $localPgData)) {
    & $localPgCtl -D $localPgData status | Out-Null
    if ($LASTEXITCODE -ne 0) {
        & $localPgCtl -D $localPgData -l (Join-Path $PSScriptRoot 'work/postgres.log') -w start
        if ($LASTEXITCODE -ne 0) { throw 'Nie udało się uruchomić lokalnego PostgreSQL.' }
    }
}
& $projectPython manage.py check --database default
if ($LASTEXITCODE -ne 0) { throw 'Sprawdź konfigurację aplikacji i bazy w .env.' }
Write-Host 'Strona: http://127.0.0.1:8000/ | Zatrzymanie strony: Ctrl+C'
& $projectPython manage.py runserver 127.0.0.1:8000
