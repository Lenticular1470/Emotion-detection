# Deployment

## Frontend on Vercel

Deploy the project root to Vercel. The `.vercelignore` file keeps the Python backend, virtual environment, and model weights out of the Vercel upload so Vercel only serves the static frontend.

```powershell
npm install -g vercel
vercel login
vercel
```

After your backend is deployed, open the Vercel URL once with the backend URL:

```text
https://your-vercel-site.vercel.app/?api=https://your-backend-url
```

The page stores that backend URL in local storage and will call:

```text
https://your-backend-url/predict
```

## Backend on Render or Railway

Use the same repository for the backend service, but configure the service as a Python web service.

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
gunicorn src.api:app
```

Health check path:

```text
/health
```

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
