// static/script.js
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('generate').addEventListener('click', function() {
        const city = document.getElementById('city').value;
        const days = document.getElementById('days').value;

        // Validate input
        if (!city || !days) {
            alert('Please enter both city and number of days.');
            return;
        }

        // Disable the button to prevent multiple clicks
        document.getElementById('generate').disabled = true;
        document.getElementById('generate').innerText = 'Generating...';

        // Send data to the backend
        fetch('/generate-itinerary', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                city: city,
                days: days
            })
        })
        .then(response => response.json())
        .then(data => {
            // Display the itinerary
            document.getElementById('itinerary').innerHTML = `<pre>${data.itinerary}</pre>`;

            // Re-enable the button
            document.getElementById('generate').disabled = false;
            document.getElementById('generate').innerText = 'Generate Itinerary';
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while generating the itinerary.');

            // Re-enable the button
            document.getElementById('generate').disabled = false;
            document.getElementById('generate').innerText = 'Generate Itinerary';
        });
    });
});
