# Deployment

## Frontend on Vercel

Deploy the project root to Vercel. Vercel should only receive the static frontend files. The `.vercelignore` file excludes the Python backend, TensorFlow model, and virtual environment so the deployment stays under Vercel's size limits.

```powershell
npm install -g vercel
vercel login
vercel
```

The Vercel link will show the frontend, but emotion prediction needs a deployed backend URL. After deploying the backend, open the Vercel URL once with:

```text
https://your-vercel-site.vercel.app/?api=https://your-backend-url
```

The page stores that backend URL in local storage and calls:

```text
https://your-backend-url/predict
```

## Backend on Render or Railway

Vercel cannot host this backend because TensorFlow/OpenCV exceed Vercel's 500 MB function storage limit. Deploy the backend as a Python web service on Render or Railway.

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
