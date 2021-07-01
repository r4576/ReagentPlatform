var dateFormat = require("dateformat");

var path = require('path');
var baseDir = path.dirname(__dirname);

var keyFile = path.join(path.join(baseDir, 'keys'), 'db_settings.json');
var dbKey = require(keyFile);

var mongoose = require('mongoose');
mongoose.connect(dbKey['ChemData']['host'], {
  useNewUrlParser: true,
  useUnifiedTopology: true, 
}).then(() => {
    var now = new Date();
    console.log("[" + dateFormat(now, "dd/mmm/yyyy HH:MM:ss") + "] Connect to Mongo DB Atlas");
}).catch((err) => {
    var now = new Date();
    console.log("[" + dateFormat(now, "dd/mmm/yyyy HH:MM:ss") + "] Connect to Mongo DB Atlas Failed...");
    console.log(err);
});

module.exports = mongoose;