// Store JWT Token
function saveToken(token) {
    localStorage.setItem("jwt", token);
}

// Retrieve JWT Token
function getToken() {
    return localStorage.getItem("jwt");
}

// Redirect If Not Logged In
function checkAuth() {
    if (!getToken()) {
        window.location.href = "/login"; // Redirect to login if not authenticated
    }
}

// Logout Function
function logout() {
    localStorage.removeItem("jwt");
    alert("Logged out successfully!");
    window.location.href = "/login"; // Redirect back to login page
}

function login() {
    let email = document.getElementById("login-email").value.trim();
    let password = document.getElementById("login-password").value.trim();

    //  Prevent empty fields
    if (!email || !password) {
        alert("Email and password are required!");
        return;
    }

    fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.token) {
            saveToken(data.token);
            alert("Login successful!");
            window.location.href = "/";
        } else {
            alert(data.error);  // Show backend error message
        }
    });
}

// User Registration
function register() {
    let email = document.getElementById("login-email").value;
    let password = document.getElementById("login-password").value;

    fetch("/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    })
    .then(response => response.json())
    .then(data => alert(data.message));
}







