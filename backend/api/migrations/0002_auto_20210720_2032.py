# Generated by Django 3.2.5 on 2021-07-20 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quantity',
            old_name='quantity',
            new_name='amount',
        ),
        migrations.AlterField(
            model_name='quantity',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='api.recipe', verbose_name='Рецепт'),
        ),
    ]