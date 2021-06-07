// request require
var express = require("express");
var router = express.Router();
var httpRequest = require("XMLHttpRequest");
var request = require("request");

// router.get("/", function (req, res, next) {
//   let reagent = req.query.reagent;
  // console.log(req.query);
  // request(
  //   {
  //     method: "GET",
  //     // reagent : A,B,C 형태로 있어야함.
  //     uri: "http://127.0.0.1:8000/api/search?keyword=" + reagent,
  //   },
    // function (error, response, body) {
    //   if (error) {
    //     throw error;
    //   } else {
    //     res.render("charts.ejs");
    //   }
    // }
  // );
// });

/* GET users listing. */
router.get("/", function (req, res, next) {
  res.render("charts", { title: "Express" });
});

module.exports = router;
