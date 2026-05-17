from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_branding_split_contact_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='branding',
            name='contact_notification_emails',
        ),
    ]