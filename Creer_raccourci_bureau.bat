@echo off
REM Cree un raccourci "The Printing Yassine" sur le Bureau de cet
REM utilisateur, qui pointe vers run.bat (donc vers l'application).
REM A lancer APRES avoir execute INSTALL.bat au moins une fois.

set "ICI=%~dp0"
set "VBS=%TEMP%\raccourci_printing_yassine.vbs"

> "%VBS%" echo Set oWS = WScript.CreateObject("WScript.Shell")
>>"%VBS%" echo sLinkFile = oWS.SpecialFolders("Desktop") ^& "\The Printing Yassine.lnk"
>>"%VBS%" echo Set oLink = oWS.CreateShortcut(sLinkFile)
>>"%VBS%" echo oLink.TargetPath = "%ICI%run.bat"
>>"%VBS%" echo oLink.WorkingDirectory = "%ICI%"
>>"%VBS%" echo oLink.IconLocation = "%ICI%icon.ico"
>>"%VBS%" echo oLink.WindowStyle = 7
>>"%VBS%" echo oLink.Description = "The Printing Yassine - Gestion de stock"
>>"%VBS%" echo oLink.Save

cscript //nologo "%VBS%"
del "%VBS%"

echo.
echo Raccourci "The Printing Yassine" cree sur le Bureau.
pause
