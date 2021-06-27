var express = require('express');

// MongoDB setting

var synonym = require('../models/synonym');
var reagent = require('../models/reagentproperty')
var safety = require('../models/materialsafety')

// Router setting

var router = express.Router();

router.post('/synonym', function(req, res, next) {
  res.sendStatus(200);

  var newSynonyms = req.body['synonyms'];
  
  if(!newSynonyms.includes(req.body['name']))
    newSynonyms.push(req.body['name']);

  newSynonyms.forEach(newSubName => {
    synonym.findOne({subName:newSubName}, function(err, result){
      if(result != null) return;
      
      var newSynonym = {
        subName : newSubName,
        mainName : req.body['name'],
        casNo : req.body['casNo']
      };
      synonym.create(newSynonym);
      console.log("[  Synonyms Data  ] " + newSubName + " added")
    });
  });
});

router.post('/reagent', function(req, res, next) {
  res.sendStatus(200);

  reagent.findOne({casNo : req.body['casNo'] }, function(err, result){
    if(result != null) return;
    reagent.create(req.body);
    console.log("[ ReagentProperty ] " + req.body['casNo'] + " added")
  });
});

module.exports = router;
