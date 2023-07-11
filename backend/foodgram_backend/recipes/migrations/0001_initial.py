# Generated by Django 4.2.3 on 2023-07-10 11:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tags', '0002_alter_tag_options_alter_tag_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('image', models.ImageField(default=None, null=True, upload_to='cats/images/')),
                ('description', models.TextField(verbose_name='Description')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('tags', models.ManyToManyField(to='tags.tag', verbose_name='Теги')),
            ],
        ),
    ]
