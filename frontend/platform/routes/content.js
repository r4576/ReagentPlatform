// request require
var express = require("express");
var router = express.Router();
var httpRequest = require("XMLHttpRequest");
var request = require("request");

function getReagent() {
  console.log("!!!!!!!!!!!!");
  var html_tag = document.getElementById("reagent");
  console.log(html_tag);
  var html_tag_value = html_tag.innerText;

  return html_tag_value;
}

router.get("/", function (req, res, next) {
  request(
    {
      method: "GET",
      uri: "http://127.0.0.1:8000/api/search?keyword=75-69-4",
    },
    function (error, response, body) {
      if (error) {
        throw error;
      }
      console.log(response.body);
    }
  );

  res.render("content/content", { title: "Express" });
});

module.exports = router;
