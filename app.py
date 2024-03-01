# take images for comaparison  from a known image folder in the system

import os
import torch
from PIL import Image
import numpy as np
from flask import Flask, render_template, request, jsonify
from facenet_pytorch import MTCNN, InceptionResnetV1, extract_face

#this is command
#this is the second command


def prewhiten(x):
    mean = x.mean().item()
    std = x.std().item()
    std_adj = np.clip(std, a_min=1.0/(float(x.numel())**0.5), a_max=None)
    y = (x - mean) / std_adj
    return y



# Load known face embeddings (adjust paths as needed)
mtcnn = MTCNN(keep_all=True, device='cpu')  # Create the MTCNN object
model = InceptionResnetV1(pretrained='vggface2').eval()

known_face_folder = "known-images"
known_face_paths = [os.path.join(known_face_folder, filename) for filename in os.listdir(known_face_folder) if filename.endswith((".jpg", ".jpeg"))]
known_face_embeddings = []
for path in known_face_paths:
    image = Image.open(path).resize((160, 160))
    if image.mode != 'RGB':
        image = image.convert('RGB')
    faces = mtcnn(image)
    if faces is not None and len(faces) > 0:
        face = prewhiten(faces[0])
        with torch.no_grad():
            embedding = model(face.unsqueeze(0))[0]
        known_face_embeddings.append(embedding)
    else:
        print(f"No face detected in {path}")

# Configure Flask app
# Create Flask app
app = Flask(__name__)


# Set a maximum content length for file uploads (adjust the value as needed)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

# Route for the main page
@app.route("/")
def home():
    return render_template("home.html")

@app.route('/main-menu.html')
def form():
    return render_template('main-menu.html')

@app.route('/home.html')
def home_page():
    return render_template('home.html')

@app.route('/suspect_reporting.html')
def suspect():
    return render_template('suspect_reporting.html')

@app.route("/upload", methods=["POST"])
def upload():
    if "image" not in request.files:
        return jsonify({"message": "No image file selected."})

    image_file = request.files["image"]

    # Validate file size and type
    if image_file.content_length > app.config['MAX_CONTENT_LENGTH']:
        return jsonify({"message": "Image file is too large."})
    if not image_file.mimetype.startswith('image/'):
        return jsonify({"message": "Please select an image file."})

    # Read and preprocess the image
    try:
        image = Image.open(image_file)
        faces = mtcnn(image)
    except Exception as e:
        return jsonify({"message": f"Error processing image: {e}"})

    # Check if a face is detected
    if faces is None or len(faces) == 0:
        return jsonify({"message": "No face detected in the image."})

    # Encode the face
    try:
        face = prewhiten(faces[0])
        with torch.no_grad():
            embedding = model(face.unsqueeze(0))[0]
    except Exception as e:
        return jsonify({"message": f"Error encoding face: {e}"})

    # Compare with known faces
    try:
        distances = [torch.nn.functional.pairwise_distance(embedding, known_embedding) for known_embedding in known_face_embeddings]
        min_distance = min(distances)
    except Exception as e:
        return jsonify({"message": f"Error comparing faces: {e}"})

    # Display the result
    if min_distance < 1.0:  # Adjust this threshold as needed
        min_index = distances.index(min_distance)
        file_name = os.path.split(known_face_paths[min_index])[-1]
        message = f"Found in Database: {file_name} with distance: {min_distance.item()}"
    else:
        message = "Not Found in Database"

    return jsonify({"message": message})

if __name__ == "__main__":
    app.run(debug=True)
