from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_tutorial_caption_en_tutorial_caption_ne'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='ip_address',
            field=models.GenericIPAddressField(blank=True, db_index=True, null=True),
        ),
    ]
