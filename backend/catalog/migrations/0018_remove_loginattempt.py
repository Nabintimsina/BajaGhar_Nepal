from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0017_restore_bilingual_fields_and_captions'),
    ]

    operations = [
        migrations.DeleteModel(
            name='LoginAttempt',
        ),
    ]
