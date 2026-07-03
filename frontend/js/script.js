async function generateTrip() {

    // Get values from the form
    const destination = document.getElementById("destination").value;
    const budget = document.getElementById("budget").value;
    const days = document.getElementById("days").value;
    const travelStyle = document.getElementById("travelStyle").value;

    // Send data to Flask backend
    const response = await fetch("http://127.0.0.1:5000/generate-trip", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            destination: destination,
            budget: budget,
            days: days,
            travelStyle: travelStyle
        })

    });

    // Receive response from backend
    const data = await response.json();

    // Save complete response
    localStorage.setItem("tripPlan", JSON.stringify(data));

    // Open results page
    window.location.href = "results.html";
}