from flask import Flask, jsonify
import os
import argparse
import datetime
import io
import torch
from PIL import Image
from flask import Flask, render_template, request, redirect

app = Flask(_name_)

DATETIME_FORMAT = "%Y-%m-%d_%H-%M-%S-%f"
model = None

@app.route("/", methods=["GET", "POST"])
def home():
    global model
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        if not file:
            return

        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))
        results = model([img])

        results.render()
        now_time = datetime.datetime.now().strftime(DATETIME_FORMAT)
        img_savename = f"static/{now_time}.png"
        Image.fromarray(results.ims[0]).save(img_savename)
        return redirect(img_savename)

    return render_template("index.html")

@app.route('/detection', methods=["POST"])
def predict():
    global model
    if not request.method == "POST":
        return

    if request.files.get("image"):
        image_file = request.files["image"]
        image_bytes = image_file.read()
        img = Image.open(io.BytesIO(image_bytes))
        results = model(img, size=640)

        results.render()
        now_time = datetime.datetime.now().strftime(DATETIME_FORMAT)
        img_savename = f"static/{now_time}.png"
        Image.fromarray(results.ims[0]).save(img_savename)
        gambar = {'image': img_savename}

        hasil = results.pandas().xyxy[0].to_dict(orient='records')
        hasil.insert(0, gambar)
        return hasil

if _name_ == "_main_":
    parser = argparse.ArgumentParser(description="Flask app exposing yolov5 models")
    parser.add_argument("--port", default=5000, type=int, help="port number")
    args = parser.parse_args()
    model = torch.hub.load('yolov5', 'custom', path='model.pt', source='local')

    model.eval()
    app.run(port=args.port)