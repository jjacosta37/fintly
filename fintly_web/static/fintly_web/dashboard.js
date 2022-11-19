//Run Fuctions
drawDropdown();
toggleSidebar();
drawCategoryDropdown();

//Load charts
month = btnMonth.innerText;
loadPieChart(month);
loadIES(month);
loadTable(month, "All");
loadLineChart();

// Toggle sidebar on mobile

function toggleSidebar() {
  if ($(window).width() < 960) {
    let sidebar = document.getElementById("sidebarJQ");
    sidebar.className =
      "navbar-nav bg-gradient-primary sidebar sidebar-dark accordion toggled";
  }
}

//Draw month in Month button and its dropdown

function getCurrentMonth(v = 0) {
  const dateObj = new Date();
  dateObj.setMonth(dateObj.getMonth() - v);
  let monthName = dateObj.toLocaleString("es-ES", { month: "long" });
  monthName = monthName.charAt(0).toUpperCase() + monthName.slice(1);
  return monthName;
}

function drawDropdown(monthName = getCurrentMonth()) {
  // Draw month in button

  let btnMonth = document.getElementById("btnMonth");
  btnMonth.innerHTML = `${monthName}<i
  class="fas fa-chevron-circle-down ml-2 d-none d-md-inline"></i>`;

  // Draw months in dropdown
  let btnDropdown = document.getElementById("btnDropdown");
  btnDropdown.innerHTML = "";
  for (let i = 0; i < 6; i++) {
    monthDropdown = getCurrentMonth(i);
    const link = document.createElement("a");
    link.className = "dropdown-item";
    link.innerText = monthDropdown;
    link.setAttribute("href", "#");
    btnDropdown.appendChild(link);
  }
}

// Update Transactions
// document.addEventListener("DOMContentLoaded", updateTransactions());

function updateTransactions() {
  console.log("prueba");
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
      month = btnMonth.innerText;
      loadPieChart(month);
      loadIES(month);
      drawCategoryDropdown();
      loadTable(month, "All");
      loadLineChart();
    })
    .catch((error) => {
      console.log(error);
    });
}

//Update data when new month is selected

let btnDropdown = document.getElementById("btnDropdown");
btnDropdown.addEventListener("click", function (e) {
  monthNew = e.target.innerText;
  monthNew2 = monthNew.toLocaleString("en-US", { month: "long" });
  console.log(monthNew2);
  loadPieChart(monthNew);
  loadIES(monthNew);
  drawDropdown(monthNew);
  loadTable(monthNew, "All");
  drawCategoryDropdown();
});

// Draw Category Dropdown

function drawCategoryDropdown() {
  let categoryDropdown = document.getElementById("categoryDropdown");
  month = btnMonth.innerText;

  fetch(urlPath + `getdistinctcategory/?month=${month}`, {
    method: "GET",
  })
    .then((response) => response.json())
    .then((data) => fetchDrawCategoryDropdown(data))
    .catch((error) => console.error("Error:", error));

  function fetchDrawCategoryDropdown(data) {
    categoryDropdown.innerHTML = '<a href="#" class="dropdown-item">All</a>';
    for (let i = 0; i < data.length; i++) {
      const link = document.createElement("a");
      link.className = "dropdown-item";
      link.innerText = data[i].category;
      link.setAttribute("href", "#");
      categoryDropdown.appendChild(link);
    }
  }
}

//Update table when new category is selected

let categoryDropdown = document.getElementById("categoryDropdown");
categoryDropdown.addEventListener("click", function (e) {
  let btnCategoryDropdown = document.getElementById("btnCategoryDropdown");
  category = e.target.innerText;
  btnCategoryDropdown.innerHTML = `${category}<i
  class="fas fa-chevron-circle-down ml-2 d-none d-md-inline"></i>`;
  month = btnMonth.innerText;
  loadTable(month, category);
  e.preventDefault();
});
