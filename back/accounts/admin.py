from django.contrib import admin
from accounts.models import UserHistory
from api.models import MaterialSafetyData, ReagentPropertyData, Synonym
# Register your models here.

admin.site.register(UserHistory)

admin.site.register(ReagentPropertyData)
admin.site.register(Synonym)
admin.site.register(MaterialSafetyData)
