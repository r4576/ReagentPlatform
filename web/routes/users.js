var express = require("express");
var router = express.Router();

var path = require("path");
var baseDir = path.dirname(__dirname);
var networkFile = path.join(path.join(baseDir, 'keys'), 'networks.json');
var network = require(networkFile);

router.get("/", function (req, res, next) {
  res.render("users", { loginURL: {
    google: network['base']['URL'] + ":" + network['authServer']['Port'] + "/google/login",
    naver: network['base']['URL'] + ":" + network['authServer']['Port'] + "/naver/login",
    kakao: network['base']['URL'] + ":" + network['authServer']['Port'] + "/kakao/login"
  }});
});

module.exports = router;
