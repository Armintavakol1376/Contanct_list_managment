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

// Get JWT token
function addContact() {
    let name = document.getElementById("name").value.trim();
    let age = document.getElementById("age").value.trim();
    let email = document.getElementById("email").value.trim();
    let token = getToken();  

    // Prevent empty inputs
    if (!name || !age || !email) {
        alert("All fields are required!");
        return;
    }

    fetch("/add_contact", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}` // Send token
        },
        body: JSON.stringify({ name, age, email })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Contact added successfully!");
            location.reload(); // Reload to update contact list
        } else {
            alert(data.error || "Failed to add contact.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred while adding the contact.");
    });
}

// Load Contacts from the Server
function loadContacts() {
    let token = getToken();
    if (!token) {
        return; // No token found; user will be redirected by checkAuth()
    }
    
    fetch("/get_contacts", {
        method: "GET",
        headers: {
            "Authorization": "Bearer " + token
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.contacts) {
            displayContacts(data.contacts);
        } else {
            alert("No contacts found.");
        }
    })
    .catch(error => {
        console.error("Error loading contacts:", error);
        alert("An error occurred while loading contacts.");
    });
}

// Display Contacts in the UI
function displayContacts(contacts) {
    let contactsList = document.getElementById("contacts");
    contactsList.innerHTML = ""; // Clear current list

    contacts.forEach(contact => {
        // Create a new list item for each contact
        let li = document.createElement("li");
        li.textContent = `${contact.name} (Age: ${contact.age}) - ${contact.email}`;
        contactsList.appendChild(li);
    });
}

// Update displayContacts() to show Edit and Delete buttons
function displayContacts(contacts) {
    let contactsList = document.getElementById("contacts");
    contactsList.innerHTML = ""; // Clear current list

    contacts.forEach(contact => {
        let li = document.createElement("li");
        li.textContent = `${contact.name} (Age: ${contact.age}) - ${contact.email}`;
        
        // Create Edit Button
        let editBtn = document.createElement("button");
        editBtn.textContent = "Edit";
        editBtn.style.marginLeft = "10px";
        editBtn.onclick = function() {
            editContact(contact.id);
        };

        // Create Delete Button
        let deleteBtn = document.createElement("button");
        deleteBtn.textContent = "Delete";
        deleteBtn.style.marginLeft = "5px";
        deleteBtn.onclick = function() {
            deleteContact(contact.id);
        };

        li.appendChild(editBtn);
        li.appendChild(deleteBtn);
        contactsList.appendChild(li);
    });
}

//Add the following function to call your DELETE endpoint
function deleteContact(contactId) {
    let token = getToken();
    if (!token) {
        alert("You are not logged in");
        return;
    }

    fetch(`/delete_contact/${contactId}`, {
        method: "DELETE",
        headers: {
            "Authorization": "Bearer " + token
        }
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message || data.error);
        loadContacts();  // Refresh contact list after deletion
    })
    .catch(error => {
        console.error("Error deleting contact:", error);
        alert("An error occurred while deleting the contact.");
    });
}

//You can use a simple prompt() for basic editing
function editContact(contactId) {
    let token = getToken();
    if (!token) {
        alert("You are not logged in");
        return;
    }

    // Prompt the user for new values
    let newName = prompt("Enter new name:");
    let newAge = prompt("Enter new age:");
    let newEmail = prompt("Enter new email:");

    // Basic validation can be added here if desired
    fetch(`/edit_contact/${contactId}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({ name: newName, age: newAge, email: newEmail })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message || data.error);
        loadContacts();  // Refresh the contact list after editing
    })
    .catch(error => {
        console.error("Error editing contact:", error);
        alert("An error occurred while editing the contact.");
    });
}






