# Generated by Django 5.1.2 on 2024-11-17 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_remove_department_classe_classe_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecturer',
            name='usersname',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.CharField(max_length=10),
        ),
    ]
