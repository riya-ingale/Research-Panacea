# Generated by Django 4.0.2 on 2022-03-10 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_rename_user_id_certification_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certification',
            name='user',
        ),
        migrations.RemoveField(
            model_name='education',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userresearch',
            name='research',
        ),
        migrations.RemoveField(
            model_name='userresearch',
            name='user',
        ),
        migrations.RemoveField(
            model_name='workexp',
            name='user',
        ),
        migrations.AddField(
            model_name='certification',
            name='user_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='education',
            name='user_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='userresearch',
            name='research_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='userresearch',
            name='user_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='workexp',
            name='user_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='saved',
            name='conference_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='saved',
            name='user_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='threads',
            name='research_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='threads',
            name='user_id',
            field=models.IntegerField(null=True),
        ),
    ]
