// script.js

// Function to trigger the scraping process
document.getElementById('scrapeButton').addEventListener('click', function () {
    const url = document.getElementById('urlInput').value;
    const errorMessage = document.getElementById('errorMessage');

    // Validate the input (make sure the URL is not empty)
    if (!url) {
        errorMessage.style.display = 'block';
        return;
    } else {
        errorMessage.style.display = 'none';
    }

    // Make a POST request to your Flask server with the URL
    fetch('http://localhost:5001/scrape', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: url }),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        alert('Scraping completed successfully!');
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error occurred while scraping. Please try again.');
    });
});
