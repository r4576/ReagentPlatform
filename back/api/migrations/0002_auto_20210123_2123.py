# Generated by Django 2.2.12 on 2021-01-23 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialsafetydata',
            name='NFPAFireNum',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='materialsafetydata',
            name='NFPAHealthNum',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='materialsafetydata',
            name='NFPAReactionNum',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='materialsafetydata',
            name='NFPASpecialNum',
            field=models.TextField(),
        ),
    ]
