# Generated by Django 4.0.2 on 2022-03-10 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collaboration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='collaborationrequests',
            name='country',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='collaborationrequests',
            name='deadline',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='collaborationrequests',
            name='organisation',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='collaborationrequests',
            name='pref_workplace',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='collaborationrequests',
            name='state',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='collaborationrequests',
            name='work_type',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
