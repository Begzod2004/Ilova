from rest_framework import serializers
from apps.contact.models import Communication, CategoryProblem, Region, District, CommunicationFile
from django.db import transaction



class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'


class CategoryProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryProblem
        fields = '__all__'


class CommunicationSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        categories = self.context.get('categories')
        for i in categories:
            cat = CategoryProblem.objects.get(id=i)
            if cat is None:
                raise serializers.ValidationError({'Error':f'{i} is invalid pk for category'})
        return attrs

    def create(self, validated_data):
        files = self.context['files']
        categories = self.context['categories']
        with transaction.atomic():
            comm = Communication.objects.create(**validated_data)
            for cat in categories:
                category = CategoryProblem.objects.get(pk=cat)
                comm.category.add(category)

            for document in files:
                CommunicationFile.objects.create(communication=comm,
                                             file=document)
        return comm

    class Meta:
        model = Communication
        fields = (
            'user',
            'district',
            'long_cord',
            'lat_cord',
            'description',
            'date_created',
        )


class ComFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunicationFile
        fields = '__all__'


class CommunicationRetriveSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        comfiles = instance.comfiles.all()
        comfile_ser = ComFileSerializer(comfiles, many=True)
        representation['files'] = comfile_ser.data
        return representation

    class Meta:
        model = Communication
        fields = '__all__'


class CommunicationListSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        comfile = instance.comfiles.first()
        comfile_ser = ComFileSerializer(comfile)
        representation['file'] = comfile_ser.data
        return representation

    class Meta:
        model = Communication
        fields = '__all__'


# class ChatSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ChatModel
#         fields = ('id', "sender", "reciver", "message", "is_read", "date_created")
        


