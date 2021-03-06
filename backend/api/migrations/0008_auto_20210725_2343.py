# Generated by Django 3.2.5 on 2021-07-25 16:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20210724_2103'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ('order', 'name'), 'verbose_name': 'Тег', 'verbose_name_plural': 'Теги'},
        ),
        migrations.AddField(
            model_name='tag',
            name='order',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Порядок вывода'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='quantity',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.ingredient', verbose_name='Ингредиент'),
        ),
    ]
