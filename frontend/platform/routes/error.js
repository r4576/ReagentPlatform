var express = require("express");
var router = express.Router();

/* GET users listing. */
router.get("/", function (req, res, next) {
  res.render("error", { title: "Express" });
  console.log("load errors page!");
});

module.exports = router;
