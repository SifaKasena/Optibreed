from rest_framework import serializers
from .models import Condition


class ConditionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Condition model.
    """
    class Meta:
        model = Condition
        fields = '__all__'
