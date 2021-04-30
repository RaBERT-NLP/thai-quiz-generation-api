from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'qacache', views.QACahceViewSet)
router.register(r'getqa', views.GetQA)

urlpatterns = [
  path('hello/', views.hello),
  path('question/', views.get_question),
  path('questions_wiki/', views.get_questions_wiki),
  path('', include(router.urls)),
  path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]