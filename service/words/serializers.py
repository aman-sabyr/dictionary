from typing import Union

from rest_framework import serializers
from .models import VerbForm
from .services_folder.find_verb import WebParser


class VerbFormSerializer(serializers.ModelSerializer):

    class Meta:
        model = VerbForm
        fields = '__all__'


class CreateVerbFormsSerializer(serializers.Serializer):
    verb = serializers.CharField()

    def getTag(self, verb) -> Union[bool, tuple]:
        """
        receives verb (class str)
        creates web parser, saves html page locally and tries to find necessary tags
        if not returns False
        is true return tuple of two tags, you can see them in class WebParser
        :param verb:
        :return:
        """
        wp = WebParser()
        response = wp.createRequest(verb)
        wp.savePage(response)
        tag = wp.getTag()
        return tag

    def validate(self, attrs) -> tuple:
        """
        receives a word and calls getTag function
        checks if received parameter is tuple
        if not raises an Error
        if it is returns this tuple
        :param attrs:
        :return:
        """
        verb = attrs.get('verb')
        tag = self.getTag(verb)
        if not tag:
            raise serializers.ValidationError('there is no verb like that')
        return tag

    def create(self, validated_data) -> VerbForm:
        """
        receives tuple of tags
        calls static method from class handleTag, which returns finished dictionary
        :param validated_data:
        :return:
        """
        result = WebParser.handleTag(validated_data)
        verbForm = VerbForm.objects.create(**result)
        return verbForm

