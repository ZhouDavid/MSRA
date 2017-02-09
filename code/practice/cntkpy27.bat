@echo off
if /I "%CMDCMDLINE%" neq ""%COMSPEC%" " (
    echo.
    echo Please execute this script from inside a regular Windows command prompt.
    echo.
    exit /b 0
)
set PATH=C:\CNTK-2-0-beta10-0-Windows-64bit-CPU-Only\cntk\cntk;%PATH%
"C:\local\Anaconda3-4.1.1-Windows-x86_64\Scripts\activate" "C:\local\Anaconda3-4.1.1-Windows-x86_64\envs\cntk-py27"