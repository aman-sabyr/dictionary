from rest_framework import serializers
from .models import VerbForm


class VerbFormSerializer(serializers.ModelSerializer):

    class Meta:
        model = VerbForm
        fields = ['original', 'translation', 'is_regular', 'past_form', 'participle', 'level']