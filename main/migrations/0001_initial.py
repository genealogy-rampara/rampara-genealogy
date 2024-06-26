# Generated by Django 4.2.13 on 2024-05-24 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('dob', models.DateField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='SpouseInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spouse_name', models.CharField(max_length=100)),
                ('spouse_fathername', models.CharField(max_length=100)),
                ('spouse_village', models.CharField(max_length=100)),
                ('person', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='spouse_info', to='main.person')),
            ],
        ),
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('children', models.ManyToManyField(related_name='children_of', to='main.person')),
                ('father', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='father_of', to='main.person')),
                ('mother', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mother_of', to='main.person')),
            ],
        ),
    ]
