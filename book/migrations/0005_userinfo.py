# Generated by Django 2.0.4 on 2018-07-08 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_remove_login_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Userinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=32)),
                ('pwd', models.CharField(max_length=32)),
                ('tel', models.IntegerField()),
                ('e_mail', models.EmailField(max_length=254)),
            ],
        ),
    ]
