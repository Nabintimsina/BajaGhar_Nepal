from django.db import migrations, models


def seed_branding_translation(apps, schema_editor):
    Branding = apps.get_model('catalog', 'Branding')
    Branding.objects.filter(pk=1).update(
        name_ne='बाजाघर',
        logo_alt_ne='बाजाघर लोगो',
    )


def reverse_seed_branding_translation(apps, schema_editor):
    Branding = apps.get_model('catalog', 'Branding')
    Branding.objects.filter(pk=1).update(
        name_ne='',
        logo_alt_ne='',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_seed_bilingual_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='branding',
            name='name_ne',
            field=models.CharField(blank=True, default='', max_length=120),
        ),
        migrations.AddField(
            model_name='branding',
            name='logo_alt_ne',
            field=models.CharField(blank=True, default='', max_length=160),
        ),
        migrations.RunPython(seed_branding_translation, reverse_seed_branding_translation),
    ]
