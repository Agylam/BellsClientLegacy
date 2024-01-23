@echo off
set source_folder=%cd%
python ./python/generate_start.py
REG ADD HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /V "Agylam AutoBells" /t REG_SZ /F /D "%source_folder%\generated\start.bat"
pause