toggleSidebar();

function toggleSidebar() {
  if ($(window).width() < 960) {
    let sidebar = document.getElementById("sidebarJQ");
    sidebar.className =
      "navbar-nav bg-gradient-primary sidebar sidebar-dark accordion toggled";
    console.log("test");
  }
}

let card = document.getElementById("tutorialBody");
let btn = document.getElementById("tutorialBtn");
let title = document.querySelector("h5");

btn.addEventListener("click", function (e) {
  console.log(title.innerText);
  if (title.innerText == "Hola! Te damos la bienvenida a Fintly") {
    e.preventDefault();
    title.innerText = "Conectar cuenta";
    card.innerHTML =
      "<object class='align-self-center mb-4'data='/static/fintly_web/sync_image.svg' width='200'> </object><div class='text-dark'><p> Para comenzar deberas sincronizar tus cuentas con Fintly. Esto lo hacemos a traves de <b>Belvo</b>, que es una aplicacion que nos permite integrarnos de una manera segura a tus cuentas financieras.</p> <p> Belvo solo permite la lectura de datos. Nunca tendra acceso a tus credenciales ni podra realizar ninguna accion desde tu cuenta. Reconocidas empresas como Rappi ya estan utilizando Belvo para sincronizarse con sus usuarios. Si deseas conocer mas sobre Belvo, te invitamos a visitar el siguiente <a href='https://belvo.com/es/' target='_blank'>link</a>.</p></div>";
    btn.innerText = "Conectar cuenta";
  } else if (title.innerText == "Conectar cuenta") {
    e.preventDefault();
    title.innerText = "Y una ultima cosa...";
    card.innerHTML =
      "<object class='align-self-center mb-3'data='/static/fintly_web/party_image.svg' width='150'> </object><div class='text-dark'><p> Construimos Fintly con el animo de ayudarte a manejar tus finanzas personales. Estas usando la primera version beta que permite controlar gastos. En un futuro tenemos planeado otras funcionalidades como enviar dinero de manera facil, pagar facturas y hasta ayudarte a presentar tus impuestos! </p> <p> Si tienes cualquier idea de mejora de producto por favor envianos un correo a hola@fintly.com e intentaremos solucionarlo!</p> <p>Esperamos que Fintly te sea util y puedas empezar a llevar un mejor control de tus finanzas!</p></div>";
    btn.innerText = "Ahora si...conectar cuenta!";
  }
});
