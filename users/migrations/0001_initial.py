# Generated by Django 4.1.7 on 2024-05-08 18:22

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('profile_description', models.TextField(blank=True, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pics/')),
                ('registration_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_access_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'users',
                'managed': True,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Blocks',
            fields=[
                ('block_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('center_latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('center_longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('radius', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'blocks',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Hoods',
            fields=[
                ('hood_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'hoods',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Locations',
            fields=[
                ('location_id', models.AutoField(primary_key=True, serialize=False)),
                ('address', models.TextField(blank=True, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
            ],
            options={
                'db_table': 'locations',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('message_id', models.AutoField(primary_key=True, serialize=False)),
                ('subject', models.CharField(blank=True, max_length=255, null=True)),
                ('body', models.TextField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(blank=True, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
            ],
            options={
                'db_table': 'messages',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Neighbors',
            fields=[
                ('neighbor_id', models.AutoField(primary_key=True, serialize=False)),
                ('creation_date', models.DateTimeField(blank=True, null=True)),
                ('neighbor_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='neighbors_neighbor_user', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='neighbors_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'neighbors',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Threads',
            fields=[
                ('thread_id', models.AutoField(primary_key=True, serialize=False)),
                ('topic', models.TextField(blank=True, null=True)),
                ('created_time', models.DateTimeField(blank=True, null=True)),
                ('initial_message', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='initial_message_of', to='users.messages')),
            ],
            options={
                'db_table': 'threads',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='messages',
            name='thread',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='messages', to='users.threads'),
        ),
        migrations.AddField(
            model_name='messages',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Friendships',
            fields=[
                ('friendship_id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
                ('creation_date', models.DateTimeField(blank=True, null=True)),
                ('user1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='friendships_user1', to=settings.AUTH_USER_MODEL)),
                ('user2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='friendships_user2', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'friendships',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Follows',
            fields=[
                ('follow_id', models.AutoField(primary_key=True, serialize=False)),
                ('block', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='users.blocks')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'follows',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='blocks',
            name='hood',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='users.hoods'),
        ),
        migrations.CreateModel(
            name='Recipients',
            fields=[
                ('recipient_id', models.AutoField(primary_key=True, serialize=False)),
                ('block', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='users.blocks')),
                ('hood', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='users.hoods')),
                ('message', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='users.messages')),
                ('neighbor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='users.neighbors')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'recipients',
                'managed': True,
                'unique_together': {('message', 'user', 'block', 'hood', 'neighbor')},
            },
        ),
        migrations.CreateModel(
            name='Userlocations',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='users.locations')),
            ],
            options={
                'db_table': 'userlocations',
                'managed': True,
                'unique_together': {('user', 'location')},
            },
        ),
    ]
