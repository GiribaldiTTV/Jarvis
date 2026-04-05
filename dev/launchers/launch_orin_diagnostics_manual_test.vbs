Set WshShell = CreateObject("WScript.Shell")
WshShell.Run """C:\Users\anden\AppData\Local\Python\pythoncore-3.14-64\pythonw.exe"" ""C:\Jarvis\desktop\orin_diagnostics.pyw"" --manual-test --runtime-log ""C:\Jarvis\dev\logs\diagnostics_ui\Runtime_manual_diagnostics_test.txt""", 0
Set WshShell = Nothing
