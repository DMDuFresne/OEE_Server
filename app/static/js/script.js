document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("oeeForm");

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const goodCount = parseFloat(document.getElementById("goodCount").value);
    const totalCount = parseFloat(document.getElementById("totalCount").value);
    const runTime = parseFloat(document.getElementById("runTime").value);
    const totalTime = parseFloat(document.getElementById("totalTime").value);
    const targetCount = parseFloat(document.getElementById("targetCount").value);

    if (isNaN(goodCount) || isNaN(totalCount) || isNaN(runTime) || isNaN(totalTime) || isNaN(targetCount)) {
      displayError("Invalid input. Please enter numeric values.");
      return;
    }

    const data = {
      good_count: goodCount,
      total_count: totalCount,
      run_time: runTime,
      total_time: totalTime,
      target_count: targetCount,
    };

    try {
      const response = await fetch("/oee/calculate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        const result = await response.json();
        displayResult(result);
      } else {
        const errorResponse = await response.text();
        throw new Error(errorResponse);
      }
    } catch (error) {
      console.error("Error calculating OEE:", error);
      displayError(error.message);
    }
  });

  fetch('/asset/all')
    .then(response => response.json())
    .then(data => {
      const container = document.getElementById('treeView');
      const treeView = generateTreeView(data.data);
      container.appendChild(treeView);

      const expandAllBtn = document.getElementById('expandAllBtn');
      const collapseAllBtn = document.getElementById('collapseAllBtn');

      expandAllBtn.addEventListener('click', () => {
        expandAll();
      });

      collapseAllBtn.addEventListener('click', () => {
        collapseAll();
      });
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
      gaugeElement.style.backgroundColor = "var(--warning-color)";
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

// Function to expand all nodes in the tree view
function expandAll() {
  const allNodes = document.querySelectorAll('#treeView .collapsed');

  for(let node of allNodes) {
    node.classList.remove('collapsed');
    node.querySelector('ul').classList.remove('hidden');
  }
}

// Function to collapse all nodes in the tree view
function collapseAll() {
  const allNodes = document.querySelectorAll('#treeView li:not(.no-children)');

  for(let node of allNodes) {
    node.classList.add('collapsed');
    node.querySelector('ul').classList.add('hidden');
  }
}


function generateTreeView(data, collapsed = true) {
  const ul = document.createElement('ul');

  for (let key in data) {
    const li = document.createElement('li');

    if (typeof data[key] === 'object' && data[key] !== null) {
      const span = document.createElement('span');
      span.textContent = key;
      span.classList.add('parent-text');
      li.appendChild(span);

      // Create a caret icon element
      const caret = document.createElement('span');
      caret.classList.add('caret');
      span.insertBefore(caret, span.firstChild);

      const childTreeView = generateTreeView(data[key], collapsed);
      li.appendChild(childTreeView);

      if (collapsed) {
        li.classList.add('collapsed');
        childTreeView.classList.add('hidden');
      }

      span.addEventListener('click', function (event) {
        event.stopPropagation();
        li.classList.toggle('collapsed');
        childTreeView.classList.toggle('hidden');
      });
    } else {
      const div = document.createElement('div');
      div.className = 'key-value';

      const keySpan = document.createElement('span');
      keySpan.textContent = key + ':';

      const valueSpan = document.createElement('span');
      valueSpan.textContent = data[key];

      div.appendChild(keySpan);
      div.appendChild(valueSpan);

      li.appendChild(div);
      li.classList.add('no-children');
    }

    ul.appendChild(li);
  }

  return ul;
}

/* -- Glow effect -- */

const blob = document.getElementById("blob");

window.onpointermove = event => {
  const { clientX, clientY } = event;

  blob.animate({
    left: `${clientX}px`,
    top: `${clientY}px`
  }, { duration: 3000, fill: "forwards" });
}