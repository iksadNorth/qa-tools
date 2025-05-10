# Python 설치
$pythonVersion = "3.12.3"
$pythonInstaller = "python-$pythonVersion-amd64.exe"
$pythonUrl = "https://www.python.org/ftp/python/$pythonVersion/$pythonInstaller"

if (-Not (Test-Path $pythonInstaller)) {
    Write-Host "Downloading Python $pythonVersion..."
    Invoke-WebRequest -Uri $pythonUrl -OutFile $pythonInstaller
}

Start-Process -FilePath ".\$pythonInstaller" -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1 Include_test=0" -Wait

# uv 설치
Write-Host "Installing uv..."
Invoke-Expression (Invoke-WebRequest https://astral.sh/uv/install.ps1).Content

# 경로 확인
Write-Host "`nPython version:"
python --version

Write-Host "`nuv version:"
uv --version
