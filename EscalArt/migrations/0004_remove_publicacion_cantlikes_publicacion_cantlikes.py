# Generated by Django 4.0.3 on 2022-05-19 03:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EscalArt', '0003_remove_guardado_id_guardado_idguardado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publicacion',
            name='cantLikes',
        ),
        migrations.AddField(
            model_name='publicacion',
            name='cantLikes',
            field=models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL, verbose_name='likes'),
        ),
    ]
