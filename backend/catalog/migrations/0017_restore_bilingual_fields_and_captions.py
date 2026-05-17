from importlib import import_module

import django.core.validators
from django.db import migrations, models


def restore_bilingual_content(apps, schema_editor):
    seed_content = import_module('catalog.migrations.0003_seed_bilingual_content')
    seed_branding = import_module('catalog.migrations.0004_branding_bilingual_fields')
    seed_content.seed_bilingual_content(apps, schema_editor)
    seed_branding.seed_branding_translation(apps, schema_editor)


def reverse_restore_bilingual_content(apps, schema_editor):
    seed_content = import_module('catalog.migrations.0003_seed_bilingual_content')
    seed_branding = import_module('catalog.migrations.0004_branding_bilingual_fields')
    seed_content.reverse_seed_bilingual_content(apps, schema_editor)
    seed_branding.reverse_seed_branding_translation(apps, schema_editor)


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0016_remove_branding_logo_alt_ne_remove_branding_name_ne_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='branding',
            name='logo_alt_ne',
            field=models.CharField(blank=True, default='', max_length=160),
        ),
        migrations.AddField(
            model_name='branding',
            name='name_ne',
            field=models.CharField(blank=True, default='', max_length=120),
        ),
        migrations.AddField(
            model_name='category',
            name='description_ne',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='category',
            name='name_ne',
            field=models.CharField(blank=True, default='', max_length=120),
        ),
        migrations.AddField(
            model_name='expert',
            name='achievements_ne',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name='expert',
            name='bio_ne',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='expert',
            name='detailed_bio_ne',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='expert',
            name='expertise_ne',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
        migrations.AddField(
            model_name='expert',
            name='name_ne',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
        migrations.AddField(
            model_name='instrument',
            name='cultural_significance_ne',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='instrument',
            name='description_ne',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='instrument',
            name='history_ne',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='instrument',
            name='materials_ne',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='instrument',
            name='name_ne',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
        migrations.AddField(
            model_name='instrument',
            name='playing_technique_ne',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='instrument',
            name='region_ne',
            field=models.CharField(blank=True, default='', max_length=120),
        ),
        migrations.AddField(
            model_name='learningcontent',
            name='content_ne',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='learningcontent',
            name='title_ne',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='tutorial',
            name='caption_en',
            field=models.FileField(
                blank=True,
                help_text='English captions (VTT or SRT format). Optional for YouTube videos.',
                null=True,
                upload_to='tutorials/captions/',
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=['vtt', 'srt'],
                        message='Upload a valid caption file (VTT or SRT format)'
                    )
                ],
            ),
        ),
        migrations.AddField(
            model_name='tutorial',
            name='caption_ne',
            field=models.FileField(
                blank=True,
                help_text='Nepali captions (VTT or SRT format). Optional for YouTube videos.',
                null=True,
                upload_to='tutorials/captions/',
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=['vtt', 'srt'],
                        message='Upload a valid caption file (VTT or SRT format)'
                    )
                ],
            ),
        ),
        migrations.AddField(
            model_name='tutorial',
            name='description_ne',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='tutorial',
            name='instructor_name_ne',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
        migrations.AddField(
            model_name='tutorial',
            name='title_ne',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='tunerconfiguration',
            name='tuning_name_ne',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.RunPython(restore_bilingual_content, reverse_restore_bilingual_content),
    ]