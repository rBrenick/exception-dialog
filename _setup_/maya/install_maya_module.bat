
:: exception_dialog is determined by the current folder name
for %%I in (.) do set exception_dialog=%%~nxI
SET CLEAN_exception_dialog=%exception_dialog:-=_%

:: Check if modules folder exists
if not exist %UserProfile%\Documents\maya\modules mkdir %UserProfile%\Documents\maya\modules

:: Delete .mod file if it already exists
if exist %UserProfile%\Documents\maya\modules\%exception_dialog%.mod del %UserProfile%\Documents\maya\modules\%exception_dialog%.mod

:: Create file with contents in users maya/modules folder
(echo|set /p=+ %exception_dialog% 1.0 %CD%\_setup_\maya & echo; & echo icons: ..\%CLEAN_exception_dialog%\icons)>%UserProfile%\Documents\maya\modules\%exception_dialog%.mod

:: end print
echo .mod file created at %UserProfile%\Documents\maya\modules\%exception_dialog%.mod



