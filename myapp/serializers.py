from myapp.models import Node, Reading
from rest_framework import serializers

class NodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Node
        fields = ('url', 'name')

class ReadingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reading
        fields = ('url', 'name')
