from django.db import models

# Create your models here.


class UserInfo(models.Model):
    user = models.CharField(max_length=32)
    passwd = models.CharField(max_length=32)


class IpInfo(models.Model):
    ip = models.CharField(max_length=32)
    hostname = models.CharField(max_length=32)
    fn = models.CharField(max_length=32)
    user_id = models.ForeignKey(UserInfo)