# Generated by Django 5.0.3 on 2024-03-20 19:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0003_alter_note_user_alter_note_venue'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Note',
        ),
    ]
