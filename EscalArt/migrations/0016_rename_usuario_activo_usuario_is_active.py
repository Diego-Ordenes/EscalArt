# Generated by Django 4.0.3 on 2022-06-03 22:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EscalArt', '0015_chat_img_referencia'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuario',
            old_name='usuario_activo',
            new_name='is_active',
        ),
    ]
