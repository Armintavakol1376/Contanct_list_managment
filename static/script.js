/* =========================
   script.js – Consolidated Version
   ========================= */

/* ----- Token & Role Functions ----- */
function saveToken(token) {
    localStorage.setItem("jwt", token);
}

function getToken() {
    return localStorage.getItem("jwt");
}

/* ----- Authentication Check & Logout ----- */
function checkAuth() {
    if (!getToken()) {
        window.location.href = "/login"; // Redirect to login if not authenticated
    }
}

function logout() {
    localStorage.removeItem("jwt");
    localStorage.removeItem("role");
    alert("Logged out successfully!");
    window.location.href = "/login";
}

/* ----- Login & Registration ----- */
function login() {
    let email = document.getElementById("login-email").value.trim();
    let password = document.getElementById("login-password").value.trim();

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
            localStorage.setItem("role", data.role);
            alert(`Login successful! You are logged in as ${data.role}`);
            window.location.href = "/";
        } else {
            alert(data.error);
        }
    })
    .catch(error => {
        console.error("Error during login:", error);
        alert("An error occurred during login.");
    });
}

function register() {
    let email = document.getElementById("login-email").value.trim();
    let password = document.getElementById("login-password").value.trim();

    if (!email || !password) {
        alert("Email and password are required for registration!");
        return;
    }

    fetch("/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    })
    .then(response => response.json())
    .then(data => alert(data.message || data.error))
    .catch(error => {
        console.error("Error during registration:", error);
        alert("An error occurred during registration.");
    });
}

/* ----- Contact Management ----- */
function addContact() {
    let name = document.getElementById("name").value.trim();
    let age = document.getElementById("age").value.trim();
    let email = document.getElementById("email").value.trim();
    let token = getToken();

    if (!name || !age || !email) {
        alert("All fields are required!");
        return;
    }

    fetch("/add_contact", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ name, age, email })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Contact added successfully!");
            loadContacts(); // Reload to update contact list
        } else {
            alert(data.error || "Failed to add contact.");
        }
    })
    .catch(error => {
        console.error("Error adding contact:", error);
        alert("An error occurred while adding the contact.");
    });
}

/* ----- Load & Search Contacts ----- */
function loadContacts(query = '') {
    let token = getToken();
    if (!token) return;

    let url = '/get_contacts';
    if (query) {
        url += '?q=' + encodeURIComponent(query);
    }

    fetch(url, {
        method: "GET",
        headers: { "Authorization": "Bearer " + token }
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

function searchContact() {
    const searchTerm = document.getElementById("search").value.trim();
    loadContacts(searchTerm);
}

/* ----- Display Contacts (Conditional Buttons) ----- */
function displayContacts(contacts) {
    let contactsList = document.getElementById("contacts");
    contactsList.innerHTML = "";
    let role = localStorage.getItem("role");

    contacts.forEach(contact => {
        let li = document.createElement("li");
        li.textContent = `${contact.name} (Age: ${contact.age}) - ${contact.email}`;
        
        // Show Edit button for admin & manager
        if (role === "admin" || role === "manager") {
            let editBtn = document.createElement("button");
            editBtn.textContent = "Edit";
            editBtn.style.marginLeft = "10px";
            editBtn.onclick = function() { openEditModal(contact); };
            li.appendChild(editBtn);
        }
        
        // Show Delete button only for admin
        if (role === "admin") {
            let deleteBtn = document.createElement("button");
            deleteBtn.textContent = "Delete";
            deleteBtn.style.marginLeft = "5px";
            deleteBtn.onclick = function() { deleteContact(contact.id); };
            li.appendChild(deleteBtn);
        }
        
        contactsList.appendChild(li);
    });
}

/* ----- Edit & Delete Contacts ----- */
function deleteContact(contactId) {
    let token = getToken();
    if (!token) {
        alert("You are not logged in");
        return;
    }

    fetch(`/delete_contact/${contactId}`, {
        method: "DELETE",
        headers: { "Authorization": "Bearer " + token }
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message || data.error);
        loadContacts();
    })
    .catch(error => {
        console.error("Error deleting contact:", error);
        alert("An error occurred while deleting the contact.");
    });
}

function openEditModal(contact) {
    document.getElementById("edit-contact-id").value = contact.id;
    document.getElementById("edit-name").value = contact.name;
    document.getElementById("edit-age").value = contact.age;
    document.getElementById("edit-email").value = contact.email;
    document.getElementById("editModal").style.display = "block";
}

function closeEditModal() {
    document.getElementById("editModal").style.display = "none";
}

function editContact() {
    let token = getToken();
    if (!token) {
        alert("You are not logged in");
        return;
    }

    let contactId = document.getElementById("edit-contact-id").value;
    let newName = document.getElementById("edit-name").value.trim();
    let newAge = document.getElementById("edit-age").value.trim();
    let newEmail = document.getElementById("edit-email").value.trim();

    if (!newName || !newAge || !newEmail) {
        alert("All fields are required!");
        return;
    }

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
        closeEditModal();
        loadContacts();
    })
    .catch(error => {
        console.error("Error editing contact:", error);
        alert("An error occurred while editing the contact.");
    });
}
