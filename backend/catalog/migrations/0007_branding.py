from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_remove_expert_media_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branding',
            fields=[
                ('id', models.PositiveSmallIntegerField(default=1, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(default='BAJAGHAR', max_length=120)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='branding/')),
                ('logo_alt', models.CharField(blank=True, default='BAJAGHAR logo', max_length=160)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Branding',
                'verbose_name_plural': 'Branding',
            },
        ),
    ]