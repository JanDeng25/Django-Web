# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 06:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('show', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=200)),
                ('upload_File', models.FileField(upload_to='./upload')),
                ('upload_date', models.DateTimeField(verbose_name='date uploaded')),
            ],
        ),
        migrations.RenameField(
            model_name='service',
            old_name='servicename',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='service',
            old_name='uploaddate',
            new_name='upload_date',
        ),
        migrations.AddField(
            model_name='file',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='show.Service'),
        ),
    ]
