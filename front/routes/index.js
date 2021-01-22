// import "node_modules/bootswatch/dist/[theme]/bootstrap.min.css";
var express = require("express");
var router = express.Router();

/* GET home page. */
router.get("/", function (req, res, next) {
  res.render("index", { title: "Express" });
});

module.exports = router;
