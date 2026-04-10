@echo off
setlocal enabledelayedexpansion

set OUTPUT=1.txt

echo Enter URLs one by one. Type 'done' to finish.
echo.

:loop
set /p URL=Enter URL: 

if /I "%URL%"=="done" goto end

:: Check if file exists
if not exist "%OUTPUT%" (
    echo %URL%>>"%OUTPUT%"
    echo Added: %URL%
    goto loop
)

:: Check for duplicate (case-insensitive)
findstr /I /X "%URL%" "%OUTPUT%" >nul
if %errorlevel%==0 (
    @REM echo Duplicate skipped: %URL%
) else (
    echo %URL%>>"%OUTPUT%"
    @REM echo Added: %URL%
)

goto loop

:end
echo.
@REM echo Done! All unique URLs saved to %OUTPUT%
pause
