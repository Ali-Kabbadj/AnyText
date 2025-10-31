@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0.."

echo.
echo --- Starting Release Process ---
echo.

:: 1. Stage all changes
echo Staging all changes...
git add .

:: Check if there are any changes to commit
git diff --quiet --cached
if %errorlevel% equ 0 (
    echo No changes to commit. Exiting.
    goto end
)

echo.
:: 2. Prompt for a commit message
set /p commit_message="Enter your commit message: "
if not defined commit_message (
    echo Commit message cannot be empty. Aborting.
    goto end
)

:: 3. Commit the changes
echo Committing changes...
git commit -m "%commit_message%"
if %errorlevel% neq 0 (
    echo Git commit failed. Aborting.
    goto end
)

echo.
:: 4. Read, increment, and write the new version
echo Reading and incrementing version...
set version_file=scripts\version.txt
set /p current_version=<%version_file%

for /f "tokens=1,2,3 delims=." %%a in ("!current_version!") do (
    set /a major=%%a
    set /a minor=%%b
    set /a patch=%%c + 1
)

set new_version=!major!.!minor!.!patch!
echo !new_version! > %version_file%
echo New version is: !new_version!

:: 5. Prompt for an optional suffix (handles the hyphen for you)
echo.
set "suffix="
set /p suffix_input="Enter optional tag suffix (e.g., rc1, beta) or press Enter for none: "
if defined suffix_input (
    set "suffix=-!suffix_input!"
)

:: 6. Create the full tag name
set tag=v!new_version!!suffix!
echo Creating tag: !tag!

git tag !tag!
if %errorlevel% neq 0 (
    echo Failed to create git tag. Aborting.
    goto end
)

echo.
:: 7. Push the commit and the new tag
echo Pushing commit and tag to remote...
git push
git push origin !tag!

if %errorlevel% neq 0 (
    echo Failed to push to remote. Please push manually.
    goto end
)

echo.
echo --- Release process complete! ---
echo Successfully pushed commit and tag '!tag!'.
echo GitHub Actions workflow should now be triggered.

:end
echo.
pause