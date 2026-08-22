const API_URL = "http://127.0.0.1:8000";

async function citizenLogin() {
    const response = await fetch(`${API_URL}/auth/citizen-login`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            email: document.getElementById("email").value.trim(),
            password: document.getElementById("password").value
        })
    });

    const result = await response.json();

    if (!response.ok) {
        alert(result.detail || "Invalid credentials");
        return false;
    }

    localStorage.setItem("citizen", JSON.stringify(result));
    localStorage.setItem("user", JSON.stringify(result));

    window.location.assign("citizenDashboard.html");
    return false;
}
async function citizenRegister(event) {
    event.preventDefault();

    const response = await fetch(`${API_URL}/auth/register`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: document.getElementById("name").value.trim(),
            email: document.getElementById("email").value.trim(),
            mobile: document.getElementById("mobile").value.trim(),
            password: document.getElementById("password").value
        })
    });

    const result = await response.json();

    if (!response.ok) {
        alert(result.detail || "Registration failed");
        return false;
    }

    alert("Registration successful!");
    window.location.href = "citizenLogin.html";
    return false;
}
async function adminLogin(event) {
    if (event) event.preventDefault();

    const response = await fetch(`${API_URL}/auth/admin-login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            admin_id: document.getElementById("adminId").value.trim(),
            password: document.getElementById("password").value
        })
    });

    const result = await response.json();

    if (!response.ok) {
        alert(result.detail || "Invalid admin credentials");
        return false;
    }

    localStorage.setItem("admin", JSON.stringify(result));
    window.location.href = "adminDashboard.html";

    return false;
}
async function officerLogin(event) {
    event.preventDefault();

    try {
        const response = await fetch(`${API_URL}/auth/officer-login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                officer_id: document.getElementById("officerId").value.trim(),
                password: document.getElementById("password").value
            })
        });

        const result = await response.json();

        if (!response.ok) {
            alert(result.detail || "Invalid officer credentials");
            return false;
        }

        localStorage.setItem("officer", JSON.stringify(result));
        window.location.href = "officerDashboard.html";
    } catch (error) {
        alert("Backend server is not running.");
        console.error(error);
    }

    return false;
}