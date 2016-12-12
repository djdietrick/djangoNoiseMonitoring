from django.shortcuts import render
from myapp.models import *
from rest_framework import viewsets
from django.template import RequestContext
from myapp.serializers import *
import requests
import json
from django.views.generic import TemplateView
import datetime


def index(request):
    nodes = Node.objects.all()
    context = {'nodes':nodes}
    return render(request, 'myapp/index.html', context)

class NodeViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer

class ReadingViewSet(viewsets.ModelViewSet):
    queryset = Reading.objects.all()
    serializer_class = ReadingSerializer


