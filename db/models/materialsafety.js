var atlas = require('./mongoAtlas')

var safetyField = {
    casNo           : String,
    phyStatus       : String,
    phyColor        : String,
    phySmell        : String,
    phyTaste        : String,
    NFPAHealthNum   : String,
    NFPAFireNum     : String,
    NFPAReactionNum : String,
    NFPASpecialNum  : String,
    NFPAHealth      : String,
    NFPAFire        : String,
    NFPAReaction    : String,
    NFPASpecial     : String,
    safReaction     : String,
    safCorrosion    : String,
    safAvoid        : String,
    humNormal       : String,
    humInhale       : String,
    humSkin         : String,
    humEye          : String,
    humMouth        : String,
    humEtc          : String,
    emeInhale       : String,
    emeSkin         : String,
    emeEye          : String,
    emeMouth        : String,
    emeEtc          : String,
    accLeakage      : String,
    accFire         : String,
    treStorage      : String,
    treTreatcaution : String,
    treDisposal     : String
};
var safetySchemaOption = {
    versionKey : false,
};

var safetySchema = atlas.Schema(safetyField, safetySchemaOption);
module.exports = atlas.model('MaterialSafety', safetySchema);