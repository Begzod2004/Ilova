from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegionViewset,
    DistrictViewset,
    CategoryViewset,
    CommunicationViewSet,
)

router = DefaultRouter()
router.register('region', RegionViewset, 'region')
router.register('district', DistrictViewset, 'district')
router.register('category', CategoryViewset, 'category')
router.register('communication', CommunicationViewSet, 'communication')


urlpatterns = [
    path('', include(router.urls)),

    # path('chat/list/', ChatListView.as_view()),
    # path('chat/create/', ChatCreateView.as_view()),

]

