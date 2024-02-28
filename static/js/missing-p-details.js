
        // Import the functions you need from the SDKs you need
        import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
        import { getFirestore,collection, addDoc  } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";
        import { getStorage, ref, uploadBytes} from "https://www.gstatic.com/firebasejs/10.8.0/firebase-storage.js";

        // Your web app's Firebase configuration
        const firebaseConfig = {
            apiKey: "AIzaSyCzjAdpOcwGcZjTmc8lIu1g5o_bzuIbVyc",
            authDomain: "prapth-dae1d.firebaseapp.com",
            projectId: "prapth-dae1d",
            storageBucket: "prapth-dae1d.appspot.com",
            messagingSenderId: "406083203416",
            appId: "1:406083203416:web:905092c7215732cab8352d",
            measurementId: "G-TZ3NX9RGYM"
        };

        // Initialize Firebase
        const app = initializeApp(firebaseConfig);
        const db = getFirestore(app);
        const storage = getStorage(app);

        document.addEventListener('DOMContentLoaded', function () {
            const form = document.getElementById('missingPersonForm');

            form.addEventListener('submit', function (e) {
                e.preventDefault();

                // addDoc(collection(db, 'missing_persons'), {
                //     name: form.elements.name.value,
                //     age: form.elements.age.value,
                //     address: form.elements.address.value,
                //     place: form.elements.place.value,
                //     days: form.elements.days.value,
                //     email: form.elements.email.value,
                //     contact: form.elements.contact.value,
                //     details: form.elements.details.value,
                //     // photos: form.elements.photos.value,
                //     // You can add more fields as needed
                // })
                // .then(function(docRef) {
                //     console.log("Document written with ID: ", docRef.id);
                //     alert("Successfully added to Firestore!");
                // })
                // .catch(function(error) {
                //     console.error("Error adding document: ", error);
                //     alert("Error adding to Firestore. Please check console for details.");
                // });


                const fileInput = form.elements.photos;
            if (fileInput.files.length > 0) {
                 const file = fileInput.files[0];
                const storageRef = ref(storage,file.name);

                // Upload the file to Firebase Storage
                uploadBytes(storageRef, file)
                    .then((snapshot) => {
                        console.log('File uploaded successfully:', snapshot);
                        // Now you can use snapshot.downloadURL to store the URL in Firestore or perform other actions
                        // For example, you can replace form.elements.photos.value with snapshot.downloadURL in your Firestore document creation.
                    })
                    .catch((error) => {
                        console.error('Error uploading file:', error);
                        alert('Error uploading file to Firebase Storage. Please check console for details.');
                    });  
     }
    else {
                alert('Please select a file before submitting the form.');
            }
        });
            
            });
    
    