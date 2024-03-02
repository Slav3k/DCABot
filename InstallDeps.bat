@echo off
SET TEMP_FILE=perm_check.tmp

:: Attempt to create a temporary file to check write permissions
echo. 2>%TEMP_FILE%
IF ERRORLEVEL 1 (
    echo You do not have the necessary permissions to write to this directory.
    echo Try to run this script with cli with elevated priviledges.
    exit /b 1
)

:: Cleanup - delete the temporary file if it was created successfully
del %TEMP_FILE%

SET VENV_NAME=venv

:: Check for .gitignore and update or create as necessary
IF EXIST .gitignore (
    FINDSTR /C:"%VENV_NAME%/" .gitignore
    IF ERRORLEVEL 1 (
        echo %VENV_NAME%/ >> .gitignore
        echo Added %VENV_NAME% to .gitignore.
    ) ELSE (
        echo %VENV_NAME% is already in .gitignore.
    )
) ELSE (
    echo %VENV_NAME%/ > .gitignore
    echo Created .gitignore and added %VENV_NAME%.
)

:: Check for virtual environment, create if not exists
IF NOT EXIST %VENV_NAME% (
    python -m venv %VENV_NAME%
    echo Virtual environment created.
)

:: Activate virtual environment and install requirements
call %VENV_NAME%\Scripts\activate && pip install -r requirements.txt

echo.
echo To activate the virtual env use: "venv\Scripts\activate"
echo To deactivate the virtual env use: "deactivate"