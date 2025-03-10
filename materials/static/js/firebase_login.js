import { initializeApp } from "https://www.gstatic.com/firebasejs/11.4.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/11.4.0/firebase-analytics.js";
import { getAuth, signInWithPopup, GoogleAuthProvider } from "https://www.gstatic.com/firebasejs/11.4.0/firebase-auth.js";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyBfy8xJ0PsiY0iGDHwx1LeX2GnTDN-8K-E",
  authDomain: "matscienceweb.firebaseapp.com",
  projectId: "matscienceweb",
  storageBucket: "matscienceweb.firebasestorage.app",
  messagingSenderId: "675001569247",
  appId: "1:675001569247:web:ab3349b822b00b46cefe6a",
  measurementId: "G-280YE5175R"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);

// Google Login function
function googleLogin() {
  const provider = new GoogleAuthProvider();
  signInWithPopup(auth, provider)
    .then((result) => {
      result.user.getIdToken().then((token) => {
        fetch('/firebase-login/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Ensure CSRF token is included
          },
          body: JSON.stringify({ firebase_token: token })
        }).then(response => response.json()).then(data => {
          if (data.status === 'success') {
            window.location.href = '/';
          } else {
            alert('Login failed');
          }
        });
      });
    })
    .catch((error) => {
      if (error.code === 'auth/popup-closed-by-user') {
        console.log("The popup was closed before completing the sign-in.");
      } else {
        console.error("Google Login Error:", error);
      }
    });
}

// Function to get CSRF token from cookies
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Export the googleLogin function to be used in your HTML
export { googleLogin };