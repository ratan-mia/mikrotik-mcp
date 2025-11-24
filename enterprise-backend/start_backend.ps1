$env:PYTHONPATH = "d:\Projects\Mikrtotik\enterprise-backend"
Set-Location "d:\Projects\Mikrtotik\enterprise-backend"
& "d:\Projects\Mikrtotik\.venv\Scripts\python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port 8001
