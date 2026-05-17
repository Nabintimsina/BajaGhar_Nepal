from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_squashed_0014_instrument_model_3d_delete_media'),
    ]

    operations = [
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
    ]
