var express = require("express");
var router = express.Router();

/* GET users listing. */
router.get("/", function (req, res, next) {
  res.render("users", { title: "Express" });
  console.log("Success to connect Login Page!");
});

module.exports = router;
