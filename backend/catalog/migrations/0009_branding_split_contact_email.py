from django.db import migrations, models


def copy_branding_emails(apps, schema_editor):
    Branding = apps.get_model('catalog', 'Branding')

    for branding in Branding.objects.all():
        legacy_emails = getattr(branding, 'contact_emails', '') or ''
        email_list = [email.strip() for email in legacy_emails.replace(';', ',').split(',') if email.strip()]

        if email_list:
            branding.contact_email = email_list[0]
            branding.contact_notification_emails = ','.join(email_list)
        else:
            branding.contact_email = 'info@bajanepal.com'
            branding.contact_notification_emails = 'admin@bajanepal.com,nabin@bajanepal.com'

        branding.save(update_fields=['contact_email', 'contact_notification_emails'])


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_branding_contact_emails_and_media_audio_cleanup'),
    ]

    operations = [
        migrations.AddField(
            model_name='branding',
            name='contact_email',
            field=models.EmailField(blank=True, default='info@bajanepal.com', help_text='Single public email shown in the footer and contact area', max_length=254),
        ),
        migrations.AddField(
            model_name='branding',
            name='contact_notification_emails',
            field=models.TextField(blank=True, default='admin@bajanepal.com,nabin@bajanepal.com', help_text='Comma-separated email addresses that receive contact form notifications'),
        ),
        migrations.RunPython(copy_branding_emails, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='branding',
            name='contact_emails',
        ),
    ]