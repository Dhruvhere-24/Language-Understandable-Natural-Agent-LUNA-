@REM this file is just update a specific file each and only one time when windows start
@echo off
setlocal enabledelayedexpansion

:: ==== CONFIG ====
set REPO_PATH=D:\Github\my-repo
set README=%REPO_PATH%\README.md
set MOTIVATE=%REPO_PATH%\motivate.txt
set LASTRUN=%REPO_PATH%\last_run.txt

cd /d %REPO_PATH%

:: ==== DATE CHECK ====
for /f %%a in ('powershell -command "Get-Date -Format yyyy-MM-dd"') do set TODAY=%%a

if exist %LASTRUN% (
    set /p LAST=<%LASTRUN%
    if "!LAST!"=="!TODAY!" exit
)

:: ==== PICK RANDOM LINE ====
for /f %%a in ('powershell -command "Get-Content '%MOTIVATE%' | Get-Random"') do set LINE=%%a

:: ==== UPDATE README ====
powershell -command ^
"(Get-Content '%README%') -replace 'Motivation: <AUTO>', 'Motivation: !LINE!' | Set-Content '%README%'"

:: ==== GIT PUSH ====
git add README.md
git commit -m "auto update"
git push

:: ==== SAVE DATE ====
echo %TODAY% > %LASTRUN%

exit