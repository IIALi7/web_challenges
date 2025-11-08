import pathlib, os
from flask import Flask, request, Response, render_template

app = Flask(__name__)
BASE_DIR = pathlib.Path(__file__).parent.resolve()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/view')
def view():
    rel = request.args.get('file','').strip()
    if not rel:
        return "Missing ?file=", 400
    # intentionally lax for the challenge — resolves relative to project root
    target = (BASE_DIR / rel)
    try:
        data = target.read_bytes()
    except FileNotFoundError as e:
        return f"Error opening file: {e}", 400
    except Exception as e:
        return f"Error: {e}", 400
    # return as plain text so flags show clearly
    return Response(data.decode('utf-8', errors='ignore'), mimetype='text/plain; charset=utf-8')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
