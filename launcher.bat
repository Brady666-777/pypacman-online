@echo off
:start
cls
echo PyPacman Multiplayer Launcher
echo =============================
echo.
echo 1. Start Multiplayer Client (Host/Join Game)
echo 2. Start Dedicated Server
echo 3. Run Original Single Player Game
echo 4. Test Multiplayer Functionality
echo 5. Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto client
if "%choice%"=="2" goto server
if "%choice%"=="3" goto singleplayer
if "%choice%"=="4" goto test
if "%choice%"=="5" goto exit

:client
echo Starting Multiplayer Client...
python main_multiplayer.py
goto menu

:server
echo Starting Dedicated Server...
python server/main_server.py
goto menu

:singleplayer
echo Starting Original Single Player Game...
python main.py
goto menu

:test
echo Running Multiplayer Tests...
python test_multiplayer.py
pause
goto menu

:menu
echo.
echo Press any key to return to menu...
pause >nul
cls
goto start

:exit
echo Goodbye!
pause
