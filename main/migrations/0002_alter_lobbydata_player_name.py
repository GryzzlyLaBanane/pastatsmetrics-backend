# Generated by Django 5.0.6 on 2024-07-09 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lobbydata',
            name='player_name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
