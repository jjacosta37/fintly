// Selecting active item in sidebar and writing topbar title

let dashitem = document.querySelectorAll(".nav-item")[1];
dashitem.className = "nav-item active";

let name = document.getElementById("topbarName");
name.innerHTML =
  '<h1 class="h5 mb-0 text-gray-800">Conectar Cuenta</h1> <button id="sidebarToggleTop" class="btn btn-link rounded-circle mr-3"> <i class="fas fa-plus-square fa-lg"></i></button>';

// Banking Institutions Map
// TODO: Got to change SVG links

const banks = {
  avvillas_co_retail: {
    display_name: "Banco AV Villas",
    logo: "https://statics.development.belvo.io/institutions/text_logos/avvillas_1.svg",
  },
  bancodebogota_co_retail: {
    display_name: "Banco de Bogotá",
    logo: "https://statics.development.belvo.io/institutions/text_logos/bancodebogota.svg",
  },
  bancodeoccidente_co_retail: {
    display_name: "Banco de Occidente",
    logo: "https://statics.development.belvo.io/institutions/text_logos/bancodeoccidente.svg",
  },
  bancofalabella_co_retail: {
    display_name: "Banco Falabella",
    logo: "https://statics.development.belvo.io/institutions/text_logos/bancofalabella.svg",
  },
  bancolombia_co_retail: {
    display_name: "Bancolombia",
    logo: "https://statics.development.belvo.io/institutions/text_logos/bancolombia.svg",
  },
  bbva_co_retail: {
    display_name: "BBVA Colombia",
    logo: "https://statics.development.belvo.io/institutions/text_logos/bbva.svg",
  },
  colpatria_co_retail: {
    display_name: "Scotiabank Colpatria",
    logo: "https://statics.development.belvo.io/institutions/text_logos/colpatria_text.svg",
  },
  davivienda_co_retail: {
    display_name: "Davivienda",
    logo: "https://statics.development.belvo.io/institutions/text_logos/davivienda.svg",
  },
};

// Drawing Balances Cards

function drawBalances() {
  fetch(urlPath + `getuserbalances/`, { method: "GET" })
    .then((response) => response.json())
    .then((data) => drawUserBalances(data))
    .catch((error) => console.error("Error:", error));
}

function drawUserBalances(data) {
  document.querySelector("#pagecontent").innerHTML = "";
  console.log(data);
  for (i in data) {
    console.log();
    buildCard(i, data[i][0][0]);
    // Hacer una funcion que pinte las tarjetas de credito/ahorros por card y meterla ca en un for var j in i.
    for (j in data[i]) {
      accountInfo = document.createElement("div");
      accountInfo.innerHTML = `                              <li class="text-s text-gray-900 list-group-item border-0" style="font-size:0.9em">
      <div class="row">
          <div class="col">${data[i][j][2]} - ${data[i][j][3]}</div>
          <div class="col text-right">$${Math.round(
            data[i][j][5]
          ).toLocaleString("en-US")}</div>
      </div>  
  </li>`;
      if (data[i][j][1] == "CREDIT_CARD") {
        accountList = document.querySelector(`#credit_list_${i}`);
        accountList.append(accountInfo);
      } else if (
        data[i][j][1] == "CHECKING_ACCOUNT" ||
        data[i][j][1] == "SAVINGS_ACCOUNT"
      ) {
        accountList = document.querySelector(`#savings_list_${i}`);
        accountList.append(accountInfo);
      }
    }
  }
}

function buildCard(id, bankname) {
  content = document.querySelector("#pagecontent");
  cardBody = document.createElement("div");
  cardBody.innerHTML = `<div class="row justify-content-center">

  <div class="col-md-10 mb-3 mx-3">
      <div class="card shadow">
          <a href="#collapseCardExample_${id}" class="d-block card-header collapsed align-top pt-0" data-toggle="collapse"
              role="button" aria-expanded="false" aria-controls="collapseCardExample_${id}" style="height: 60px;">

              <object class="align-top p-0" data="${banks[bankname]["logo"]}" height="60px">
              </object>
          </a>
          <div class="collapse" id="collapseCardExample_${id}" style="">
              <div class="card-body">
                  <div class="row no-gutters align-items-center">
                      <div class="col mr-2">
                          <ul class="list-group list-group-flush border-0">
                              <div class="" style="font-size:0.75em">
                                  CUENTAS DE AHORRO
                              </div>
                              <div id="savings_list_${id}">
                              </div>
                              <div class="pt-2 border-top pt-3" style="font-size:0.75em">
                                  TARJETAS DE CREDITO
                              </div>
                              <div id="credit_list_${id}">
                              </div>
                          </ul>
                      </div>
                  </div>
              </div>
          </div>
      </div>
  </div>

</div>`;
  content.appendChild(cardBody);
}

document.addEventListener("DOMContentLoaded", drawBalances());
