var atlas = require('./mongoAtlas')

var reagentField = {
    casNo           : String,
    formula         : String,
    molecularWeight : String,
    meltingpoint    : String,
    boilingpoint    : String,
    density         : String
};
var reagentSchemaOption = {
    versionKey : false,
};

var reagentSchema = atlas.Schema(reagentField, reagentSchemaOption);
module.exports = atlas.model('ReagentProperty', reagentSchema);