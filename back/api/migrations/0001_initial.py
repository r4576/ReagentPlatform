# Generated by Django 2.2.12 on 2021-02-24 16:49

from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MaterialSafetyData',
            fields=[
                ('id', djongo.models.fields.ObjectIdField(auto_created=True, db_column='_id', primary_key=True, serialize=False)),
                ('casNo', models.TextField()),
                ('phyStatus', models.TextField()),
                ('phyColor', models.TextField()),
                ('phySmell', models.TextField()),
                ('phyTaste', models.TextField()),
                ('NFPAHealthNum', models.TextField()),
                ('NFPAFireNum', models.TextField()),
                ('NFPAReactionNum', models.TextField()),
                ('NFPASpecialNum', models.TextField()),
                ('NFPAHealth', models.TextField()),
                ('NFPAFire', models.TextField()),
                ('NFPAReaction', models.TextField()),
                ('NFPASpecial', models.TextField()),
                ('safReaction', models.TextField()),
                ('safCorrosion', models.TextField()),
                ('safAvoid', models.TextField()),
                ('humNormal', models.TextField()),
                ('humInhale', models.TextField()),
                ('humSkin', models.TextField()),
                ('humEye', models.TextField()),
                ('humMouth', models.TextField()),
                ('humEtc', models.TextField()),
                ('emeInhale', models.TextField()),
                ('emeSkin', models.TextField()),
                ('emeEye', models.TextField()),
                ('emeMouth', models.TextField()),
                ('emeEtc', models.TextField()),
                ('accLeakage', models.TextField()),
                ('accFire', models.TextField()),
                ('treStorage', models.TextField()),
                ('treTreatcaution', models.TextField()),
                ('treDisposal', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ReagentPropertyData',
            fields=[
                ('id', djongo.models.fields.ObjectIdField(auto_created=True, db_column='_id', primary_key=True, serialize=False)),
                ('casNo', models.TextField()),
                ('formula', models.TextField()),
                ('molecularWeight', models.TextField()),
                ('meltingpoint', models.TextField()),
                ('boilingpoint', models.TextField()),
                ('density', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Synonym',
            fields=[
                ('id', djongo.models.fields.ObjectIdField(auto_created=True, db_column='_id', primary_key=True, serialize=False)),
                ('subName', models.TextField()),
                ('mainName', models.TextField()),
                ('casNo', models.TextField()),
            ],
        ),
    ]
