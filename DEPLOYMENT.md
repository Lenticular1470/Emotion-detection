# Deployment

## Full App on Vercel

Deploy the project root to Vercel. Vercel uses `src/app.py` as the Flask entrypoint, which imports the app from `src/api.py`.

```powershell
npm install -g vercel
vercel login
vercel
```

Health check URL after deployment:

```text
https://your-vercel-site.vercel.app/health
```

If Vercel fails because the TensorFlow/OpenCV bundle is too large, deploy the backend on Render or Railway with `gunicorn src.api:app` and deploy only the static frontend on Vercel.

## Local Run

```powershell
cd C:\student-project\emotion-detection
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe src\api.py
```

Then open:

```text
http://127.0.0.1:8000/
```
