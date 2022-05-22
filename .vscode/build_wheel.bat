SET ROOT=%cd%

if exist %ROOT%\build RMDIR /S /Q %ROOT%\build
if exist %ROOT%\dist RMDIR /S /Q %ROOT%\dist

python -m pip install --upgrade wheel
python -m pip install --upgrade build
python -m pip install --upgrade twine

python -m build

python -m twine check dist/*