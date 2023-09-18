// static/script.js

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("investment-form");
    const recommendationsList = document.getElementById("recommendations");

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const amount = parseFloat(document.getElementById("amount").value);
        const risk_tolerance = document.getElementById("risk_tolerance").value;
        const duration = parseInt(document.getElementById("duration").value);
        const target_amount = parseFloat(document.getElementById("target_amount").value);

        // Make an AJAX request to the Flask backend
        fetch("/", {
            method: "POST",
            body: JSON.stringify({
                amount: amount,
                risk_tolerance: risk_tolerance,
                duration: duration,
                target_amount: target_amount
            }),
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            // Clear the previous recommendations
            recommendationsList.innerHTML = "";

            // Iterate through the recommendations and add them to the list
            data.forEach(recommendation => {
                const listItem = document.createElement("li");
                listItem.textContent = `Asset Type: ${recommendation.asset_type}, Symbol: ${recommendation.symbol}, Name: ${recommendation.name}, Allocation: ${recommendation.allocation}, Expected Return: ${recommendation.expected_return}`;
                recommendationsList.appendChild(listItem);
            });
        })
        .catch(error => console.error("Error:", error));
    });
});
