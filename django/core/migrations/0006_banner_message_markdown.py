# Generated by Django 2.2.10 on 2020-03-17 21:22

import core.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_add_banner_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='_banner_message_rendered',
            field=models.TextField(default='', editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='banner_message_markup_type',
            field=models.CharField(choices=[('', '--'), ('markdown', 'markdown'), ('html', 'html'), ('plain', 'plain'), ('', '')], default='markdown', max_length=30),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='banner_message',
            field=core.fields.MarkdownField(blank=True, help_text='Markdown-enabled banner notification displayed on the front page', rendered_field=True),
        ),
    ]