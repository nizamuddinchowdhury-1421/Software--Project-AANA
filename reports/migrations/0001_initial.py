

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):


    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('centers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProblemReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Brief description of the problem', max_length=200)),
                ('description', models.TextField(help_text='Detailed description of the problem')),
                ('problem_type', models.CharField(choices=[('engine', 'Engine Problem'), ('tire', 'Tire Issue'), ('battery', 'Battery Problem'), ('brake', 'Brake Issue'), ('electrical', 'Electrical Problem'), ('fuel', 'Fuel System'), ('other', 'Other')], default='other', max_length=20)),
                ('priority', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('urgent', 'Urgent')], default='medium', max_length=10)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('assigned', 'Assigned'), ('in_progress', 'In Progress'), ('resolved', 'Resolved'), ('closed', 'Closed')], default='pending', max_length=20)),
                ('location', models.CharField(help_text='Current location where the problem occurred', max_length=200)),
                ('latitude', models.FloatField(blank=True, help_text='GPS latitude', null=True)),
                ('longitude', models.FloatField(blank=True, help_text='GPS longitude', null=True)),
                ('phone_number', models.CharField(help_text='Contact number for assistance', max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('assigned_agent', models.ForeignKey(blank=True, limit_choices_to={'groups__name': 'Agents'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_reports', to=settings.AUTH_USER_MODEL)),
                ('assigned_center', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='centers.servicecenter')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='problem_reports', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ProblemResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(help_text='Response message to the user')),
                ('is_solution', models.BooleanField(default=False, help_text='Is this a solution to the problem?')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('problem_report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='reports.problemreport')),
                ('responder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='problem_responses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='ProblemPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(help_text='Upload photos of the problem', upload_to='problem_photos/%Y/%m/%d/')),
                ('description', models.CharField(blank=True, help_text='Optional description of this photo', max_length=200)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('problem_report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='reports.problemreport')),
            ],
            options={
                'ordering': ['uploaded_at'],
            },
        ),
    ]
