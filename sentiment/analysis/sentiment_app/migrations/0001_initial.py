# Generated by Django 5.0.2 on 2025-01-30 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnalysisResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input_text', models.TextField()),
                ('positive_percent', models.FloatField(default=0.0)),
                ('negative_percent', models.FloatField(default=0.0)),
                ('neutral_percent', models.FloatField(default=0.0)),
                ('analysis_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
