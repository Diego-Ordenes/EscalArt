# Generated by Django 4.0.3 on 2022-05-22 04:30

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('EscalArt', '0005_remove_perfil_seguidos_remove_perfil_seguidores_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicacion',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
