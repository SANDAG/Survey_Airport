set PATH=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312;%PATH%
python -m venv geoplot_survey_airport
call geoplot_survey_airport\Scripts\activate
pip install -r requirements_geoplot.txt
pip list
call geoplot_survey_airport\Scripts\deactivate
pause
