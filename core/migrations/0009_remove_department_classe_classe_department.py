# Generated by Django 5.1.2 on 2024-11-14 13:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_department_creationdate_mark_creationdate_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='classe',
        ),
        migrations.AddField(
            model_name='classe',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.department'),
        ),
    ]
