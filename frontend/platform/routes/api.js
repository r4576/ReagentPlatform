var express = require("express");
var request = require("request");
var router = express.Router();

/* GET users listing. */
// router.get("/api", function (req, res, next) {
//   res.render("search", { title: "Express" });
// });

var result = 0;

var __dirname = "api/search/?keyword=C3HH9N,H2O";

var geturl = "http://127.0.0.1:8000/" + __dirname + result;
request.get({ url: geturl });

module.exports = router;
