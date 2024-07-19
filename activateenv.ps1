<#
.SYNOPSIS
    Reads variables from a .env file and sets them as environmental variables.

.DESCRIPTION
    Parses each line from a specified .env file to extract key-value pairs and sets them as environmental variables in the process scope.

.NOTES
    Version:        1.2
    Author:         Bill Gates
    Creation Date:  2024-07-14
    Purpose/Change: Set environment variables in process scope for immediate access.

.EXAMPLE
    PS> .\SetEnvVarsFromDotenv.ps1 -FilePath ".\.env"
#>

param (
    [Parameter(Mandatory=$true)]
    [string]$FilePath
)

$envCount = 0
$failCount = 0

try {
    if (-Not (Test-Path $FilePath)) {
        Throw "File not found: $FilePath"
    }

    Get-Content $FilePath | ForEach-Object {
        $keyValue = $_.Split('=', 2)
        if ($keyValue.Count -eq 2) {
            $key = $keyValue[0].Trim()
            $value = $keyValue[1].Trim()
            [System.Environment]::SetEnvironmentVariable($key, $value, [System.EnvironmentVariableTarget]::Process)
            Write-Host "Successfully set [$key] to [$value] in process scope."
            $envCount++
        } else {
            Write-Host "Failed to parse line: $_"
            $failCount++
        }
    }

    Write-Host "Summary: $envCount environment variable(s) set in process scope. $failCount failed to parse."
} catch {
    Write-Error "An error occurred: $_"
}

Get-ChildItem env:
