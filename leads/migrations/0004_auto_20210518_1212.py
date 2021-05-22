# Generated by Django 3.0.7 on 2021-05-18 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0003_auto_20210516_1047'),
    ]

    operations = [
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zone', models.CharField(default='None', max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='leads',
            name='zone',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='leads.Zone'),
        ),
    ]
