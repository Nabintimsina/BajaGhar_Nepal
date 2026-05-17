from django.db import migrations


def copy_instrument_fields_to_ne(apps, schema_editor):
    Instrument = apps.get_model('catalog', 'Instrument')

    fields = [
        ('history', 'history_ne'),
        ('materials', 'materials_ne'),
        ('playing_technique', 'playing_technique_ne'),
        ('cultural_significance', 'cultural_significance_ne'),
        ('description', 'description_ne'),
        ('name', 'name_ne'),
        ('region', 'region_ne'),
    ]

    instruments = Instrument.objects.all()
    for inst in instruments:
        updated = False
        for en_field, ne_field in fields:
            try:
                en_val = getattr(inst, en_field, None)
                ne_val = getattr(inst, ne_field, None)
            except Exception:
                en_val = None
                ne_val = None

            if (ne_val is None or ne_val == '') and (en_val not in (None, '')):
                setattr(inst, ne_field, en_val)
                updated = True

        if updated:
            inst.save(update_fields=[f for _, f in fields])


def reverse_copy(apps, schema_editor):
    # Don't attempt to reverse — leave Nepali fields untouched
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0019_add_show_tuner'),
    ]

    operations = [
        migrations.RunPython(copy_instrument_fields_to_ne, reverse_copy),
    ]
