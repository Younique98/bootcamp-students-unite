# Generated by Django 3.2.4 on 2021-06-09 20:43

import bootcampstudentsuniteapi.models.bootcamp_graduate
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BootCampGraduate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(max_length=50)),
                ('bootcamp_graduate_image', models.ImageField(blank=True, upload_to=bootcampstudentsuniteapi.models.bootcamp_graduate.upload_to)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CodingBootcampSchool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='GroupProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('number_of_graduates_signed_up', models.IntegerField()),
                ('description', models.CharField(max_length=150)),
                ('estimated_time_to_completion', models.CharField(max_length=50)),
                ('github_link', models.CharField(max_length=150)),
                ('project_manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bootcampstudentsuniteapi.bootcampgraduate')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('boot_camp_graduate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bootcampstudentsuniteapi.bootcampgraduate')),
                ('group_project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bootcampstudentsuniteapi.groupproject')),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bootcamp_graduate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bootcampstudentsuniteapi.bootcampgraduate')),
                ('group_project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bootcampstudentsuniteapi.groupproject')),
            ],
        ),
        migrations.CreateModel(
            name='JobBoard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=150)),
                ('job_link', models.CharField(max_length=150)),
                ('poster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bootcampstudentsuniteapi.bootcampgraduate')),
            ],
        ),
    ]
