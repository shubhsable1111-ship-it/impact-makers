async function registerUser() {
  const data = {
    name: document.getElementById("name").value,
    email: document.getElementById("email").value,
    job_type: document.getElementById("job").value,
    months_active: parseInt(document.getElementById("months").value)
  };

  const result = await apiPost("/register", data);
  localStorage.setItem("userId", result.id);
  window.location.href = "dashboard.html";
}
