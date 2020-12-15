# Generated by Django 3.1.4 on 2020-12-15 15:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('make', models.CharField(max_length=50)),
                ('model', models.CharField(max_length=50)),
                ('image', models.ImageField(default='defaultbike.jpeg', upload_to='images/bikepics')),
                ('fee', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Bikesize',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Biketype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Rider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=75)),
                ('city', models.CharField(max_length=50)),
                ('image', models.ImageField(default='default.jpeg', upload_to='images/profilePics')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cycleshareapi.state')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=500)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewauthor', to='cycleshareapi.rider')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewdperson', to='cycleshareapi.rider')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('bike', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cycleshareapi.bike')),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cycleshareapi.payment')),
                ('rider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cycleshareapi.rider')),
            ],
        ),
        migrations.CreateModel(
            name='Paymentjoin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cycleshareapi.payment')),
                ('rider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cycleshareapi.rider')),
            ],
        ),
        migrations.AddField(
            model_name='bike',
            name='bikesize',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cycleshareapi.bikesize'),
        ),
        migrations.AddField(
            model_name='bike',
            name='biketype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cycleshareapi.biketype'),
        ),
    ]