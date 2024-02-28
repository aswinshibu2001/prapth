// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, fetchSignInMethodsForEmail, signOut } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";
import { getDatabase,  ref, update } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-database.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-analytics.js";
import {  getFirestore,collection, doc, setDoc as setFirestore, getDoc } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";

        // Your web app's Firebase configuration
        // For Firebase JS SDK v7.20.0 and later, measurementId is optional
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
        const analytics = getAnalytics(app);
        const firestore = getFirestore(app);
        const database = getDatabase(app);
        const auth = getAuth();

        const signupForm = document.getElementById('signup-form');
        const signinForm = document.getElementById('signin-form');

        signupForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            var email = document.getElementById('email').value;
            var password = document.getElementById('password').value;
            var username = document.getElementById('name').value;

            try {
                const methods = await fetchSignInMethodsForEmail(auth, email);
        
                if (methods.length > 0) {
                    // Email already exists
                    alert('Email is already in use. Please use a different email.');
                } else {
                    // Proceed with the sign-up
                    const userCredential = await createUserWithEmailAndPassword(auth, email, password);
                    const user = userCredential.user;
        
                    // Check if the username already exists in Firestore
                    const userDocRef = doc(collection(firestore, 'users'), username);
                    const docSnapshot = await getDoc(userDocRef);
        
                    if (docSnapshot.exists()) {
                        // Username already exists
                        alert('Username is already in use. Please choose a different username.');
                    } else {
                        // Username is available, store data in Firestore
                        await setFirestore(userDocRef, {
                            username: username,
                            email: email,
                        });
        
                        alert('User Created');
                    }
                }
            } catch (error) {
                console.error('Error checking email existence:', error);
                alert('Error during sign-up. Please try again.');
            }
        });

        signinForm.addEventListener('submit', (e) => {
            e.preventDefault();

            var email = document.getElementById('signin-email').value;
            var password = document.getElementById('signin-password').value;

            signInWithEmailAndPassword(auth, email, password)
                .then((userCredential) => {
                    const user = userCredential.user;

                    const dt = new Date();

                    update(ref(database, 'users/' + user.uid), {
                        last_login: dt,
                    });

                    alert('User Logged In');
                    // const usernamePlaceholder = document.getElementById('username-placeholder');

                    // // Set the content of the span to the username
                    // usernamePlaceholder.textContent = `Welcome, ${user.displayName || user.email}`;
                    // Redirect to monitoring.html after successful sign-in
                   // window.location.href = '/main-menu.html';
                   //const mainMenuPlaceholder = document.getElementById('main-menu-placeholder');

                   // Load main-menu.html content dynamically
                //    fetch('templates/main-menu.html')
                //        .then(response => response.text())
                //        .then(html => {
                //            mainMenuPlaceholder.innerHTML = html;
                //         })
                //         .catch(error => {
                //             console.error('Error loading main-menu.html:', error);
                //         });
                const usernamePlaceholder = document.getElementById('username-placeholder');
                if (usernamePlaceholder) {
                    usernamePlaceholder.textContent = user.displayName || user.email;
                }
                const mainMenuContent = document.getElementById('main-menu-content');
                // Show main menu content
                mainMenuContent.style.display = 'block';
        
                // Hide the login form
                const loginForm = document.getElementById('login-form');
                loginForm.style.display = 'none';
         }) })
            .catch((error) => {
                const errorCode = error.code;
                const errorMessage = error.message;
        
                alert(errorMessage);
            });
                        // Hide the login form or perform other actions as needed
        //                 const loginForm = document.getElementById('login-form');
        //                 loginForm.style.display = 'none';
        // })})
        //             .catch((error) => {
        //                 const errorCode = error.code;
        //                 const errorMessage = error.message;
                
        //                 alert(errorMessage);
        //             });
                

        const signoutButton = document.getElementById('signout');

signoutButton.addEventListener('click', (e) => {
  e.preventDefault();

  const auth = getAuth();
  auth.signOut().then(() => {
    alert('User Signed Out');

    // Redirect to the home page after successful sign-out
    window.location.href = "{{ url_for('home') }}";
  }).catch((error) => {
    console.error('Error signing out:', error);
    alert('Error during sign-out. Please try again.');
  });
});