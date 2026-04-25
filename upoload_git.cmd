@echo off
cd /d %~dp0

set msg=update %date% %time%

git add .

git diff --cached --quiet
if %errorlevel%==0 (
    echo Нет изменений
) else (
    git commit -m "%msg%"
    git push
)

pause
