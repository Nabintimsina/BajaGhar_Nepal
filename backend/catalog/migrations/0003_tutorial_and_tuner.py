# Generated migration for Tutorial and TunerConfiguration models

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tutorial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('video_url', models.URLField()),
                ('instructor_name', models.CharField(max_length=150)),
                ('duration', models.CharField(blank=True, help_text="e.g., '12:30'", max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('instrument', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tutorials', to='catalog.instrument')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='TunerConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tuning_name', models.CharField(default='Standard', max_length=100)),
                ('notes', models.JSONField(default=list, help_text="List of note names, e.g. ['E2', 'A2', 'D3', 'G3', 'B3', 'E4']")),
                ('frequencies', models.JSONField(default=list, help_text='List of frequencies in Hz, e.g. [82.41, 110.00, 146.83, 196.00, 246.94, 329.63]')),
                ('is_default', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('instrument', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tuner_config', to='catalog.instrument')),
            ],
            options={
                'ordering': ['-is_default', 'tuning_name'],
            },
        ),
    ]
