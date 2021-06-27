var atlas = require('./mongoAtlas')

var synonymField = {
  subName   : String,
  mainName  : String,
  casNo     : String
};

var synonymSchemaOption = {
  versionKey : false,
};

var synonymSchema = atlas.Schema(synonymField, synonymSchemaOption);
module.exports = atlas.model('Synonym', synonymSchema);