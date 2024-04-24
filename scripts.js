function addPoints(scaleNumber) {
    const nameInput = document.getElementById(`scale${scaleNumber}-name`);
    const pointsInput = document.getElementById(`scale${scaleNumber}-add`);
    const pointsDisplay = document.getElementById(`scale${scaleNumber}-points`);

    const name = nameInput.value.trim();
    const pointsToAdd = parseInt(pointsInput.value, 10);

    if (!name || isNaN(pointsToAdd) || pointsToAdd <= 0) {
        alert("Please enter a valid name and positive points.");
        return;
    }

    // Update displayed points
    const currentPoints = parseInt(pointsDisplay.textContent, 10);
    const newTotal = currentPoints + pointsToAdd;
    pointsDisplay.textContent = newTotal; // Update the displayed points

    // Send the data to the back-end (adjust the endpoint as needed)
    fetch('/save-points', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, points: newTotal })
    })
    .then(response => response.text())
    .then(data => {
        console.log("Points saved:", data);
    })
    .catch(err => {
        console.error("Error saving points:", err);
    });
}