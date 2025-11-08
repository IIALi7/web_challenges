import os, pathlib
from flask import Flask, request, send_from_directory, redirect, url_for, render_template, Response

app = Flask(__name__)
os.makedirs("uploads", exist_ok=True)

BASE_DIR = pathlib.Path(__file__).parent.resolve()

@app.route("/")
def index():
    return render_template("index.html")

# ===== File Upload =====
ALLOWED_EXT = {"txt","png","jpg","gif","php"}

@app.route("/upload", methods=["GET","POST"])
def upload():
    if request.method == "POST":
        f = request.files.get("file")
        if not f or f.filename == "":
            return "No file", 400
        ext = f.filename.rsplit(".",1)[-1].lower() if "." in f.filename else ""
        if ext not in ALLOWED_EXT:
            return f"Extension .{ext} not allowed", 400
        save_path = os.path.join("uploads", f.filename)
        f.save(save_path)
        return redirect(url_for("serve_upload", filename=f.filename))
    return '''<!doctype html>
<html><head><meta charset="utf-8"><title>Upload</title></head>
<body>
<h2>Upload a file</h2>
<form method="post" enctype="multipart/form-data">
  <input type="file" name="file">
  <input type="submit" value="Upload">
</form>
<p>Allowed extensions: txt, png, jpg, gif, php</p>
<p>After upload, access at <code>/uploads/filename</code></p>
<p><a href="/">Back</a></p>
</body></html>'''

@app.route("/uploads/<path:filename>")
def serve_upload(filename):
    return send_from_directory("uploads", filename)

# ===== Path Traversal (intentional for challenge) =====
@app.route("/view")
def view():
    rel = request.args.get("file", "")
    if not rel:
        return "Missing ?file=", 400
    target = (BASE_DIR / rel)  # intentionally lax for the challenge
    try:
        data = target.read_bytes()
    except FileNotFoundError as e:
        return f"Error opening file: {e}", 400
    except Exception as e:
        return f"Error: {e}", 400
    try:
        return Response(data.decode("utf-8", errors="ignore"), mimetype="text/plain; charset=utf-8")
    except Exception:
        # if not text, try to send as file
        return send_from_directory(target.parent.as_posix(), target.name)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

