from django.db import models
from apps.contact.enums import ProblemType
from apps.account.models import  SimpleUser



class Region(models.Model):
    name = models.CharField(max_length=100)


class District(models.Model):
    region = models.ForeignKey(Region, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)


class CategoryProblem(models.Model):
    title = models.CharField(max_length=50, verbose_name="Nomi")
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Communication(models.Model):
    user = models.ForeignKey(SimpleUser, on_delete=models.CASCADE)
    number_id = models.CharField(max_length=50,unique=True,blank=True)
    status = models.CharField(max_length=20, choices=ProblemType.choices(), default=ProblemType.prosess.value)
    category = models.ManyToManyField(CategoryProblem, verbose_name="category",related_name='category')
    district = models.ForeignKey(District, on_delete=models.PROTECT)
    long_cord = models.DecimalField(max_digits=10, decimal_places=7)
    lat_cord = models.DecimalField(max_digits=10, decimal_places=7)
    description = models.TextField(verbose_name='comment', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        com = Communication.objects.last()
        if com is not None:
            id_number = str(com.id + 1)
        else:
            id_number = str(1)
        nols = "0" * (7 - len(id_number)) + id_number
        self.number_id = f"{self.district.region.name[:1]}" + nols
        return super(Communication, self).save( *args, **kwargs)

    def str(self):
        return self.district.name


class CommunicationFile(models.Model):
    communication = models.ForeignKey(Communication, on_delete=models.CASCADE, related_name='comfiles')
    file = models.FileField(upload_to='communications')


# class Chat(models.Model):
#     communication = models.ForeignKey(Communication, on_delete=models.CASCADE, related_name='chat')
#     user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='chat_from')
#     is_user = models.BooleanField()
#     message = models.TextField()
#     file = models.FileField(upload_to='chatmedia')
#     is_read = models.BooleanField(default=False)
#     created_date = models.DateTimeField(auto_now_add=True)

#     def str(self):
#         return f'{self.is_user} {self.message[:30]}'


# class ChatModel(models.Model):
#     sender = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, related_name="Sender")
#     reciver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="Reciver")
#     message = models.CharField(max_length=221)
#     is_read = models.BooleanField(default=False)
#     date_created = models.DateTimeField(auto_now_add=True)

#     def __str__(self) -> str:
#         return f"sender {self.message}"
