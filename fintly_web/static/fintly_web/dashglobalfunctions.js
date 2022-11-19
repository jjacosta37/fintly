(function ($) {
  "use strict"; // Start of use strict

  // Toggle the side navigation
  $("#sidebarToggle, #sidebarToggleTop").on("click", function (e) {
    $("body").toggleClass("sidebar-toggled");
    $(".sidebar").toggleClass("toggled");
    if ($(".sidebar").hasClass("toggled")) {
      $(".sidebar .collapse").collapse("hide");
    }
  });

  // Close any open menu accordions when window is resized below 768px
  $(window).resize(function () {
    if ($(window).width() < 768) {
      $(".sidebar .collapse").collapse("hide");
    }

    // Toggle the side navigation when window is resized below 480px
    if ($(window).width() < 480 && !$(".sidebar").hasClass("toggled")) {
      $("body").addClass("sidebar-toggled");
      $(".sidebar").addClass("toggled");
      $(".sidebar .collapse").collapse("hide");
    }
  });

  // Prevent the content wrapper from scrolling when the fixed side navigation hovered over
  $("body.fixed-nav .sidebar").on(
    "mousewheel DOMMouseScroll wheel",
    function (e) {
      if ($(window).width() > 768) {
        var e0 = e.originalEvent,
          delta = e0.wheelDelta || -e0.detail;
        this.scrollTop += (delta < 0 ? 1 : -1) * 30;
        e.preventDefault();
      }
    }
  );
})(jQuery); // End of use strict

toggleSidebar();

function toggleSidebar() {
  if ($(window).width() < 960) {
    let sidebar = document.getElementById("sidebarJQ");
    sidebar.className =
      "navbar-nav bg-gradient-primary sidebar sidebar-dark accordion toggled";
    console.log("test");
  }
}

// Print user name in navbar

function printUsername() {
  let username = document.getElementById("username");
  fetch(urlPath + `getusername/`, { method: "GET" })
    .then((response) => response.json())
    .then((data) => (username.innerText = data))
    .catch((error) => console.error("Error:", error));
}

printUsername();
