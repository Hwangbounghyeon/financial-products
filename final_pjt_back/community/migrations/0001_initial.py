# Generated by Django 4.2.8 on 2024-05-22 10:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('key', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('like', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Community',
            fields=[
                ('key', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('content', models.CharField(max_length=255)),
                ('like', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CommunityReport',
            fields=[
                ('key', models.AutoField(primary_key=True, serialize=False)),
                ('reported_at', models.DateTimeField(auto_now_add=True)),
                ('content', models.CharField(max_length=255)),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.community')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CommentReport',
            fields=[
                ('key', models.AutoField(primary_key=True, serialize=False)),
                ('reported_at', models.DateTimeField(auto_now_add=True)),
                ('content', models.CharField(max_length=255)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='community',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='community.community'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]