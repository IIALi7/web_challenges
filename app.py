import os
from flask import Flask, request, render_template, redirect, url_for, send_from_directory, abort
import sqlite3, os, pathlib

BASE_DIR = pathlib.Path(__file__).parent.resolve()
FILES_DIR = BASE_DIR / "files"
UPLOADS_DIR = BASE_DIR / "uploads"
DB_PATH = BASE_DIR / "users.db"

app = Flask(__name__)
os.makedirs('uploads', exist_ok=True)
app.secret_key = 'ctf_insecure_secret'
app.config['UPLOAD_FOLDER'] = str(UPLOADS_DIR)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB

# --- Ensure sample DB exists on startup ---
def ensure_db():
    import sqlite3
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, username TEXT);")
        cur.executemany("INSERT INTO users(id, username) VALUES (?, ?);", [(1,'admin'),(2,'ali'),(3,'mohammed')])
        conn.commit()
        conn.close()
        print("Created users.db")
    else:
        print("users.db already exists")

# Call ensure_db on import/startup (safe for simple hosting)
ensure_db()

# --- Home ---
@app.route("/")
def index():
    return render_template("index.html")

# --- Path traversal (intentionally vulnerable for teaching) ---
@app.route("/view")
def view_file():
    fname = request.args.get("file", "gift.png")
    # INTENTIONAL: vulnerable naive join (for demo only)
    target = os.path.join(str(FILES_DIR), fname)
    try:
        with open(target, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        return render_template("file_view.html", filename=fname, content=content)
    except Exception as e:
        return f"Error opening file: {e}", 400

# --- SQLi demo (intentionally vulnerable) ---
def query_db_raw(q):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute(q)
        rows = cur.fetchall()
    finally:
        conn.close()
    return rows

@app.route("/user")
def user():
    user_id = request.args.get("id","1")
    # INTENTIONAL: vulnerable query building
    q = f"SELECT id, username FROM users WHERE id = {user_id};"
    try:
        rows = query_db_raw(q)
    except Exception as e:
        return f"SQL Error: {e}<br>Query: {q}", 500
    return render_template("users.html", query=q, rows=rows)

# --- File upload demo ---
ALLOWED_EXT = ["txt","png","jpg","gif","php"]
def allowed(filename):
    return "." in filename and filename.rsplit(".",1)[1].lower() in ALLOWED_EXT

@app.route("/upload", methods=["GET","POST"])
def upload():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part", 400
        f = request.files["file"]
        if f.filename == "":
            return "No selected file", 400
        if not allowed(f.filename):
            return "File type not allowed", 400
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        f.save(save_path)
        return redirect(url_for('uploaded_file', filename=f.filename))
    return render_template("upload.html")

@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    # If a "php" file is accessed we SIMULATE execution for demo (do NOT execute real commands)
    full = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(full):
        abort(404)
    if filename.endswith(".php"):
        cmd = request.args.get("cmd","whoami")
        # Simulated output to demonstrate risk (do NOT run commands in demo)
        simulated = f"Simulated execution output for cmd='{cmd}':\\nwww-data"
        return f"<pre>{simulated}</pre>"
    # Otherwise, serve file content
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# --- Brute-force / Directory enumeration demo ---
# Hidden file not linked anywhere: /hidden/secret_note.txt
@app.route("/hidden/<path:name>")
def hidden(name):
    # simply attempt to serve from files/hidden
    hidden_dir = FILES_DIR / "hidden"
    full = hidden_dir / name
    if full.exists():
        return send_from_directory(str(hidden_dir), name)
    abort(404)



# === CTF challenge routes ===
from flask import session, flash

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = request.form.get("username","")
        pw = request.form.get("password","")
        if (user == "admin" and pw == "admin123") or (user == "guest" and pw == "guest"):
            session['authed'] = True
            return redirect(url_for("secret"))
        else:
            return "Login failed", 401
    return '''
      <h2>Login (CTF challenge)</h2>
      <form method="post">
        <input name="username" placeholder="username"><br>
        <input name="password" placeholder="password"><br>
        <input type="submit" value="Login">
      </form>
    '''

@app.route("/secret")
def secret():
    if not session.get('authed'):
        return redirect(url_for('login'))
    return "<h2>Secret area</h2><p>Flag: CSC{BRUTE_FORCE_FLAG_4}</p>"

@app.route("/challenge/path")
def challenge_path():
    return '<p>Try: /view?file=../../files/flags/flag_path.txt</p>'

@app.route("/challenge/sqli")
def challenge_sqli():
    return '<p>Try: /user?id=1 OR 1=1<br>Union example: /user?id=1 UNION SELECT 1,flag FROM flags-- </p>'

@app.route("/challenge/upload")
def challenge_upload():
    return '<p>Upload a file at /upload (e.g. myflag.txt) then access /uploads/myflag.txt</p>'

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

