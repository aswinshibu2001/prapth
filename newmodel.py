#take images for comparison from a firebase storage
#comment by Jeevan
import os
import torch
from PIL import Image
import numpy as np
from flask import Flask, render_template, request, jsonify
from facenet_pytorch import MTCNN, InceptionResnetV1, extract_face
import firebase_admin
from firebase_admin import credentials, storage

cred = credentials.Certificate('prapth-dae1d-firebase-adminsdk-mevkq-3803db7a63.json')
firebase_admin.initialize_app(cred)
bucket = storage.bucket('prapth-dae1d.appspot.com')


def prewhiten(x):
    mean = x.mean().item()
    std = x.std().item()
    std_adj = np.clip(std, a_min=1.0/(float(x.numel())**0.5), a_max=None)
    y = (x - mean) / std_adj
    return y



# Load known face embeddings (adjust paths as needed)
mtcnn = MTCNN(keep_all=True, device='cpu')  # Create the MTCNN object
model = InceptionResnetV1(pretrained='vggface2').eval()

known_face_embeddings = []
known_face_filenames = []  # Store filenames for matching

# List files in the Firebase Storage bucket
blobs = bucket.list_blobs()
for blob in blobs:
    try:
        # Extract the file name from the full path
        filename = blob.name.split('/')[-1]

        if filename.endswith((".jpg", ".jpeg")):
            # Download the image from Firebase Storage
            blob.download_to_filename(filename)

            # Process the downloaded image
            try:
                image = Image.open(filename).resize((160, 160))
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                faces = mtcnn(image)
                if faces is not None and len(faces) > 0:
                    face = prewhiten(faces[0])
                    with torch.no_grad():
                        embedding = model(face.unsqueeze(0))[0]
                    known_face_embeddings.append(embedding)
                    known_face_filenames.append(filename)  # Store filename
                else:
                    print(f"No face detected in {filename}")
            except Exception as e:
                print(f"Error processing image {filename}: {e}")
            finally:
                # Remove the downloaded file
                os.remove(filename)
    except Exception as e:
        print(f"Error processing blob {blob.name}: {e}")


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

@app.route('/login.html')
def login():
    return render_template('login.html')





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
        file_name = os.path.split(known_face_filenames[min_index])[-1]
        message = f"Found in Database: {file_name} with distance: {min_distance.item()}"
    else:
        message = "Not Found in Database"

    return jsonify({"message": message})

if __name__ == "__main__":
    app.run(debug=True)
