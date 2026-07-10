from flask import Flask, render_template, request, url_for
import tensorflow as tf
import numpy as np
from PIL import Image
import os
import base64
from io import BytesIO

app = Flask(__name__)

# Load Model
model = tf.keras.models.load_model("model/mobilenetV2Model.keras")

# Load Class Labels
with open("class_labels.txt", "r") as f:
    class_labels = [line.strip() for line in f.readlines()]

# Bin Mapping
BIN_MAPPING = {
    "battery": {
        "bin": "Red Bin",
        "color": "red",
        "tip": "Dispose batteries at authorized e-waste collection centers."
    },

    "biological": {
        "bin": "Green Bin",
        "color": "green",
        "tip": "Organic waste can be composted."
    },

    "cardboard": {
        "bin": "Blue Bin",
        "color": "blue",
        "tip": "Cardboard is recyclable."
    },

    "clothes": {
        "bin": "Grey Bin",
        "color": "grey",
        "tip": "Donate reusable clothes whenever possible."
    },

    "glass": {
        "bin": "Blue Bin",
        "color": "blue",
        "tip": "Glass can be recycled."
    },

    "metal": {
        "bin": "Blue Bin",
        "color": "blue",
        "tip": "Separate metal waste for recycling."
    },

    "paper": {
        "bin": "Blue Bin",
        "color": "blue",
        "tip": "Paper should be kept dry before recycling."
    },

    "plastic": {
        "bin": "Blue Bin",
        "color": "blue",
        "tip": "Clean plastic before disposal."
    },

    "shoes": {
        "bin": "Grey Bin",
        "color": "grey",
        "tip": "Reuse or donate shoes if possible."
    },

    "trash": {
        "bin": "Grey Bin",
        "color": "grey",
        "tip": "Dispose general waste responsibly."
    }
}

# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Classifier Page
@app.route("/classifier")
def classifier():
    return render_template("classifier.html")

# Prediction Route
@app.route("/predict", methods=["POST"])

def predict():
    
    file = request.files.get("image")

    captured_image = request.form.get("capturedImage")

    # -------------------------
    # Uploaded Image
    # -------------------------
    if file and file.filename != "":

        upload_folder = "static/uploads"

        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        file_path = os.path.join(
            upload_folder,
            file.filename
        )

        file.save(file_path)

        img = Image.open(file_path).convert("RGB")

        image_path = "/" + file_path.replace("\\", "/")

    # -------------------------
    # Camera Image
    # -------------------------
    elif captured_image:

        image_data = captured_image.split(",")[1]

        image_bytes = base64.b64decode(image_data)

        img = Image.open(
            BytesIO(image_bytes)
        ).convert("RGB")

        image_path = captured_image

    else:
        return "No image selected"

    # -------------------------
    # Preprocessing
    # -------------------------

    img = img.resize((224, 224))

    img_array = np.array(img)

    img_array = img_array / 255.0

    img_array = np.expand_dims(img_array, axis=0)

    # -------------------------
    # Prediction
    # -------------------------

    predictions = model.predict(img_array)

    predicted_index = np.argmax(predictions)

    confidence = float(np.max(predictions))

    predicted_class = class_labels[predicted_index]

    result = BIN_MAPPING[predicted_class]

    # Waste Type

    if predicted_class == "biological":
        waste_type = "Organic / Food Waste"

    elif predicted_class == "battery":
        waste_type = "Hazardous Waste"

    elif predicted_class in [
        "plastic",
        "glass",
        "paper",
        "cardboard",
        "metal"
    ]:
        waste_type = "Recyclable Waste"

    else:
        waste_type = "General Waste"

    # Bin Images

    bin_images = {
        "green": "bins/green_bin.png",
        "blue": "bins/blue_bin.png",
        "red": "bins/red_bin.png",
        "grey": "bins/grey_bin.png"
    }

    bin_image = bin_images[result["color"]]

    return render_template(
        "result.html",

        prediction=predicted_class.title(),

        confidence=round(confidence * 100, 2),

        waste_type=waste_type,

        bin_name=result["bin"],

        disposal_tip=result["tip"],

        image_path=image_path,

        bin_image=url_for(
            "static",
            filename=bin_image
        )
    )

if __name__ == "__main__":
    app.run(debug=True)
    