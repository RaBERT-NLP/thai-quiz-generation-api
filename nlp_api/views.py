from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import viewsets
import hashlib

from .serializers import QACahceSerializer
from .models import QACahce
from .lib.qa import QAModel

import random

qa = QAModel()

# Create your views here.

class SuccessResponse(Response):
  def __init__(self, data=dict(), status=200, *args, **kwargs):
    data = {"success": True, "status_code": status, "data": data, "message": ""}
    super().__init__(data=data, status=status, *args, **kwargs)


class FailureResponse(Response):
  def __init__(self, data="", status=500, *args, **kwargs):
    data = {"success": False, "status_code": status, "data": "", "message": data}
    super().__init__(data=data, status=status, *args, **kwargs)

class QACahceViewSet(viewsets.ModelViewSet) :
  queryset = QACahce.objects.all().order_by('text')
  serializer_class = QACahceSerializer

class GetQA(viewsets.ModelViewSet) :
  queryset = QACahce.objects.all().order_by('text')
  # print("getqa")
  # print(queryset)
  serializer_class = QACahceSerializer

@api_view(["GET"])
def hello(request):
    return SuccessResponse("OK", status=200)

def get_cache_by_hash(text_hash) :
  try :
    cache = QACahce.objects.get(text_hash=text_hash)
    return True,cache
  except :
    return False,None

@api_view(["POST"])
def get_quizzes_text(request):
    try :
      data = JSONParser().parse(request)

      text = data['text'].strip()
      limit = int(data['limit'])

      data = qa.generate_quizzes_text(text, n_questions=limit)
      
      return SuccessResponse(data, status=200)

    except KeyError:
      return FailureResponse("[text] is missing in body.")     

    except:
      return FailureResponse("Can't generate question and answers from this article.")


@api_view(["POST"])
def get_quizzes_url(request):
    try :
      data = JSONParser().parse(request)

      url = data['url'].strip()
      limit = int(data['limit'])

      data = qa.generate_quizzes_url(url, n_questions=limit)
      
      return SuccessResponse(data, status=200)

    except KeyError:
      return FailureResponse("[text] is missing in body.")
    
    except:
      return FailureResponse("Can't generate question and answers from this article.")