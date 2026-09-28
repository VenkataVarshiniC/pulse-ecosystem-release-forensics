param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('init', 'start', 'stop', 'create', 'migrate', 'reset', 'status')]
    [string]$Action,
    [ValidateSet('pulse_dev', 'pulse_test')]
    [string]$Database = 'pulse_dev'
)

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$envPath = Join-Path $repoRoot '.env'
$localRoot = Join-Path $repoRoot '.local\postgres'
$dataPath = Join-Path $localRoot 'data'
$logPath = Join-Path $localRoot 'server.log'
$pgBin = if ($env:PULSE_PG_BIN) { $env:PULSE_PG_BIN } else { 'C:\Program Files\PostgreSQL\16\bin' }
$pgConfig = Join-Path $pgBin 'pg_config.exe'
if (-not (Test-Path -LiteralPath $pgConfig)) {
    throw "PostgreSQL tools are missing at $pgBin. Install PostgreSQL 16.14 or set PULSE_PG_BIN."
}
$installedVersion = (& $pgConfig --version)
if ($LASTEXITCODE -ne 0 -or $installedVersion -ne 'PostgreSQL 16.14') {
    throw "Expected PostgreSQL 16.14; found $installedVersion. Change the pin through a documented migration."
}

function Invoke-Pg([string]$tool, [string[]]$arguments) {
    & (Join-Path $pgBin $tool) @arguments
    if ($LASTEXITCODE -ne 0) { throw "$tool failed with exit code $LASTEXITCODE" }
}

function Read-LocalEnvironment {
    if (-not (Test-Path -LiteralPath $envPath)) {
        throw "Missing ignored root .env. Run db.ps1 -Action init."
    }
    foreach ($line in Get-Content -LiteralPath $envPath) {
        if ($line -match '^([A-Z_]+)=(.*)$') {
            [Environment]::SetEnvironmentVariable($Matches[1], $Matches[2], 'Process')
        }
    }
    if ($env:PGHOST -ne '127.0.0.1' -or $env:PGPORT -ne '55432' -or $env:PGUSER -ne 'pulse_local' -or -not $env:PGPASSWORD) {
        throw 'Local database configuration is incomplete or not loopback-only.'
    }
    $env:PGDATABASE = $Database
}

function Ensure-Database {
    Assert-LocalCluster
    $exists = & (Join-Path $pgBin 'psql.exe') -X -w -At -d postgres -c "SELECT 1 FROM pg_database WHERE datname = '$Database'"
    if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect local PostgreSQL databases.' }
    if ($exists -ne '1') { Invoke-Pg 'createdb.exe' @('-w', $Database) }
}

function Assert-LocalCluster {
    if (-not (Test-Path -LiteralPath (Join-Path $dataPath 'PG_VERSION'))) {
        throw 'Isolated local cluster is absent. Run db.ps1 -Action init.'
    }
    & (Join-Path $pgBin 'pg_ctl.exe') -D $dataPath status *> $null
    if ($LASTEXITCODE -ne 0) {
        throw 'Isolated local cluster is not running. Run db.ps1 -Action start.'
    }
}

function Apply-Migrations {
    Ensure-Database
    $revisionTable = & (Join-Path $pgBin 'psql.exe') -X -w -At -d $Database -c "SELECT to_regclass('public.schema_migrations') IS NOT NULL"
    if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect migration state.' }
    $applied = @()
    if ($revisionTable -eq 't') {
        $applied = @(& (Join-Path $pgBin 'psql.exe') -X -w -At -d $Database -c 'SELECT version FROM public.schema_migrations ORDER BY version')
        if ($LASTEXITCODE -ne 0) { throw 'Cannot read migration state.' }
    }
    $migrations = @(Get-ChildItem -LiteralPath (Join-Path $PSScriptRoot 'migrations') -Filter 'V*__*.sql' | Sort-Object Name)
    foreach ($migration in $migrations) {
        if ($migration.Name -notmatch '^V([0-9]+)__') { throw 'Invalid migration name.' }
        $version = [int]$Matches[1]
        if ($applied -contains "$version") { continue }
        Invoke-Pg 'psql.exe' @('-X', '-w', '-v', 'ON_ERROR_STOP=1', '-d', $Database, '-f', $migration.FullName)
        $applied += "$version"
    }
    Write-Output "Database $Database at migration $($applied -join ',')."
}

if ($Action -eq 'init') {
    if (-not (Test-Path -LiteralPath $envPath)) {
        $bytes = [System.Security.Cryptography.RandomNumberGenerator]::GetBytes(32)
        $secret = [Convert]::ToHexString($bytes).ToLowerInvariant()
        $lines = @('PGHOST=127.0.0.1', 'PGPORT=55432', 'PGDATABASE=pulse_dev', 'PGUSER=pulse_local', "PGPASSWORD=$secret")
        [System.IO.File]::WriteAllLines($envPath, $lines)
    }
    Read-LocalEnvironment
    if (Test-Path -LiteralPath (Join-Path $dataPath 'PG_VERSION')) {
        throw 'Local cluster already initialized; refusing to overwrite it.'
    }
    New-Item -ItemType Directory -Force -Path $localRoot | Out-Null
    $pwPath = Join-Path $localRoot 'initdb-password.tmp'
    try {
        [System.IO.File]::WriteAllText($pwPath, $env:PGPASSWORD)
        Invoke-Pg 'initdb.exe' @('-D', $dataPath, '--username=pulse_local', "--pwfile=$pwPath", '--auth-host=scram-sha-256', '--auth-local=scram-sha-256', '--encoding=UTF8', '--no-instructions')
    }
    finally {
        if (Test-Path -LiteralPath $pwPath) { Remove-Item -LiteralPath $pwPath }
    }
    Write-Output 'Initialized isolated local cluster; credentials remain in ignored .env.'
    exit
}

Read-LocalEnvironment
switch ($Action) {
    'start' {
        Invoke-Pg 'pg_ctl.exe' @('-D', $dataPath, '-l', $logPath, '-o', '-h 127.0.0.1 -p 55432', '-w', 'start')
    }
    'stop' {
        Invoke-Pg 'pg_ctl.exe' @('-D', $dataPath, '-m', 'fast', '-w', 'stop')
    }
    'status' {
        Invoke-Pg 'pg_isready.exe' @('-h', '127.0.0.1', '-p', '55432')
    }
    'create' { Ensure-Database }
    'migrate' { Apply-Migrations }
    'reset' {
        Assert-LocalCluster
        Invoke-Pg 'dropdb.exe' @('-w', '--if-exists', '--force', $Database)
        Invoke-Pg 'createdb.exe' @('-w', $Database)
        Apply-Migrations
    }
}
