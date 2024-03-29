# Generated by Django 2.2.5 on 2019-09-10 20:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Burning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('town', models.CharField(choices=[('B', 'Bangladesh'), ('L', 'London'), ('D', 'Denmark')], default='B', max_length=1)),
                ('dragon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Dragon')),
            ],
        ),
    ]
