# Generated by Django 5.1.3 on 2024-12-01 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='isbn',
            field=models.CharField(default='0000000000000', max_length=13, unique=True),
        ),
        migrations.DeleteModel(
            name='BorrowedBook',
        ),
    ]
