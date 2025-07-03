
@echo off
ECHO Starting Competitor Hiring Analysis Setup...

:: Navigate to project directory
cd /d D:\compititor_hiring_analysis
IF %ERRORLEVEL% NEQ 0 (
    ECHO Error: Could not navigate to D:\compititor_hiring_analysis
    pause
    exit /b %ERRORLEVEL%
)

:: Activate virtual environment
IF EXIST venv (
    CALL venv\Scripts\activate
    IF %ERRORLEVEL% NEQ 0 (
        ECHO Error: Failed to activate virtual environment
        pause
        exit /b %ERRORLEVEL%
    )
) ELSE (
    ECHO Creating virtual environment...
    python -m venv venv
    CALL venv\Scripts\activate
    IF %ERRORLEVEL% NEQ 0 (
        ECHO Error: Failed to create or activate virtual environment
        pause
        exit /b %ERRORLEVEL%
    )
)

:: Install dependencies
ECHO Installing dependencies from requirements.txt...
pip install -r src\requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    ECHO Error: Failed to install dependencies
    pause
    exit /b %ERRORLEVEL%
)

:: Install Jupyter and IPython for notebook execution
ECHO Installing Jupyter and IPython...
pip install jupyter ipython
IF %ERRORLEVEL% NEQ 0 (
    ECHO Error: Failed to install Jupyter or IPython
    pause
    exit /b %ERRORLEVEL%
)

:: Install spaCy model
ECHO Installing spaCy model en_core_web_sm...
python -m spacy download en_core_web_sm
IF %ERRORLEVEL% NEQ 0 (
    ECHO Error: Failed to install spaCy model
    pause
    exit /b %ERRORLEVEL%
)

:: Run the notebook to generate output CSVs
ECHO Running competitor_hiring_analysis.ipynb...
jupyter nbconvert --to notebook --execute src\competitor_hiring_analysis.ipynb --output-dir src
IF %ERRORLEVEL% NEQ 0 (
    ECHO Error: Failed to run Jupyter notebook
    pause
    exit /b %ERRORLEVEL%
)

:: Run Streamlit dashboard
ECHO Starting Streamlit dashboard...
streamlit run src\app.py
IF %ERRORLEVEL% NEQ 0 (
    ECHO Error: Failed to start Streamlit dashboard
    pause
    exit /b %ERRORLEVEL%
)

ECHO Setup complete! Streamlit dashboard should be running at http://localhost:8501
pause
