from flask import Flask, request, render_template
import os
from werkzeug.utils import secure_filename

FILE_PATH = "uploaded"

app = Flask(__name__)

app.config['FILE_PATH'] = FILE_PATH

if not os.path.exists(app.config['FILE_PATH']):
    os.mkdir(app.config['FILE_PATH'])

def process_video(filename):
    os.system(f"python3 poc.py 5 true {filename}")
    return "Done"

@app.route("/", methods=["GET", "POST"])
def hello():
    if request.method == "GET":
        return render_template("base.html")
    
    elif request.method == "POST":
        if 'file' not in request.files:
            return render_template("base.html")
        file = request.files['file']
        if file.filename == '':
            return render_template("base.html")
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['FILE_PATH'], filename))
            print(process_video(filename))
            return render_template("uploaded.html")
        return render_template("base.html")





if __name__ == "__main__":
    app.run()