document.addEventListener("DOMContentLoaded", loadContacts);

function loadContacts() {
    fetch("/get_contacts")
        .then(response => response.json())
        .then(data => displayContacts(data.contacts))
        .catch(error => console.error("Error loading contacts:", error));
}

function addContact() {
    let name = document.getElementById("name").value;
    let age = document.getElementById("age").value;
    let email = document.getElementById("email").value;

    if (!name || !age || !email) {
        alert("Please fill all fields!");
        return;
    }

    fetch("/add_contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, age, email })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            loadContacts();  // Reload the updated contact list
        }
    });
}

function displayContacts(contacts) {
    let contactList = document.getElementById("contacts");
    contactList.innerHTML = "";

    contacts.forEach((person, index) => {
        let li = document.createElement("li");
        li.innerHTML = `
            ${person.name} | ${person.age} | ${person.email}
            <button onclick="deleteContact(${index})">Delete</button>
        `;
        contactList.appendChild(li);
    });
}

function deleteContact(index) {
    fetch(`/delete_contact/${index}`, { method: "DELETE" })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                loadContacts();  // Reload the updated list
            }
        });
}

function searchContact() {
    let searchValue = document.getElementById("search").value.trim();
    
    if (searchValue === "") {
        loadContacts();
        return;
    }

    fetch(`/search_contacts/${searchValue}`)
        .then(response => response.json())
        .then(data => displayContacts(data.contacts));
}
