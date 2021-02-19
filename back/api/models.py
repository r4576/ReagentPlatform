from djongo import models


class Keyword(models.Model):
    objects = models.DjongoManager()

    id = models.ObjectIdField(db_column='_id', primary_key=True)
    keyword = models.TextField()
    casNo = models.TextField()


class ReagentPropertyData(models.Model):
    objects = models.DjongoManager()

    id = models.ObjectIdField(db_column='_id', primary_key=True)
    casNo = models.TextField()
    formula = models.TextField()
    molecularWeight = models.TextField()
    meltingpoint = models.TextField()
    boilingpoint = models.TextField()
    density = models.TextField()


class MaterialSafetyData(models.Model):
    objects = models.DjongoManager()

    id = models.ObjectIdField(db_column='_id', primary_key=True)
    casNo = models.TextField()
    phyStatus = models.TextField()
    phyColor = models.TextField()
    phySmell = models.TextField()
    phyTaste = models.TextField()
    NFPAHealthNum  = models.TextField()
    NFPAFireNum  = models.TextField()
    NFPAReactionNum  = models.TextField()
    NFPASpecialNum  = models.TextField()
    NFPAHealth = models.TextField()
    NFPAFire = models.TextField()
    NFPAReaction = models.TextField()
    NFPASpecial = models.TextField()
    safReaction = models.TextField()
    safCorrosion = models.TextField()
    safAvoid = models.TextField()
    humNormal = models.TextField()
    humInhale = models.TextField()
    humSkin = models.TextField()
    humEye = models.TextField()
    humMouth = models.TextField()
    humEtc = models.TextField()
    emeInhale = models.TextField()
    emeSkin = models.TextField()
    emeEye = models.TextField()
    emeMouth = models.TextField()
    emeEtc = models.TextField()
    accLeakage = models.TextField()
    accFire = models.TextField()
    treStorage = models.TextField()
    treTreatcaution = models.TextField()
    treDisposal = models.TextField()
    
