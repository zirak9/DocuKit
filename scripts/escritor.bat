@echo off
title DocuKit - Escritor
echo ========================================
echo  DocuKit - Documentacion para Escritor
echo  Presentado por DAVOHOMEHOUSE
echo  Tecnologia VALKYRIE FIRE WIND
echo  Hecho por zirak9
echo ========================================
echo.
echo Documentando este proyecto...
echo (Subiendo un nivel desde DocuKit/)
echo.
cd ..
python "%~dp0..\docufy_engine.py"
echo.
echo Los reportes estan en la carpeta 'Reportes/'
pause