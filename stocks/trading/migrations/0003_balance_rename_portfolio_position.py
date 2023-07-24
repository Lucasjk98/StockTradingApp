# Generated by Django 4.2.3 on 2023-07-23 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0002_remove_portfolio_user_id_remove_transaction_user_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cash', models.IntegerField(default=500)),
            ],
        ),
        migrations.RenameModel(
            old_name='Portfolio',
            new_name='Position',
        ),
    ]