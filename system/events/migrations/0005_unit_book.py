# Generated by Django 4.1.3 on 2023-03-10 11:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_teacher_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='Book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='events.book'),
        ),
    ]
