# Generated by Django 4.2.2 on 2023-06-23 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Capteur',
            fields=[
                ('nom', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('piece', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'capteur',
            },
        ),
        migrations.CreateModel(
            name='Donnee',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('heure', models.TimeField()),
                ('temperature', models.FloatField()),
                ('capteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mqttapp.capteur')),
            ],
            options={
                'db_table': 'donnee',
            },
        ),
    ]
