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

  // Format the OEE results as percentages with up to 2 decimal points
  const formattedAvailability = (parseFloat(result.availability) * 100).toFixed(2) + "%";
  const formattedPerformance = (parseFloat(result.performance) * 100).toFixed(2) + "%";
  const formattedQuality = (parseFloat(result.quality) * 100).toFixed(2) + "%";
  const formattedOEE = (parseFloat(result.oee) * 100).toFixed(2) + "%";

  // Update the innerHTML of the resultContainer with the formatted OEE values and gauges
  resultContainer.innerHTML = `
    <h1>OEE</h1>
    <label>Availability</label>
    <div class="result-item">
      <div class="oee-gauge">
        <div class="oee-fill" id="availabilityBar"></div>
        <div class="oee-label" id="availabilityLabel">${formattedAvailability}</div>
      </div>
    </div>
    <label>Performance</label>
    <div class="result-item">
      <div class="oee-gauge">
        <div class="oee-fill" id="performanceBar"></div>
        <div class="oee-label" id="performanceLabel">${formattedPerformance}</div>
      </div>
    </div>
    <label>Quality</label>
    <div class="result-item">
      <div class="oee-gauge">
        <div class="oee-fill" id="qualityBar"></div>
        <div class="oee-label" id="qualityLabel">${formattedQuality}</div>
      </div>
    </div>
    <label>OEE</label>
    <div class="result-item">
      <div class="oee-gauge">
        <div class="oee-fill" id="oeeBar"></div>
        <div class="oee-label" id="oeeLabel">${formattedOEE}</div>
      </div>
    </div>
    <p id="timestamp">Timestamp: ${result.timestamp}</p>
  `;

  // Update the gauges
  updateGauge(parseFloat(result.availability), "availabilityBar");
  updateGauge(parseFloat(result.performance), "performanceBar");
  updateGauge(parseFloat(result.quality), "qualityBar");
  updateGauge(parseFloat(result.oee), "oeeBar");
}

function updateGauge(value, gaugeId) {
  const gaugeElement = document.getElementById(gaugeId);

  if (gaugeElement) {
    gaugeElement.style.width = value * 100 + "%";

    // Update the gauge color based on the value
    if (value > 0.8) {
      gaugeElement.style.backgroundColor = "var(--success-color)";
    } else if (value > 0.6) {
      gaugeElement.style.backgroundColor = "var(--primary-color)";
    } else {
      gaugeElement.style.backgroundColor = "var(--danger-color)";
    }
  }
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
