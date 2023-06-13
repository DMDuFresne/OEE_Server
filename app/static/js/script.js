// Wait for the DOM to be fully loaded
document.addEventListener("DOMContentLoaded", () => {
  // Get the form element
  const form = document.getElementById("oeeForm");

  // Add an event listener for the form submission
  form.addEventListener("submit", async (event) => {
    event.preventDefault(); // Prevent the default form submission

    // Get the form values
    const goodCount = parseFloat(document.getElementById("goodCount").value);
    const totalCount = parseFloat(document.getElementById("totalCount").value);
    const runTime = parseFloat(document.getElementById("runTime").value);
    const totalTime = parseFloat(document.getElementById("totalTime").value);
    const targetCount = parseFloat(document.getElementById("targetCount").value);

    // Validate the form values
    if (isNaN(goodCount) || isNaN(totalCount) || isNaN(runTime) || isNaN(totalTime) || isNaN(targetCount)) {
      displayError("Invalid input. Please enter numeric values.");
      return;
    }

    // Create a JSON object with the input data
    const data = {
      good_count: goodCount,
      total_count: totalCount,
      run_time: runTime,
      total_time: totalTime,
      target_count: targetCount,
    };

    try {
      // Send a POST request to the Flask API
      const response = await fetch("/oee/calculate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        // Parse the response JSON
        const result = await response.json();

        // Display the calculated OEE values in the UI
        displayResult(result);
      } else {
        // Handle the case when the response is not JSON
        const errorResponse = await response.text();
        throw new Error(errorResponse);
      }
    } catch (error) {
      console.error("Error calculating OEE:", error);
      // Display an error message in the UI
      displayError(error.message);
    }
  });
});

// Function to display the calculated OEE values in the UI
function displayResult(result) {
  // Show the result container
  const resultContainer = document.getElementById("resultContainer");
  resultContainer.classList.remove("hidden");
  resultContainer.innerHTML = ""; // Clear previous content

  // Update the result values in the UI
  const availabilityElement = document.createElement("p");
  availabilityElement.textContent = `Availability: ${result.availability}`;
  resultContainer.appendChild(availabilityElement);

  const performanceElement = document.createElement("p");
  performanceElement.textContent = `Performance: ${result.performance}`;
  resultContainer.appendChild(performanceElement);

  const qualityElement = document.createElement("p");
  qualityElement.textContent = `Quality: ${result.quality}`;
  resultContainer.appendChild(qualityElement);

  const oeeElement = document.createElement("p");
  oeeElement.textContent = `OEE: ${result.oee}`;
  resultContainer.appendChild(oeeElement);

  const timestampElement = document.createElement("p");
  timestampElement.textContent = `Timestamp: ${result.timestamp}`;
  resultContainer.appendChild(timestampElement);
}

// Function to display an error message in the UI
function displayError(message) {
  // Show the result container
  const resultContainer = document.getElementById("resultContainer");
  resultContainer.classList.remove("hidden");
  resultContainer.innerHTML = ""; // Clear previous content

  // Update the error message in the UI
  const errorElement = document.createElement("p");
  errorElement.classList.add("error");
  errorElement.textContent = message;
  resultContainer.appendChild(errorElement);
}
