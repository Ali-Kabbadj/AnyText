@echo off
cd /d "%~dp0.."

echo Building AnyText executable...

pyinstaller scripts/AnyText.spec

if %errorlevel% neq 0 (
    echo.
    echo Build failed. Press any key to continue...
    pause
    exit /b %errorlevel%
)

echo.
echo Cleaning up build files...

if not exist "release" mkdir "release"

move /Y "dist\AnyText.exe" "release\AnyText.exe"

rmdir /s /q "dist"
rmdir /s /q "build"

echo.
echo Build complete! The executable is in the 'release' folder.
pause