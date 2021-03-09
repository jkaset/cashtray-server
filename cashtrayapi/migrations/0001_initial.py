# Generated by Django 3.1.7 on 2021-03-09 00:17

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
            name='Nonsmoker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quit_date', models.DateTimeField(auto_now_add=True)),
                ('cigs_per_day', models.IntegerField()),
                ('price_per_pack', models.FloatField()),
                ('cigs_per_pack', models.IntegerField()),
                ('start_smoking_year', models.DateField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reward_name', models.CharField(max_length=50)),
                ('reward_cost', models.FloatField()),
                ('redeemed', models.BooleanField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cashtrayapi.nonsmoker')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=500)),
                ('created_on', models.DateField()),
                ('commenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_commenting', to='cashtrayapi.nonsmoker')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cashtrayapi.nonsmoker')),
            ],
        ),
    ]
