# Generated by Django 3.0.5 on 2022-03-10 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_relationship'),
        ('chat', '0003_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='user_1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_1', to='profiles.Profile'),
        ),
        migrations.AlterField(
            model_name='chat',
            name='user_2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_2', to='profiles.Profile'),
        ),
        migrations.AlterField(
            model_name='message',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.Profile'),
        ),
    ]
