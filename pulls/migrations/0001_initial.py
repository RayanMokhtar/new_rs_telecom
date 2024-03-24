# Generated by Django 4.2.2 on 2024-02-09 13:36

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mission',
            fields=[
                ('id_mission', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('start_mission', models.DateTimeField()),
                ('end_mission', models.DateTimeField()),
                ('client_mission', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id_user', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('users_name', models.CharField(max_length=255)),
                ('users_fname', models.CharField(max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('delete_date', models.DateTimeField(null=True)),
                ('update_date', models.DateTimeField(null=True)),
                ('users_phone', models.CharField(max_length=255, null=True)),
                ('users_company', models.CharField(max_length=255)),
                ('users_mail', models.CharField(max_length=50, unique=True)),
                ('users_type', models.CharField(max_length=255)),
                ('users_password', models.CharField(max_length=128)),
                ('users_region', models.CharField(max_length=255)),
                ('users_address', models.CharField(max_length=255)),
                ('users_postal', models.CharField(max_length=10, null=True)),
                ('users_is_active', models.BooleanField(default=True)),
                ('users_preavis', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
