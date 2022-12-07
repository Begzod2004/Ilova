from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

from apps.account.enums import UserRoles
from apps.account.managers import CustomUserManager, DirectorsManager, SimpleUserManager, StaffManager


class ForCheckModel(models.Model):
    phone_regex = RegexValidator(regex=r'^998[0-9]{2}[0-9]{7}$', message="Faqat o'zbek raqamlarigina tasdiqlanadi")
    phone = models.CharField(_('Telefon raqam'), validators=[phone_regex], max_length=17)
    code = models.CharField(max_length=5)


class Account(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^998[0-9]{2}[0-9]{7}$', message="Faqat o'zbek raqamlarigina tasdiqlanadi")

    phone = models.CharField(_('Telefon raqam'), validators=[phone_regex], max_length=17, unique=True)

    full_name = models.CharField(max_length=50, verbose_name='Full name', null=True)
    image = models.ImageField(upload_to='accounts/', verbose_name='Account image', null=True, blank=True)
    role = models.CharField(max_length=20, choices=UserRoles.choices(),default=UserRoles.simpleuser.value)
    activ_code = models.CharField(max_length=5, blank=True, null=True)
    date_modified = models.DateTimeField(auto_now=True, verbose_name='Date modified')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date created')

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        if self.full_name:
            return f'{self.full_name} ({self.phone})'
        return f'{self.phone}'

    def image_tag(self):
        if self.image:
            return mark_safe(f'<a href="{self.image.url}"><img src="{self.image.url}" style="height:40px;"/></a>')
        return 'no_image'

    @property
    def image_url(self):
        if self.image:
            if settings.DEBUG:
                return f'{settings.LOCAL_BASE_URL}{self.image.url}'
            return f'{settings.PROD_BASE_URL}{self.image.url}'
        else:
            return None

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return data


class Director(Account):
    objects = DirectorsManager()

    class Meta:
        proxy = True


class SimpleUser(Account):
    objects = SimpleUserManager()

    class Meta:
        proxy = True



class Staff(Account):
    objects = StaffManager()

    class Meta:
        proxy = True