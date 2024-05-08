from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

class Hoods(models.Model):
    hood_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'hoods'

class Blocks(models.Model):
    block_id = models.AutoField(primary_key=True)
    hood = models.ForeignKey('Hoods', models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    center_latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    center_longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    radius = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'blocks'


class Follows(models.Model):
    follow_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    block = models.ForeignKey(Blocks, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'follows'

class Users(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    profile_description = models.TextField(blank=True, null=True)
    # profile_picture_url = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # 修改字段类型为 ImageField
    registration_date = models.DateTimeField(default=timezone.now)
    last_access_date = models.DateTimeField(default=timezone.now)

    # registration_date = models.DateTimeField(blank=True, null=True)
    # last_access_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True  # make sure magnaged by Django 
        db_table = 'users'

class Friendships(models.Model):
    friendship_id = models.AutoField(primary_key=True)
    user1 = models.ForeignKey('Users', models.DO_NOTHING, related_name='friendships_user1', blank=True, null=True)
    user2 = models.ForeignKey('Users', models.DO_NOTHING, related_name='friendships_user2', blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    creation_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'friendships'





class Locations(models.Model):
    location_id = models.AutoField(primary_key=True)
    address = models.TextField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'locations'


# class Memberships(models.Model):
#     membership_id = models.AutoField(primary_key=True)
#     user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
#     block = models.ForeignKey(Blocks, models.DO_NOTHING, blank=True, null=True)
#     join_date = models.DateTimeField(blank=True, null=True)
#     status = models.CharField(max_length=50, blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'memberships'

class Messages(models.Model):
    message_id = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    user = models.ForeignKey('Users', on_delete=models.CASCADE, blank=True, null=True)
    thread = models.ForeignKey('Threads', models.DO_NOTHING, related_name='messages', blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'messages'

class Recipients(models.Model):
    message = models.ForeignKey('Messages', models.DO_NOTHING, primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, null=True, blank=True)
    block = models.ForeignKey('Blocks', models.DO_NOTHING, null=True, blank=True)
    hood = models.ForeignKey('Hoods', models.DO_NOTHING, null=True, blank=True)
    neighbor = models.ForeignKey('Neighbors', models.DO_NOTHING, null=True, blank=True)
    class Meta:
        managed = True
        db_table = 'recipients'
        unique_together = (('message', 'user', 'block', 'hood','neighbor'),)

class Threads(models.Model):
    thread_id = models.AutoField(primary_key=True)
    topic = models.TextField(blank=True, null=True)
    initial_message = models.OneToOneField('Messages', on_delete=models.CASCADE, related_name='initial_message_of', blank=True, null=True)
    # created_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='created_by', blank=True, null=True)
    created_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'threads'

class Neighbors(models.Model):
    neighbor_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, related_name='neighbors_user', blank=True, null=True)
    neighbor_user = models.ForeignKey('Users', models.DO_NOTHING, related_name='neighbors_neighbor_user', blank=True, null=True)
    creation_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'neighbors'







class Userlocations(models.Model):
    user = models.OneToOneField('Users', models.DO_NOTHING, primary_key=True)
    location = models.ForeignKey(Locations, on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'userlocations'
        unique_together = (('user', 'location'),)


# class Users(models.Model):
#     user_id = models.AutoField(primary_key=True)
#     first_name = models.CharField(max_length=64, blank=True, null=True)
#     last_name = models.CharField(max_length=64, blank=True, null=True)
#     email = models.CharField(unique=True, max_length=255)
#     password = models.CharField(max_length=255)
#     profile_description = models.TextField(blank=True, null=True)
#     profile_picture_url = models.TextField(blank=True, null=True)
#     registration_date = models.DateTimeField(blank=True, null=True)
#     last_access_date = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'users'
