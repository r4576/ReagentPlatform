from rest_meets_djongo.serializers import DjongoModelSerializer
from api.models import MolecularData


class MolecularSerializer(DjongoModelSerializer):
    class Meta:
        model = MolecularData
        fields = '__all__'

