# Web Vulnerable Mini Lab (for teaching)
Contains 4 mini vulnerable demos:
1. Path Traversal -> /view?file=../../etc_passwd.txt
2. SQL Injection -> /user?id=1 OR 1=1
3. File Upload (malicious file simulation) -> /upload (uploads accessible at /uploads/<name>)
4. Brute Force / Directory Enumeration -> hidden files under files/hidden/ (not linked)

## Setup (local)
1. Create Python venv:
   python -m venv venv
   source venv/bin/activate   (on Windows use venv\Scripts\activate)

2. Install:
   pip install -r requirements.txt

3. Initialize DB:
   python init_db.py

4. Run:
   python app.py
   Open http://127.0.0.1:5000

## Notes for hosting (Render.com recommended)
Render supports Python web services easily:
1. Create a new Web Service on Render:
   - Connect your GitHub repo (or upload code).
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`  (Render provides gunicorn)
   - Port: Render sets PORT automatically.

2. Make sure `users.db` is created on first startup (you can run `python init_db.py` in a deploy hook or add code that creates if missing).

## Quick GitHub → Render deployment (recommended)
1. Create a new GitHub repository and push this project to it:
   git init
   git add .
   git commit -m "mini web vuln lab for teaching"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main

2. In Render:
   - New → Web Service → Connect GitHub repo.
   - Region: pick nearest.
   - Branch: main
   - Build Command: pip install -r requirements.txt
   - Start Command: gunicorn app:app

3. After deploy, Render runs the app and users.db will be created automatically on first boot.
