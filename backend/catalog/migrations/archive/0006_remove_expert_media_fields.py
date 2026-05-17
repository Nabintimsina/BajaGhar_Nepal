from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_instrument_show_brightness_control'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expert',
            name='performance_video',
        ),
        migrations.RemoveField(
            model_name='expert',
            name='teaching_audio',
        ),
    ]
