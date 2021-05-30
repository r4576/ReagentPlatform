window.onload = function () {
  let reagent = req.query.reagent;
  console.log("Test!!!");
  console.log(reagent);
  request(
    {
      method: "GET",
      uri: "http://127.0.0.1:8000/api/search?keyword=" + reagent,
    },
    function (error, response, body) {
      if (error) {
        throw error;
      } else {
        console.log("Receive Data !");
        // console.log(`Before Parsing Data ! : ${response.body}`);
        const allResultJson = JSON.parse(response.body);
        const allResult = [];
        for (let i = 0; i < allResultJson.length; i++) {
          let result = {
            reagentName: sample[i].Name,
            casNo: sample[i].ReagentProperty.casNo,
            formula: sample[i].ReagentProperty.formula,
            molecularWeight: sample[i].ReagentProperty.molecularWeight,
            meltingpoint: sample[i].ReagentProperty.meltingpoint,
            boilingpoint: sample[i].ReagentProperty.boilingpoint,
            density: sample[i].ReagentProperty.density,
            MaterialSafety: "Temporaily Empty!",
          };
          console.log("Parsing Success!!");
          allResult.push(result);
        }
        console.log(allResult);

        let newTBODY = document.getElementsByTagName("tbody");
        console.log("Tbody : ", newTBODY);
        console.log("Result : ", result);
        let newTD = "";
        for (let data in allResult) {
          for (let key in allResult[data]) {
            // console.log(allResult[i][j]);
            // console.log(`word : ${word}`);
            // newTD.append(allResult[i][j]);
            // console.log(typeof allResult[i][j]);
            console.log("Data : ", allResult[data][key]);
            // let word = document.createTextNode(allResult[data][key]);
            // newTD.innerText = allResult[i][j];
            // console.log("word : ", word);
            newTD += "<td>" + allResult[data][key] + "</td>";
          }
          console.log(newTD);
          // $("#tbody-insert").appendChild(newTR);
          newTD = "<tr>" + newTD + "</tr>";
          console.log(newTBODY);
        }
        newTBODY.innerHTML(newTD);
        console.log(newTBODY);
      }
    }
  );
};
