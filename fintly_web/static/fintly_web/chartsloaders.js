function loadPieChart(month) {
  google.charts.load("current", { packages: ["corechart"] });
  google.charts.load("current", { packages: ["bar"] });
  google.charts.setOnLoadCallback(drawPieChart);

  // let month = document.getElementById("btnMonth");

  function drawPieChart() {
    fetch(urlPath + `getcategorygroupby/?month=${month}`, { method: "GET" })
      .then((response) => response.json())
      .then((data) => drawChart(data))
      .catch((error) => console.error("Error:", error));

    function drawChart(a) {
      table = [["Task", "Hours per Day"]];

      for (let i = 0; i < a.length; i++) {
        table.push([a[i].category, a[i].total_price]);
      }

      var data = google.visualization.arrayToDataTable(table);

      let pieOptions = {
        pieHole: 0.7,
        chartArea: { width: "100%", height: "90%" },
        theme: "material",
        pieSliceText: "none",
        colors: [
          "#C2DCE3",
          "#67A8B9",
          "#0C748F",
          "#09576B",
          "#084859",
          "#052B36",
        ],
      };

      var chart = new google.visualization.PieChart(
        document.getElementById("donutchart")
      );
      chart.draw(data, pieOptions);

      google.visualization.events.addListener(chart, "select", function (e) {
        col = chart.getSelection()[0].row + 1;
        cat = table[col][0];
        let btnCategoryDropdown = document.getElementById(
          "btnCategoryDropdown"
        );
        btnCategoryDropdown.innerHTML = `${cat}<i
        class="fas fa-chevron-circle-down ml-2 d-none d-md-inline"></i>`;
        drawTable(month, cat);
      });
    }
  }
}

function loadIES(month) {
  // Draw Expenses

  function drawGastos() {
    let expense_html = document.getElementById("Expenses");
    let income_html = document.getElementById("income");
    let savings_html = document.getElementById("savings_projection");

    fetch(urlPath + `getincomeoutcome/?month=${month}`, { method: "GET" })
      .then((response) => response.json())
      .then((data) => drawExpenses(data))
      .catch((error) => console.error("Error:", error));

    function drawExpenses(a) {
      try {
        let expense = Math.round(a[1].outcome);
        let income = Math.round(a[0].income);
        let savings = Math.round(a[2].savings);

        exp = expense.toLocaleString("en-US");
        inc = income.toLocaleString("en-US");
        sav = savings.toLocaleString("en-US");

        expense_html.textContent = `$${exp}`;
        income_html.textContent = `$${inc}`;
        savings_html.textContent = `$${sav}`;
      } catch {}
    }
  }

  // Draw Savings

  function drawSav() {
    let savings = document.getElementById("savings");
    fetch(urlPath + "updateincomesavings/", { method: "GET" })
      .then((response) => response.json())
      .then((data) => drawSavings(data))
      .catch((error) => console.error("Error:", error));

    function drawSavings(a) {
      let inc = Math.round(a["ahorro"]);
      inc = inc.toLocaleString("en-US");
      console.log(inc);
      savings.textContent = `$${inc}`;
    }
  }

  drawGastos();
  // drawInc();
  drawSav();
}

function loadTable(month, category) {
  fetch(urlPath + `getexpenselist/?month=${month}&category=${category}`, {
    method: "GET",
  })
    .then((response) => response.json())
    .then((data) => fetchDrawTable(data))
    .catch((error) => console.error("Error:", error));

  function fetchDrawTable(data) {
    let list = document.getElementById("tbody");
    list.innerHTML = "";

    if ($.fn.dataTable.isDataTable("#dataTable")) {
      console.log("prueba destroy");
      $("#dataTable").DataTable().clear();
      $("#dataTable").DataTable().destroy();
    }

    for (let i = 0; i < data.length; i++) {
      const row = document.createElement("tr");
      let amount = Math.round(data[i].amount);
      amount = amount.toLocaleString("en-US");
      row.innerHTML = `
              <td>'${data[i].category}'</td>
              <td>${data[i].description}</td>
              <td>${data[i].transaction_date}</td>
              <td>$ ${amount}</td>
            `;

      console.log(data[i].transaction_date);

      list.appendChild(row);
    }

    $(document).ready(function () {
      $("#dataTable").DataTable({
        order: [[3, "desc"]],
      });
    });
  }
}

function loadLineChart() {
  fetch(urlPath + `getexpensesbymonth/`, { method: "GET" })
    .then((response) => response.json())
    .then((data) => drawLineChart(data))
    .catch((error) => console.error("Error:", error));

  function drawLineChart(data) {
    // Set new default font family and font color to mimic Bootstrap's default styling
    (Chart.defaults.global.defaultFontFamily = "Nunito"),
      '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
    Chart.defaults.global.defaultFontColor = "#858796";

    let dataLC = [];
    let labelsLC = [];

    for (let i = 0; i < data.length; i++) {
      const dateObjTest = new Date(data[i].month + " 00:00:00");
      const month = dateObjTest.toLocaleString("default", { month: "short" });

      dataLC.push(data[i].total_price);
      labelsLC.push(month);
    }

    function number_format(number, decimals, dec_point, thousands_sep) {
      // *     example: number_format(1234.56, 2, ',', ' ');
      // *     return: '1 234,56'
      number = (number + "").replace(",", "").replace(" ", "");
      var n = !isFinite(+number) ? 0 : +number,
        prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
        sep = typeof thousands_sep === "undefined" ? "," : thousands_sep,
        dec = typeof dec_point === "undefined" ? "." : dec_point,
        s = "",
        toFixedFix = function (n, prec) {
          var k = Math.pow(10, prec);
          return "" + Math.round(n * k) / k;
        };
      // Fix for IE parseFloat(0.55).toFixed(0) = 0;
      s = (prec ? toFixedFix(n, prec) : "" + Math.round(n)).split(".");
      if (s[0].length > 3) {
        s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
      }
      if ((s[1] || "").length < prec) {
        s[1] = s[1] || "";
        s[1] += new Array(prec - s[1].length + 1).join("0");
      }
      return s.join(dec);
    }

    // Area Chart Example

    var ctx = document.getElementById("myAreaChart");
    var myLineChart = new Chart(ctx, {
      type: "line",
      data: {
        labels: labelsLC,
        datasets: [
          {
            label: "Gastos",
            lineTension: 0.3,
            backgroundColor: "rgba(12, 116, 143, 0.05)",
            borderColor: "rgba(12, 116, 143, 1)",
            pointRadius: 3,
            pointBackgroundColor: "rgba(12, 116, 143, 1)",
            pointBorderColor: "rgba(12, 116, 143, 1)",
            pointHoverRadius: 3,
            pointHoverBackgroundColor: "rgba(12, 116, 143, 1)",
            pointHoverBorderColor: "rgba(12, 116, 143, 1)",
            pointHitRadius: 10,
            pointBorderWidth: 2,
            data: dataLC,
          },
        ],
      },
      options: {
        maintainAspectRatio: false,
        layout: {
          padding: {
            left: 10,
            right: 25,
            top: 15,
            bottom: 0,
          },
        },
        scales: {
          xAxes: [
            {
              time: {
                unit: "date",
              },
              gridLines: {
                display: false,
                drawBorder: false,
              },
              ticks: {
                maxTicksLimit: 7,
              },
            },
          ],
          yAxes: [
            {
              ticks: {
                maxTicksLimit: 5,
                padding: 10,
                // Include a dollar sign in the ticks
                callback: function (value, index, values) {
                  return "$" + number_format(value);
                },
              },
              gridLines: {
                color: "rgb(234, 236, 244)",
                zeroLineColor: "rgb(234, 236, 244)",
                drawBorder: false,
                borderDash: [2],
                zeroLineBorderDash: [2],
              },
            },
          ],
        },
        legend: {
          display: false,
        },
        tooltips: {
          backgroundColor: "rgb(255,255,255)",
          bodyFontColor: "#858796",
          titleMarginBottom: 10,
          titleFontColor: "#6e707e",
          titleFontSize: 14,
          borderColor: "#dddfeb",
          borderWidth: 1,
          xPadding: 15,
          yPadding: 15,
          displayColors: false,
          intersect: false,
          mode: "index",
          caretPadding: 10,
          callbacks: {
            label: function (tooltipItem, chart) {
              var datasetLabel =
                chart.datasets[tooltipItem.datasetIndex].label || "";
              return datasetLabel + ": $" + number_format(tooltipItem.yLabel);
            },
          },
        },
      },
    });
  }
}
