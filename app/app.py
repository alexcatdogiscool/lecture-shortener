from flask import Flask, request, render_template, redirect, send_file, make_response
import os



app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        resp = make_response(render_template("base.html"))
        resp.set_cookie('user_id', '1234')
        return resp
    
    elif request.method == "POST":
        if 'file' not in request.files:
            return render_template("base.html")
        file = request.files['file']
        if file.filename == '':
            return render_template("base.html")
        if file:
            #do file saving stuff
            id = request.cookies.get('user_id')
            resp = make_response(redirect('/uploaded'))
            resp.set_cookie('user_id', id)
            return resp
            
            
        return render_template("base.html")


@app.route('/uploaded')
def uploaded():
    id = request.cookies.get("id")
    return render_template('uploaded.html', user_id=id)

@app.route("/download")
def download():
    id = request.cookies.get("user_id")
    vid_path = os.path.join('output', f'{id}.mp4')
    print(id, vid_path)
    return send_file(vid_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0")