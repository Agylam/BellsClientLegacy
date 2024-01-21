@echo off
set source_folder=%cd%
REG ADD HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /V "Agylam AutoBells" /t REG_SZ /F /D "%source_folder%\start.bat"