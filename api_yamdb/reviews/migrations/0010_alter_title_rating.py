# Generated by Django 3.2 on 2023-02-25 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0009_alter_review_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='rating',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=3, null=True, verbose_name='Рейтинг произведения'),
        ),
    ]
