# Generated by Django 4.2.7 on 2023-12-15 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wargameapi', '0003_alter_eventgamer_army_alter_eventgamer_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventgamer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gamer_events', to='wargameapi.wargameuser'),
        ),
    ]
