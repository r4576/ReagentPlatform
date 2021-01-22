from djongo import models


class MolecularData(models.Model):
    objects = models.DjongoManager()

    db_id = models.ObjectIdField(db_column='_id', primary_key=True)
    casNo = models.TextField()
    name = models.TextField()
    formula = models.TextField()

