# Generated by Django 4.0.2 on 2022-03-13 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_researchpapers_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='github',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='linkedin',
            field=models.TextField(null=True),
        ),
    ]
