# Generated by Django 5.1.2 on 2024-11-22 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myquizz', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizdetails1',
            name='title_quiz',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='quizdetails2',
            name='correct_option',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='quizdetails2',
            name='option1',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='quizdetails2',
            name='option2',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='quizdetails2',
            name='option3',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='quizdetails2',
            name='question',
            field=models.CharField(max_length=200),
        ),
    ]