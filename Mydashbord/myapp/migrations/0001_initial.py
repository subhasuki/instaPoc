# Generated by Django 3.1.7 on 2021-02-25 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Insta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=200, null=True)),
                ('pic1', models.CharField(max_length=200, null=True)),
                ('pic2', models.CharField(max_length=200, null=True)),
                ('pic3', models.CharField(max_length=200, null=True)),
                ('pic4', models.CharField(max_length=200, null=True)),
                ('pic5', models.CharField(max_length=200, null=True)),
                ('pic6', models.CharField(max_length=200, null=True)),
            ],
        ),
    ]
