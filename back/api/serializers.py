from rest_meets_djongo.serializers import DjongoModelSerializer
from api.models import MaterialSafetyData, ReagentPropertyData


class ReagentPropertyDataSerializer(DjongoModelSerializer):
    class Meta:
        model = ReagentPropertyData
        fields = '__all__'


class MaterialSafetyDataSerializer(DjongoModelSerializer):
    class Meta:
        model = MaterialSafetyData
        fields = '__all__'
