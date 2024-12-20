# Generated by Django 5.1.2 on 2024-11-03 10:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=255)),
                ('lastname', models.CharField(max_length=255)),
                ('gender', models.CharField(max_length=1)),
                ('creationdate', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Classe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classcode', models.CharField(max_length=10)),
                ('classname', models.CharField(max_length=255)),
                ('level', models.IntegerField()),
                ('speciality', models.CharField(max_length=255)),
                ('creationdate', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.administrator')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departmentcode', models.CharField(max_length=20)),
                ('departmentname', models.CharField(max_length=255)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.administrator')),
            ],
        ),
        migrations.CreateModel(
            name='Lecturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=255)),
                ('lastname', models.CharField(max_length=255)),
                ('gender', models.CharField(max_length=1)),
                ('dateofbirth', models.DateField()),
                ('email', models.EmailField(max_length=254)),
                ('creationdate', models.DateTimeField(auto_now=True)),
                ('address', models.CharField(default='Logbaba', max_length=200)),
                ('phonenumber', models.IntegerField(default=677285764)),
                ('picture', models.ImageField(default='teacher.png', upload_to='lecturer_pictures')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.administrator')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.department')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coursecode', models.CharField(max_length=10)),
                ('coursetitle', models.CharField(max_length=255)),
                ('credits', models.IntegerField()),
                ('semester', models.CharField(choices=[('semester 1', 'semester 1'), ('semester 2', 'semester 2'), ('semester 3', 'semester 3'), ('semester 4', 'semester 4'), ('semester 5', 'semester 5'), ('semester 6', 'semester 6'), ('semester 7', 'semester 7'), ('semester 8', 'semester 8'), ('semester 9', 'semester 9'), ('semester 10', 'semester 10'), ('semester 11', 'semester 11'), ('semester 12', 'semester 12'), ('semester 13', 'semester 13'), ('semester 14', 'semester 14')], default='semester 1', max_length=25)),
                ('creationdate', models.DateField(auto_now=True)),
                ('classe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.classe')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.administrator')),
                ('lecturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.lecturer')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=255)),
                ('lastname', models.CharField(max_length=255)),
                ('usersname', models.CharField(max_length=255)),
                ('gender', models.CharField(max_length=1)),
                ('dateofbirth', models.DateField()),
                ('address', models.CharField(default='Bepanda', max_length=200)),
                ('phonenumber', models.CharField(default='+237677285763', max_length=20)),
                ('picture', models.ImageField(default='teacher.png', upload_to='students/')),
                ('parentemail', models.EmailField(max_length=254)),
                ('creationdate', models.DateTimeField(auto_now=True)),
                ('classe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.classe')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.administrator')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Marks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.IntegerField()),
                ('grade', models.CharField(choices=[('A+', 'A+'), ('A', 'A'), ('A-', 'A-'), ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'), ('C+', 'C+'), ('C', 'C'), ('C-', 'C-'), ('D', 'D'), ('E', 'E'), ('F', 'F')], default='A+', max_length=10)),
                ('semester', models.CharField(max_length=25)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.course')),
                ('lecturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.lecturer')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.student')),
            ],
        ),
    ]
