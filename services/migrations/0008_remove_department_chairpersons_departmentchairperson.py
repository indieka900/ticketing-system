# Generated by Django 5.0.9 on 2024-11-07 07:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0007_remove_department_chairperson_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='chairpersons',
        ),
        migrations.CreateModel(
            name='DepartmentChairperson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_assigned', models.DateField(auto_now_add=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chairs', to='services.department')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='chair_department', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'department')},
            },
        ),
    ]
