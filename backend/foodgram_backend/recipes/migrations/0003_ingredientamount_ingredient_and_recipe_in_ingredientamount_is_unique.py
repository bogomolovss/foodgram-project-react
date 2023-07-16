# Generated by Django 4.2.3 on 2023-07-13 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_alter_ingredientamount_recipe'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='ingredientamount',
            constraint=models.UniqueConstraint(fields=('ingredient', 'recipe'), name='Ingredient and Recipe in IngredientAmount is unique'),
        ),
    ]