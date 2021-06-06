// request require
var express = require("express");
var router = express.Router();
var httpRequest = require("XMLHttpRequest");
var request = require("request");

router.get("/", function (req, res, next) {
  let reagent = req.query.reagent;
  console.log(req.query);
  request(
    {
      method: "GET",
      // reagent : A,B,C 형태로 있어야함.
      uri: "http://127.0.0.1:8000/api/search?keyword=" + reagent,
    },
    function (error, response, body) {
      if (error) {
        throw error;
      } else {
        const allResult = [];
        console.log("Receive Data !");
        // console.log(`Before Parsing Data ! : ${response.body}`);
        const allResultJson = JSON.parse(response.body);
        for (let i = 0; i < allResultJson.length; i++) {
          let result = {
            reagentName: allResultJson[i].Name,
            casNo: allResultJson[i].ReagentProperty.casNo,
            formula: allResultJson[i].ReagentProperty.formula,
            molecularWeight: allResultJson[i].ReagentProperty.molecularWeight,
            meltingpoint: allResultJson[i].ReagentProperty.meltingpoint,
            boilingpoint: allResultJson[i].ReagentProperty.boilingpoint,
            density: allResultJson[i].ReagentProperty.density,
            MaterialSafety: allResultJson[i].MaterialSafety,
          };
          allResult.push(result);
        }
        console.log("Parsing Success!!");
        res.render("tables.ejs", { data: allResult });
      }
    }
  );
});

module.exports = router;
