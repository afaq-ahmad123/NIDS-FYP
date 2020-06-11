# Generated by Django 2.2.7 on 2020-01-01 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('name', models.CharField(max_length=99)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=99, unique=True)),
                ('password', models.CharField(max_length=99)),
                ('contact', models.CharField(max_length=29)),
            ],
        ),
    ]