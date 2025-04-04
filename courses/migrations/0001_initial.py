# Generated by Django 4.2 on 2025-04-02 09:25

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tutors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=200)),
                ('coursecode', models.CharField(default='', max_length=200)),
                ('topic', models.CharField(choices=[('3D 列印基礎', '3D 列印基礎'), ('Steam 平台應用', 'Steam 平台應用'), ('蒸汽朋克設計', '蒸汽朋克設計'), ('高精度列印', '高精度列印'), ('逆向設計 ', '逆向設計'), ('金屬材料應用', '金屬材料應用'), ('硬件改造', '硬件改造'), ('機械結構', '機械結構'), ('醫療應用', '醫療應用'), ('場景設計', '場景設計')], default='', max_length=50)),
                ('description', models.TextField(blank=True)),
                ('studentreq', models.TextField(blank=True)),
                ('coursefee', models.IntegerField(default=0)),
                ('classsize', models.IntegerField(default=0)),
                ('durationhr', models.DecimalField(decimal_places=1, default=0.0, max_digits=2)),
                ('demo', models.URLField(default='https://example.com', max_length=500)),
                ('is_published', models.BooleanField(default=True)),
                ('list_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('photo_main', models.ImageField(upload_to='photos/%Y/%m/%d/')),
                ('photo_1', models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/')),
                ('photo_2', models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/')),
                ('photo_3', models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/')),
                ('photo_4', models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/')),
                ('photo_5', models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/')),
                ('photo_6', models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/')),
                ('tutor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='tutors.tutor')),
            ],
        ),
    ]
