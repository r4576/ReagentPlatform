from api.models import molecular_data
from rest_meets_djongo.serializers import DjongoModelSerializer


class MolecularSerializer(DjongoModelSerializer):
    class Meta:
        model = molecular_data
        fields = '__all__'

