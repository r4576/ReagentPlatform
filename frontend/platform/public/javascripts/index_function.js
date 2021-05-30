// Enter키 prevent
$("form input").keydown(function (e) {
  if (e.keyCode == 13) {
    e.preventDefault();
    makeBadge(takeSearchContent());
  }
});

function makeIndex() {
  var html_tag = document.getElementById("reagent");
  var html_tag_len = html_tag.innerHTML.length;
  return html_tag_len % 9;
}

function makeBadge(content) {
  if (content === false) {
    alert("Please Input you reagent name!");
  }

  idx = makeIndex();
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

function submit_empty_click() {
  alert("값을 입력해주세요!");
}
