from djongo import models

# {
#     'cas_no': '75-31-0', 
#     'Name': 'iso-propylamine', 
#     'Formula': 'C3H9N', 
#     'Molecular Weight': '59.11', 
#     'Melting point': '-101 ℃', 
#     'Boiling point': '33 ℃', 
#     'Density': '0.69 g/cm3'
# }
class molecular_data(models.Model):
    cas_no = models.TextField()
    name = models.TextField()
    formula = models.TextField()
    molecular = models.TextField()
    meltingPoint = models.TextField()
    boilingPoint = models.TextField()
    density = models.TextField()
    
