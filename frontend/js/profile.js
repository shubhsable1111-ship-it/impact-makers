async function loadProfile(){
  const id = localStorage.getItem("userId");
  const data = await apiGet("/user/" + id);

  document.getElementById("profile-data").innerHTML =
    `<p>Name: ${data.name}</p>
     <p>Email: ${data.email}</p>
     <p>Job: ${data.job_type}</p>
     <p>Score: ${data.credit_profile?.digital_trust_score || "N/A"}</p>`;
}

loadProfile();
