const API_URL = "http://127.0.0.1:8000";

document.addEventListener("DOMContentLoaded", async () => {
    const table = document.getElementById("complaintTable");

    // केवल officer dashboard पर चलेगा
    if (!table) return;

    const officer = JSON.parse(localStorage.getItem("officer") || "null");

    if (!officer) {
        alert("Please login first.");
        window.location.href = "officerLogin.html";
        return;
    }

    const department = officer.department || "Road Department";
    document.getElementById("departmentText").textContent =
        `Department: ${department}`;

    try {
        const response = await fetch(
            `${API_URL}/officer/complaints/${encodeURIComponent(department)}`
        );

        const complaints = await response.json();

        if (!response.ok || complaints.length === 0) {
            table.innerHTML = `
                <tr>
                    <td colspan="5">No complaints assigned.</td>
                </tr>
            `;
            return;
        }

        table.innerHTML = complaints.map(complaint => `
            <tr>
                <td>${complaint.id}</td>
                <td>${complaint.description}</td>
                <td>${complaint.priority}</td>
                <td>${complaint.status}</td>
                <td>
                    <a href="officerComplaintDetail.html?id=${complaint.id}">
                        View
                    </a>
                </td>
            </tr>
        `).join("");

    } catch (error) {
        console.error(error);
        table.innerHTML = `
            <tr>
                <td colspan="5">Unable to load complaints.</td>
            </tr>
        `;
    }
});