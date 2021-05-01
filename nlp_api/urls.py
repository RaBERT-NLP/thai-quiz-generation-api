from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'qacache', views.QACahceViewSet)
router.register(r'getqa', views.GetQA)

urlpatterns = [
  path('hello/', views.hello),
  path('questions_text/', views.get_quizzes_text),
  path('questions_url/', views.get_quizzes_url),
  path('', include(router.urls)),
  path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]