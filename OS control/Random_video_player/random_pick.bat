@echo off
setlocal enabledelayedexpansion

set FILE=1.txt

:: Count total lines
set COUNT=0
for /f "usebackq delims=" %%a in ("%FILE%") do (
    set /a COUNT+=1
)

:: Random line number
set /a PICK=(%RANDOM% %% %COUNT%) + 1

:: Fetch that line
set LINE=0
for /f "usebackq delims=" %%a in ("%FILE%") do (
    set /a LINE+=1
    if !LINE! equ %PICK% (
        echo %%a
        exit /b
    )
)
