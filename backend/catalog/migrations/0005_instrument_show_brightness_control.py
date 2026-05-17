from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_alter_tutorial_optional_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='instrument',
            name='show_brightness_control',
            field=models.BooleanField(default=False),
        ),
    ]
