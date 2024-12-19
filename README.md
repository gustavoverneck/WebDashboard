# WebDashboard



To create a .exe using pyinstaller:
pyinstaller.exe --onefile --add-data "templates:templates" --add-data "static:static" --add-data "src:src" --noconsole --icon=static/icon.ico app.py
