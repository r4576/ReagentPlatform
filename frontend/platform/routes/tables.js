// request require
var express = require("express");
var router = express.Router();
var httpRequest = require("XMLHttpRequest");
var request = require("request");

// function printOneDictResult(varName, resultName) {
//   console.log(`VarName : ${varName}, resultName : ${resultName}`);
// }
// function printAllDictResult(result) {
//   for (let i in result) {
//     printOneDictResult(i, result[i]);
//   }
//   console.log("Trasfer Success!!");
// }

// function splitResult(sample) {
//   const allResult = [];
//   for (let i = 0; i < sample.length; i++) {
//     let result = {
//       reagentName: sample[i].Name,
//       casNo: sample[i].ReagentProperty.casNo,
//       formula: sample[i].ReagentProperty.formula,
//       molecularWeight: sample[i].ReagentProperty.molecularWeight,
//       meltingpoint: sample[i].ReagentProperty.meltingpoint,
//       boilingpoint: sample[i].ReagentProperty.boilingpoint,
//       density: sample[i].ReagentProperty.density,
//       MaterialSafety: "Temporaily Empty!",
//     };
//     console.log("Parsing Success!!");
//     printAllDictResult(result);

//     allResult.push(result);
//   }
//   // console.log(allResult);

//   return allResult;
// }

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
            MaterialSafety: "Temporaily Empty!",
          };
          allResult.push(result);
        }
        console.log("Parsing Success!!");
        console.log(`Before tranfer Result : `, allResult);
        res.render("tables.ejs", { data: allResult });
      }
    }
  );
  // res.render("tables", { title: "Express" });
});

/* GET home page. */
// router.get("/", (req, res, next) => {
//   let reagent = req.query.reagent;
//   console.log(req.query);
//   const allResult = [];
//   fetch("http://127.0.0.1:8000/api/search?keyword=" + reagent)
//     .then((data) => {
//       console.log(data);
//       data
//         .json()
//         .then((contents) => {
//           res.render("tables.ejs", { allResult: contents });
//         })
//         .catch((error) => {
//           console.log("\x1b[31m" + error.name + "\x1b[0m: " + error.message);
//           res.redirect("/");
//         });
//     })
//     .catch((error) => {
//       console.log(error);
//       res.render("tables.ejs", { allResult: allResult });
//     });
// });

module.exports = router;
