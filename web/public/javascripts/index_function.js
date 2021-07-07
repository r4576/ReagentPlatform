// Enter키 prevent
// $("form input").keydown(function (e) {
//   if (e.keyCode == 13) {
//     e.preventDefault();
//     makeBadge(takeSearchContent());
//   }
// });

// function makeIndex() {
//   var html_tag = document.getElementById("");
//   var html_tag_len = html_tag.innerHTML.length;
//   return html_tag_len % 9;
// }

// function makeBadge(content) {
//   if (content === false) {
//     alert("Please Input you  name!");
//   }

//   idx = makeIndex();
//   badge_list = [
//     '<span class="badge badge-primary">',
//     '<span class="badge badge-secondary">',
//     '<span class="badge badge-success">',
//     '<span class="badge badge-danger">',
//     '<span class="badge badge-warning">',
//     '<span class="badge badge-info">',
//     '<span class="badge badge-light">',
//     '<span class="badge badge-dark">',
//   ];
//   document.getElementById("").innerHTML =
//     document.getElementById("").innerHTML +
//     badge_list[idx] +
//     content +
//     "</span>";
// }
  $('#modalChart').on('shown.bs.modal',function(event){
      var link = $(event.relatedTarget);
      // get data source
      var source = link.attr('data-source').split(',');
      // get title
      var labels = ["1","2","3"];
      // Chart initialisieren
      var modal = $(this);
      var canvas = modal.find('#chart');
      var ctx = canvas[0];
      console.log((canvas));
      var chart = new Chart(ctx).Radar({        
          responsive: true,
          labels: labels,
          datasets: [{
              fillColor: "rgba(151,187,205,0.2)",
              strokeColor: "rgba(151,187,205,1)",
              pointColor: "rgba(151,187,205,1)",
              pointStrokeColor: "#fff",
              pointHighlightFill: "#fff",
              pointHighlightStroke: "rgba(151,187,205,1)",
              data: source
          }]
      },{});
  }).on('hidden.bs.modal',function(event){
      // reset canvas size
      var modal = $(this);
      var canvas = modal.find('#chart');
      canvas.attr('width','568px').attr('height','300px');
      alert("Material Safety를 꼭 확인하시길 바랍니다!");
      // destroy modal
      $(this).data('bs.modal', null);
  });