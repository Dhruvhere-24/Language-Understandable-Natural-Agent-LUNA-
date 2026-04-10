@echo off

setlocal

for /f "delims=" %%u in ('call random_pick.bat') do set URL=%%u

echo Playing URL: %URL%
start brave "%URL%"

timeout /t 5 /nobreak >nul
start test.vbs

exit

