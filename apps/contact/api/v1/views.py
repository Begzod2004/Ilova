from django.conf import settings
from django.db.models import Q
from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render
import json
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions, generics
from apps.contact.models import Communication, Region, District, CategoryProblem
from .permissions import IsNotClient
from .serializers import RegionSerializer, DistrictSerializer, CategoryProblemSerializer, CommunicationSerializer, \
    CommunicationRetriveSerializer, CommunicationListSerializer
from ...enums import ProblemType


class RegionViewset(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = []


class DistrictViewset(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    permission_classes = []


class CategoryViewset(viewsets.ModelViewSet):
    queryset = CategoryProblem.objects.all()
    serializer_class = CategoryProblemSerializer
    permission_classes = []


class CommunicationViewSet(viewsets.ModelViewSet):
    queryset = Communication.objects.all()
    serializer_class = CommunicationSerializer
    # permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post', 'get']

    def get_serializer_class(self):
        serializer_dict = {
            'list': CommunicationListSerializer,
            'create': CommunicationSerializer,
            'retrieve': CommunicationRetriveSerializer,
        }
        return serializer_dict.get(self.action, self.serializer_class)

    @action(detail=True, methods=['post'], url_path='changestatus',
            permission_classes=[IsNotClient, permissions.IsAuthenticated])
    def changestatus(self, request, *args, **kwargs):
        comm = self.get_object()
        status = self.request.data.get('status')

        if status not in [i[0] for i in list(ProblemType.choices())]:
            return Response({"Xatolik!": "Status xato kiritildi"}, status=status.HTTP_400_BAD_REQUEST)

        comm.status = status
        comm.save()
        comm_serilizer = CommunicationRetriveSerializer(comm)
        return Response(comm_serilizer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        files = request.FILES.getlist('files', None)
        categories = request.data.get('category')
        data = request.data
        # data['user'] = request.user
        serializer = self.serializer_class(data=data, context={'files': files,'categories':categories})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ChatCreateView(generics.CreateAPIView):
#     queryset = ChatModel.objects.all()
#     serializer_class = ChatSerializer

    
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#     def perform_create(self, serializer):
#         serializer.save()


# class ChatListView(generics.ListAPIView):
#     queryset = ChatModel.objects.filter(is_read=False).order_by('-id')
#     serializer_class = ChatSerializer
#     permission_classes = (permissions.IsAuthenticated,)

#     def get_queryset(self):
#         qs = self.queryset.all()
#         qs = qs.filter(Q(sender_id=self.request.user.id) | Q(reciver_id=self.request.user.id))
#         return qs
    



