from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0020_copy_instrument_fields_to_ne'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tunerconfiguration',
            name='instrument',
            field=models.ForeignKey(on_delete=models.CASCADE, related_name='tuner_configs', to='catalog.instrument'),
        ),
    ]
