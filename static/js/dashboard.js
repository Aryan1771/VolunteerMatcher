let problemTypeChart;
let areaChart;

function showDashboardMessage(message) {
  const messageBox = document.getElementById("dashboardMessage");
  messageBox.textContent = message;
  messageBox.classList.remove("hidden");
  messageBox.classList.add("message-error");
}

function text(value) {
  return escapeHtml(value || "-");
}

function escapeHtml(value) {
  const element = document.createElement("div");
  element.textContent = String(value);
  return element.innerHTML;
}

function skillsCell(skills) {
  if (!skills || skills.length === 0) {
    return "-";
  }

  return skills.map((skill) => `<span class="pill">${escapeHtml(skill)}</span>`).join("");
}

function setSummary(summary) {
  document.getElementById("totalProblems").textContent = summary.totalProblems;
  document.getElementById("totalVolunteers").textContent = summary.totalVolunteers;
  document.getElementById("openProblems").textContent = summary.openProblems;
  document.getElementById("resolvedProblems").textContent = summary.resolvedProblems;
}

function setProblemsTable(problems) {
  const table = document.getElementById("problemsTable");

  if (!problems.length) {
    table.innerHTML = '<tr><td colspan="5">No problems found.</td></tr>';
    return;
  }

  table.innerHTML = problems
    .map(
      (problem) => `
        <tr>
          <td>${text(problem.location)}</td>
          <td>${text(problem.problemType)}</td>
          <td>${text(problem.severity)}</td>
          <td>${text(problem.status)}</td>
          <td>${text(problem.description)}</td>
        </tr>
      `
    )
    .join("");
}

function setVolunteersTable(volunteers) {
  const table = document.getElementById("volunteersTable");

  if (!volunteers.length) {
    table.innerHTML = '<tr><td colspan="4">No volunteers found.</td></tr>';
    return;
  }

  table.innerHTML = volunteers
    .map(
      (volunteer) => `
        <tr>
          <td>${text(volunteer.name)}</td>
          <td>${skillsCell(volunteer.skills)}</td>
          <td>${text(volunteer.preferredLocation)}</td>
          <td>${text(volunteer.availability)}</td>
        </tr>
      `
    )
    .join("");
}

function setRecommendationsTable(items) {
  const table = document.getElementById("recommendationsTable");

  if (!items.length) {
    table.innerHTML = '<tr><td colspan="3">No recommendations found.</td></tr>';
    return;
  }

  table.innerHTML = items
    .map((item) => {
      const matches = item.recommendedVolunteers.length
        ? item.recommendedVolunteers
            .map((volunteer) => `${escapeHtml(volunteer.name)} <span class="pill">Score ${escapeHtml(volunteer.score)}</span>`)
            .join("<br>")
        : "-";

      return `
        <tr>
          <td>${text(item.problem.problemType)} (${text(item.problem.severity)})</td>
          <td>${text(item.problem.location)}</td>
          <td>${matches}</td>
        </tr>
      `;
    })
    .join("");
}

function renderProblemTypeChart(rows) {
  const labels = rows.map((row) => row.type);
  const values = rows.map((row) => row.count);

  if (problemTypeChart) {
    problemTypeChart.destroy();
  }

  problemTypeChart = new Chart(document.getElementById("problemTypeChart"), {
    type: "pie",
    data: {
      labels,
      datasets: [
        {
          data: values,
          backgroundColor: ["#0f766e", "#e11d48", "#f59e0b"],
        },
      ],
    },
    options: {
      maintainAspectRatio: false,
    },
  });
}

function renderAreaChart(rows) {
  const labels = rows.map((row) => row.location);
  const values = rows.map((row) => row.count);

  if (areaChart) {
    areaChart.destroy();
  }

  areaChart = new Chart(document.getElementById("areaChart"), {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label: "Problems",
          data: values,
          backgroundColor: "#0f766e",
        },
      ],
    },
    options: {
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            precision: 0,
          },
        },
      },
    },
  });
}

async function loadDashboard() {
  try {
    const [summary, problems, volunteers, problemTypes, areaProblems, recommendations] = await Promise.all([
      window.api.request("/api/dashboard/summary"),
      window.api.request("/api/problems"),
      window.api.request("/api/volunteers"),
      window.api.request("/api/dashboard/problem-types"),
      window.api.request("/api/dashboard/area-problems"),
      window.api.request("/api/dashboard/recommendations"),
    ]);

    setSummary(summary);
    setProblemsTable(problems);
    setVolunteersTable(volunteers);
    setRecommendationsTable(recommendations);
    renderProblemTypeChart(problemTypes);
    renderAreaChart(areaProblems);
  } catch (error) {
    showDashboardMessage(error.message);
  }
}

document.addEventListener("DOMContentLoaded", loadDashboard);
