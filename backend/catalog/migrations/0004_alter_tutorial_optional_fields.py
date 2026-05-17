from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_tutorial_and_tuner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorial',
            name='duration',
            field=models.CharField(blank=True, default='', help_text="e.g., '12:30'", max_length=50),
        ),
        migrations.AlterField(
            model_name='tutorial',
            name='instructor_name',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
    ]