const API_URL = "http://127.0.0.1:8000";

function getCitizen() {
    const data =
        localStorage.getItem("citizen") ||
        localStorage.getItem("user");

    return data ? JSON.parse(data) : null;
}

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("complaintForm");
    const table = document.getElementById("complaintTable");

    if (form) {
        form.addEventListener("submit", submitComplaint);
    }

    if (table) {
        loadComplaints();
    }
});

async function submitComplaint(event) {
    event.preventDefault();

    const citizen = getCitizen();

    if (!citizen || !citizen.id) {
        alert("Please login first.");
        location.href = "citizenLogin.html";
        return;
    }

    const formData = new FormData();
    formData.append("user_id", citizen.id);
    formData.append(
        "description",
        document.getElementById("description").value.trim()
    );
    formData.append(
        "location",
        document.getElementById("location").value.trim()
    );
    formData.append(
        "category",
        document.getElementById("category").value
    );

    const image = document.getElementById("image");
    if (image && image.files.length > 0) {
        formData.append("image", image.files[0]);
    }

    try {
        const response = await fetch(`${API_URL}/complaints`, {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        if (!response.ok) {
            alert(result.detail || "Complaint submission failed");
            return;
        }

        alert("Complaint submitted successfully!");
        location.href = "citizenDashboard.html";
    } catch (error) {
        console.error(error);
        alert("Backend server is not running.");
    }
}

async function loadComplaints() {
    const citizen = getCitizen();

    if (!citizen || !citizen.id) {
        location.href = "citizenLogin.html";
        return;
    }

    const table = document.getElementById("complaintTable");

    try {
        const response = await fetch(
            `${API_URL}/complaints/user/${citizen.id}`
        );

        const complaints = await response.json();

        if (!response.ok) {
            table.innerHTML = "<tr><td colspan='5'>Unable to load complaints.</td></tr>";
            return;
        }

        if (complaints.length === 0) {
            table.innerHTML = "<tr><td colspan='5'>No complaints found.</td></tr>";
            return;
        }

        table.innerHTML = complaints.map(complaint => `
            <tr>
                <td>${complaint.id}</td>
                <td>${complaint.category}</td>
                <td>${complaint.location}</td>
                <td>${complaint.status}</td>
                <td>${complaint.priority}</td>
            </tr>
        `).join("");
    } catch (error) {
        console.error(error);
        table.innerHTML = "<tr><td colspan='5'>Server connection failed.</td></tr>";
    }
}

function logout() {
    localStorage.removeItem("citizen");
    localStorage.removeItem("user");
    location.href = "citizenLogin.html";
}