from rest_framework.serializers import ModelSerializer
from .models import Rent


class RentSerializer(ModelSerializer):
    class Meta:
        model = Rent
        fields = '__all__'
        depth = 2


