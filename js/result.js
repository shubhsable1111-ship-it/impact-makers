const data = JSON.parse(localStorage.getItem("scoreData"));

if(data){
  document.getElementById("score-circle").innerText =
    data.digital_trust_score + "/100";

  document.getElementById("risk").innerText =
    "Risk: " + data.risk_category;

  const list = document.getElementById("explanation");
  data.explanation.forEach(item=>{
    const li = document.createElement("li");
    li.innerText = item;
    list.appendChild(li);
  });
}
