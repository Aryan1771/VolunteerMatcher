function showMessage(element, message, type) {
  if (!element) {
    return;
  }

  element.textContent = message;
  element.classList.remove("hidden", "message-success", "message-error");
  element.classList.add(type === "success" ? "message-success" : "message-error");
}

function selectedSkills(form) {
  return Array.from(form.querySelectorAll('input[name="skills"]:checked')).map((input) => input.value);
}

function setMinimumDate(inputId) {
  const input = document.getElementById(inputId);
  if (!input) {
    return;
  }

  input.min = new Date().toISOString().split("T")[0];
}

setMinimumDate("workDate");
setMinimumDate("availableDate");

const problemForm = document.getElementById("problemForm");
if (problemForm) {
  problemForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const messageBox = document.getElementById("problemMessage");
    const formData = new FormData(problemForm);
    const payload = {
      location: formData.get("location"),
      problemType: formData.get("problemType"),
      severity: Number(formData.get("severity")),
      description: formData.get("description"),
      availability: formData.get("availability"),
      workDate: formData.get("workDate"),
    };

    try {
      await window.api.request("/api/problems", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      problemForm.reset();
      showMessage(messageBox, "Problem report submitted successfully.", "success");
    } catch (error) {
      showMessage(messageBox, error.message, "error");
    }
  });
}

const volunteerForm = document.getElementById("volunteerForm");
if (volunteerForm) {
  volunteerForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const messageBox = document.getElementById("volunteerMessage");
    const formData = new FormData(volunteerForm);
    const payload = {
      name: formData.get("name"),
      skills: selectedSkills(volunteerForm),
      preferredLocation: formData.get("preferredLocation"),
      availability: formData.get("availability"),
      availableDate: formData.get("availableDate"),
    };

    try {
      await window.api.request("/api/volunteers", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      volunteerForm.reset();
      showMessage(messageBox, "Volunteer registered successfully.", "success");
    } catch (error) {
      showMessage(messageBox, error.message, "error");
    }
  });
}

const loginForm = document.getElementById("loginForm");
if (loginForm) {
  loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const messageBox = document.getElementById("loginMessage");
    const formData = new FormData(loginForm);
    const payload = {
      username: formData.get("username"),
      password: formData.get("password"),
    };

    try {
      await window.api.request("/api/auth/login", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      window.location.href = "/admin/dashboard";
    } catch (error) {
      showMessage(messageBox, error.message, "error");
    }
  });
}
