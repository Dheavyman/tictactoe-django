# Generated by Django 2.1.1 on 2018-09-10 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameplay', '0003_auto_20180906_1955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='move',
            name='by_first_player',
            field=models.BooleanField(editable=False),
        ),
    ]