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

  // Scroll to top button appear
  $(document).on("scroll", function () {
    var scrollDistance = $(this).scrollTop();
    if (scrollDistance > 100) {
      $(".scroll-to-top").fadeIn();
    } else {
      $(".scroll-to-top").fadeOut();
    }
  });

  // Smooth scrolling using jQuery easing
  $(document).on("click", "a.scroll-to-top", function (e) {
    var $anchor = $(this);
    $("html, body")
      .stop()
      .animate(
        {
          scrollTop: $($anchor.attr("href")).offset().top,
        },
        1000,
        "easeInOutExpo"
      );
    e.preventDefault();
  });

  // page 로딩되면 자동으로 query 분석한 후, table 에 파싱
  $(document).ready(function () {
    let reagent = req.query.reagent;
    console.log("Test!!!");
    console.log(reagent);
    request(
      {
        method: "GET",
        uri: "http://127.0.0.1:8000/api/search?keyword=" + reagent,
      },
      function (error, response, body) {
        if (error) {
          throw error;
        } else {
          console.log("Receive Data !");
          // console.log(`Before Parsing Data ! : ${response.body}`);
          const allResultJson = JSON.parse(response.body);
          const allResult = [];
          for (let i = 0; i < allResultJson.length; i++) {
            let result = {
              reagentName: sample[i].Name,
              casNo: sample[i].ReagentProperty.casNo,
              formula: sample[i].ReagentProperty.formula,
              molecularWeight: sample[i].ReagentProperty.molecularWeight,
              meltingpoint: sample[i].ReagentProperty.meltingpoint,
              boilingpoint: sample[i].ReagentProperty.boilingpoint,
              density: sample[i].ReagentProperty.density,
              MaterialSafety: "Temporaily Empty!",
            };
            console.log("Parsing Success!!");
            allResult.push(result);
          }
          console.log(allResult);

          let newTBODY = document.getElementsByTagName("tbody");
          console.log("Tbody : ", newTBODY);
          console.log("Result : ", result);
          let newTD = "";
          for (let data in allResult) {
            for (let key in allResult[data]) {
              // console.log(allResult[i][j]);
              // console.log(`word : ${word}`);
              // newTD.append(allResult[i][j]);
              // console.log(typeof allResult[i][j]);
              console.log("Data : ", allResult[data][key]);
              // let word = document.createTextNode(allResult[data][key]);
              // newTD.innerText = allResult[i][j];
              // console.log("word : ", word);
              newTD += "<td>" + allResult[data][key] + "</td>";
            }
            console.log(newTD);
            // $("#tbody-insert").appendChild(newTR);
            newTD = "<tr>" + newTD + "</tr>";
            console.log(newTBODY);
          }
          newTBODY.innerHTML(newTD);
          console.log(newTBODY);
        }
      }
    );
  });
})(jQuery); // End of use strict
