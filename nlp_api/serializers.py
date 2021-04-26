# nlpapi/serializers.py
from rest_framework import serializers
from .models import QACahce
class QACahceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = QACahce
        fields = ('text', 'answer')