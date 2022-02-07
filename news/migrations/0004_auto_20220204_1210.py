# Generated by Django 3.1.5 on 2022-02-04 12:10

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0003_auto_20220124_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentaries',
            name='date',
            field=models.DateTimeField(null=True, verbose_name=datetime.datetime(2022, 2, 4, 12, 10, 28, 175446)),
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='news',
            name='likes',
            field=models.ManyToManyField(to='news.Likes'),
        ),
    ]
