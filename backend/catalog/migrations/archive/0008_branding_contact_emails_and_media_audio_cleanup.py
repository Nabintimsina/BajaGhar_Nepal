from django.db import migrations, models


def remove_audio_media(apps, schema_editor):
    Media = apps.get_model('catalog', 'Media')
    Media.objects.filter(media_type='audio').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_branding'),
    ]

    operations = [
        migrations.AddField(
            model_name='branding',
            name='contact_emails',
            field=models.TextField(blank=True, default='info@bajanepal.com', help_text='Comma-separated email addresses that receive contact form notifications'),
        ),
        migrations.RunPython(remove_audio_media, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='media',
            name='media_type',
            field=models.CharField(choices=[('image', 'Image'), ('model_3d', '3D Model'), ('video', 'Video')], max_length=20),
        ),
    ]
