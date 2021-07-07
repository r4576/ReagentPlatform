var express = require("express");
var router = express.Router();
var request = require("request");

var path = require("path");
var baseDir = path.dirname(__dirname);
var networkFile = path.join(path.join(baseDir, 'keys'), 'networks.json');
var network = require(networkFile);

router.get("/", function (req, res, next) {
  let reagent = req.query.reagent;
  request({
      method: "GET",
      uri: network['apiServer']['URL'] + ":" + network['apiServer']['Port'] + "/api/search?keyword=" + reagent,
    },function (error, response, body) {
      if (error) {
        throw error;
      } else {
        const data = [];
        const apiResponse = JSON.parse(response.body);
        for (let i = 0; i < apiResponse.length; i++) {
          let result = {
            reagentName: apiResponse[i].Name,
            casNo: apiResponse[i].ReagentProperty.casNo,
            formula: apiResponse[i].ReagentProperty.formula,
            molecularWeight: apiResponse[i].ReagentProperty.molecularWeight,
            meltingpoint: apiResponse[i].ReagentProperty.meltingpoint,
            boilingpoint: apiResponse[i].ReagentProperty.boilingpoint,
            density: apiResponse[i].ReagentProperty.density,
            MaterialSafety: apiResponse[i].MaterialSafety,
          };
          data.push(result);
        }
        res.render("tables", { data: data });
      }
    }
  );
});

module.exports = router;
