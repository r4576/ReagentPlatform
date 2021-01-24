// Enter키 prevent
// $("form input").keydown(function (e) {
//   if (e.keyCode == 13) {
//     e.preventDefault();
//     return false;
//   }
// });

function makeRandom() {
  var random_num = Math.random();
  console.log(Math.floor(random_num * 10));
  return Math.floor(random_num * 10);
}

function makeBadge(content) {
  if (content === false) {
    alert("Please Input you reagent name!");
  }

  idx = makeRandom();
  badge_list = [
    '<span class="badge badge-primary">',
    '<span class="badge badge-secondary">',
    '<span class="badge badge-success">',
    '<span class="badge badge-danger">',
    '<span class="badge badge-warning">',
    '<span class="badge badge-info">',
    '<span class="badge badge-light">',
    '<span class="badge badge-dark">',
  ];
  document.getElementById("reagent").innerHTML =
    document.getElementById("reagent").innerHTML +
    badge_list[idx] +
    content +
    "</span>";
}

function takeSearchContent() {
  var value = $(".form-control").val();

  return value;
}
