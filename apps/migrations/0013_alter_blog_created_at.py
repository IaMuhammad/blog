# Generated by Django 4.1.3 on 2022-12-10 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0012_rename_viewed_at_date_blogviewing_viewed_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
