# originally created model
#some comments
import cv2
import torch
import numpy as np
from facenet_pytorch import MTCNN, InceptionResnetV1, extract_face
from PIL import Image
from tkinter import filedialog
from tkinter import Tk

# Define the modified prewhiten function
def prewhiten(x):
    mean = x.mean().item()
    std = x.std().item()
    std_adj = np.clip(std, a_min=1.0/(float(x.numel())**0.5), a_max=None)
    y = (x - mean) / std_adj
    return y

# Initialize MTCNN for face detection
mtcnn = MTCNN(keep_all=True, device='cpu')

# Initialize Inception Resnet V1 for face recognition
model = InceptionResnetV1(pretrained='vggface2').eval()

# Load images of known people
image_of_person1 = Image.open("images\\aswin.jpg")  # Replace with the actual path
image_of_person2 = Image.open("images\\jithin.jpg")  # Replace with the actual path
image_of_person3 = Image.open("images\\jeevan.jpg")
image_of_person4 = Image.open("images\\jis.jpg")


# Preprocess images
person1_faces = mtcnn(image_of_person1)
person2_faces = mtcnn(image_of_person2)
person3_faces = mtcnn(image_of_person3)
person4_faces = mtcnn(image_of_person4)

# Encode faces
if person1_faces is not None and len(person1_faces) > 0:
    person1_face = prewhiten(person1_faces[0])
    with torch.no_grad():
        person1_embedding = model(person1_face.unsqueeze(0))[0]
else:
    print("No face detected in image_of_person1")

if person2_faces is not None and len(person2_faces) > 0:
    person2_face = prewhiten(person2_faces[0])
    with torch.no_grad():
        person2_embedding = model(person2_face.unsqueeze(0))[0]
else:
    print("No face detected in image_of_person2")

if person3_faces is not None and len(person3_faces) > 0:
    person3_face = prewhiten(person3_faces[0])
    with torch.no_grad():
        person3_embedding = model(person3_face.unsqueeze(0))[0]
else:
    print("No face detected in image_of_person3")

if person4_faces is not None and len(person4_faces) > 0:
    person4_face = prewhiten(person4_faces[0])
    with torch.no_grad():
        person4_embedding = model(person4_face.unsqueeze(0))[0]
else:
    print("No face detected in image_of_person4")

# Rest of the code remains unchanged

known_face_embeddings = [person1_embedding, person2_embedding, person3_embedding, person4_embedding]
known_face_names = ["aswin.jpg", "jithin.jpg", "jeevan.jpg", "jis.jpg"]

# Choose a file using a file dialog
Tk().withdraw()  # Close the root window
file_path = filedialog.askopenfilename(title="Select an image file", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])

if file_path:
    # Load the chosen image
    # ... (previous code)

    # Load the chosen image
    image_to_check = Image.open(file_path)

    # Perform face detection
    faces_to_check = mtcnn(image_to_check)

    # Check if a face is detected in the chosen image
    if faces_to_check is not None and len(faces_to_check) > 0:
        # Encode the face
        face_to_check = prewhiten(faces_to_check[0])

        with torch.no_grad():
            embedding_to_check = model(face_to_check.unsqueeze(0))[0]

        # Compare with known faces
        distances = [torch.nn.functional.pairwise_distance(embedding_to_check, known_embedding) for known_embedding in known_face_embeddings]
        min_distance = min(distances)

        # Display the result
        if min_distance < 1.0:  # Adjust this threshold as needed
            min_index = distances.index(min_distance)
            file_name = known_face_names[min_index]
            print(f"Found in Database: {file_name} with distance: {min_distance.item()}")
        else:
            print("Not Found in Database")

        # Optionally, you can display the chosen image with the result
        # cv2.imshow('Chosen Image with Result', cv2.cvtColor(np.array(image_to_check), cv2.COLOR_RGB2BGR))
        cv2.waitKey(0)
        cv2.destroyAllWindows()

else:
    print("No face detected in the chosen image.")
