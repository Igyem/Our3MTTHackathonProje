// Function to handle form submission
function predictDisease() {
    // Get the image file
    const imageFile = document.getElementById('image').files[0];

    // Create a FormData object to send the image
    const formData = new FormData();
    formData.append('image', imageFile);

    // Send AJAX request to the Flask backend
    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json()) // Assuming JSON response
    .then(data => {
        // Display the prediction results
        const resultsDiv = document.getElementById('prediction-results');
        resultsDiv.innerHTML = `
            <h2>Prediction: ${data.class}</h2>
            <p>Confidence: ${data.confidence}%</p>
        `;
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle errors, e.g., display an error message
    });
}

// Add event listener to the form
const form = document.getElementById('prediction-form'); // Replace with your form's ID
form.addEventListener('submit', (event) => {
    event.preventDefault(); // Prevent default form submission
    predictDisease();
});