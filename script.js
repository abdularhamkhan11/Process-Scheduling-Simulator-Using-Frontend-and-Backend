function generateInputs() {
  const count = parseInt(document.getElementById("processCount").value);
  const form = document.getElementById("processForm");
  form.innerHTML = "";

  for (let i = 0; i < count; i++) {
    form.innerHTML += `
      <div>
        <label>Process P${i + 1}:</label>
        <input type="number" placeholder="Arrival Time" id="at${i}" min="0" required />
        <input type="number" placeholder="Burst Time" id="bt${i}" min="1" required />
      </div>`;
  }
}

document.getElementById("algorithm").addEventListener("change", function () {
  document.getElementById("quantumDiv").style.display = this.value === "RR" ? "block" : "none";
});

async function simulate() {
  const count = parseInt(document.getElementById("processCount").value);
  const algo = document.getElementById("algorithm").value;
  const quantum = parseInt(document.getElementById("quantum").value);

  const processes = [];
  for (let i = 0; i < count; i++) {
    const at = parseInt(document.getElementById(`at${i}`).value);
    const bt = parseInt(document.getElementById(`bt${i}`).value);
    if (isNaN(at) || isNaN(bt)) {
      alert("Please enter valid Arrival and Burst times for all processes.");
      return;
    }
    processes.push({ id: i + 1, at, bt });
  }

  const response = await fetch('/simulate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ processes, algorithm: algo, quantum })
  });

  if (!response.ok) {
    alert("Error in simulation.");
    return;
  }

  const result = await response.json();
  renderOutput(result);
}

function renderOutput(data) {
  const outputDiv = document.getElementById("output");
  const ganttChart = document.getElementById("ganttChart");

  let html = `<h2>📋 Process Table</h2>
    <table>
      <tr>
        <th>Process</th>
        <th>Arrival</th>
        <th>Burst</th>
        <th>Completion</th>
        <th>Waiting</th>
        <th>Turnaround</th>
      </tr>`;

  data.output.forEach(p => {
    html += `<tr>
      <td>P${p.id}</td>
      <td>${p.at}</td>
      <td>${p.bt}</td>
      <td>${p.ct}</td>
      <td>${p.wt}</td>
      <td>${p.tat}</td>
    </tr>`;
  });

  html += "</table>";
  outputDiv.innerHTML = html;

  ganttChart.innerHTML = `<h2>📊 Gantt Chart</h2>`;
  data.timeline.forEach(p => {
    const width = (p.end - p.start) * 20;
    ganttChart.innerHTML += `<div class="bar" style="width:${width}px;" data-time="${p.start}-${p.end}">P${p.id}</div>`;
  });
}
