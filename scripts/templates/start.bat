@echo off
cd {$WORK_PATH}
git pull
python ./src/main
pause