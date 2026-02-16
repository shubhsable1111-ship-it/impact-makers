async function calculateScore() {
  const data = {
    user_id: localStorage.getItem("userId"),
    avg_income: parseInt(document.getElementById("income").value),
    income_variance: parseFloat(document.getElementById("variance").value),
    upi_txn_count: parseInt(document.getElementById("upi").value),
    bill_payment_score: parseInt(document.getElementById("bill").value),
    withdrawal_ratio: parseFloat(document.getElementById("withdrawal").value)
  };

  const result = await apiPost("/calculate-score", data);
  localStorage.setItem("scoreData", JSON.stringify(result));
  window.location.href = "result.html";
}
