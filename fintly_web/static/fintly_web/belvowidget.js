function updateTransactions() {
  const csrftoken = getCookie("csrftoken");
  fetch(urlPath + "updatetransactions/", {
    method: "POST", // or 'PUT'
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Transactions Updated");
    })
    .catch((error) => {
      console.log(error);
    });
}
