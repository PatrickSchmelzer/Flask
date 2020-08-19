@echo on
CALL .\env\Scripts\activate
set FLASH_APP=app.py
set FLASH_ENV=development
flask run

pause