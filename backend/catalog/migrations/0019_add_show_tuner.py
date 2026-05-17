from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0018_remove_loginattempt'),
    ]

    operations = [
        migrations.AddField(
            model_name='instrument',
            name='show_tuner',
            field=models.BooleanField(default=False, help_text='Show tuner/practice tool in the frontend instrument page'),
        ),
    ]
