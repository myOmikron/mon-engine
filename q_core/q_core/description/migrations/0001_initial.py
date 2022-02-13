# Generated by Django 4.0.1 on 2022-02-10 22:25

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255, unique=True)),
                ('cmd', models.CharField(blank=True, default='', max_length=1024, null=True)),
                ('comment', models.CharField(blank=True, default='', max_length=1024, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255, unique=True)),
                ('mail', models.EmailField(blank=True, default='', max_length=255, null=True)),
                ('comment', models.CharField(blank=True, default='', max_length=1024, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContactGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255, unique=True)),
                ('comment', models.CharField(blank=True, default='', max_length=1024, null=True)),
                ('linked_contacts', models.ManyToManyField(blank=True, to='description.Contact')),
            ],
        ),
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=16, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DayTimePeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='description.day')),
            ],
        ),
        migrations.CreateModel(
            name='GlobalVariable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(blank=True, default='', max_length=1024, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('address', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('disabled', models.BooleanField(blank=True, default=False, null=True)),
                ('comment', models.CharField(blank=True, default='', max_length=1024, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(blank=True, default='', max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.CharField(default='', max_length=4, validators=[django.core.validators.RegexValidator('(([01][0-9]|2[0-3])[0-5][0-9]|2400)')])),
                ('stop_time', models.CharField(default='', max_length=4, validators=[django.core.validators.RegexValidator('(([01][0-9]|2[0-3])[0-5][0-9]|2400)')])),
            ],
        ),
        migrations.CreateModel(
            name='Proxy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255, unique=True)),
                ('address', models.CharField(default='', max_length=255)),
                ('port', models.PositiveIntegerField(default=8443)),
                ('secret', models.CharField(default='', max_length=255)),
                ('web_secret', models.CharField(default='', max_length=255)),
                ('web_address', models.CharField(default='', max_length=255)),
                ('web_port', models.PositiveIntegerField(default=4443)),
                ('disabled', models.BooleanField(default=False)),
                ('comment', models.CharField(blank=True, default='', max_length=1024, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SchedulingInterval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interval', models.PositiveIntegerField(default=350)),
            ],
        ),
        migrations.CreateModel(
            name='TimePeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255, unique=True)),
                ('comment', models.CharField(blank=True, default='', max_length=1024, null=True)),
                ('time_periods', models.ManyToManyField(to='description.DayTimePeriod')),
            ],
        ),
        migrations.CreateModel(
            name='OrderedListItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.PositiveIntegerField(default=1)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
        migrations.CreateModel(
            name='MetricTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255, unique=True)),
                ('comment', models.CharField(blank=True, default='', max_length=1024, null=True)),
                ('linked_check', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='description.check')),
                ('linked_contact_groups', models.ManyToManyField(blank=True, to='description.ContactGroup')),
                ('linked_contacts', models.ManyToManyField(blank=True, to='description.Contact')),
                ('metric_templates', models.ManyToManyField(blank=True, to='description.MetricTemplate')),
                ('notification_period', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='notification_mt', to='description.timeperiod')),
                ('scheduling_interval', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='description.schedulinginterval')),
                ('scheduling_period', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='scheduling_mt', to='description.timeperiod')),
            ],
        ),
        migrations.CreateModel(
            name='Metric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
                ('disabled', models.BooleanField(blank=True, default=False, null=True)),
                ('comment', models.CharField(blank=True, default='', max_length=1024, null=True)),
                ('linked_check', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='description.check')),
                ('linked_contact_groups', models.ManyToManyField(blank=True, to='description.ContactGroup')),
                ('linked_contacts', models.ManyToManyField(blank=True, to='description.Contact')),
                ('linked_host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='description.host')),
                ('linked_proxy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='description.proxy')),
                ('metric_templates', models.ManyToManyField(blank=True, to='description.MetricTemplate')),
                ('notification_period', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='notification', to='description.timeperiod')),
                ('scheduling_interval', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='description.schedulinginterval')),
                ('scheduling_period', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='scheduling', to='description.timeperiod')),
            ],
        ),
        migrations.CreateModel(
            name='HostTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255, unique=True)),
                ('address', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('comment', models.CharField(blank=True, default='', max_length=1024, null=True)),
                ('host_templates', models.ManyToManyField(blank=True, to='description.OrderedListItem')),
                ('linked_check', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='description.check')),
                ('linked_contact_groups', models.ManyToManyField(blank=True, to='description.ContactGroup')),
                ('linked_contacts', models.ManyToManyField(blank=True, to='description.Contact')),
                ('notification_period', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='notification_ht', to='description.timeperiod')),
                ('scheduling_interval', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='description.schedulinginterval')),
                ('scheduling_period', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='scheduling_ht', to='description.timeperiod')),
            ],
        ),
        migrations.AddField(
            model_name='host',
            name='host_templates',
            field=models.ManyToManyField(blank=True, to='description.OrderedListItem'),
        ),
        migrations.AddField(
            model_name='host',
            name='linked_check',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='description.check'),
        ),
        migrations.AddField(
            model_name='host',
            name='linked_contact_groups',
            field=models.ManyToManyField(blank=True, to='description.ContactGroup'),
        ),
        migrations.AddField(
            model_name='host',
            name='linked_contacts',
            field=models.ManyToManyField(blank=True, to='description.Contact'),
        ),
        migrations.AddField(
            model_name='host',
            name='linked_proxy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='description.proxy'),
        ),
        migrations.AddField(
            model_name='host',
            name='notification_period',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='notification_h', to='description.timeperiod'),
        ),
        migrations.AddField(
            model_name='host',
            name='scheduling_interval',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='description.schedulinginterval'),
        ),
        migrations.AddField(
            model_name='host',
            name='scheduling_period',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='scheduling_h', to='description.timeperiod'),
        ),
        migrations.CreateModel(
            name='GenericKVP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='key', to='description.label')),
                ('value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='value', to='description.label')),
            ],
        ),
        migrations.AddField(
            model_name='daytimeperiod',
            name='periods',
            field=models.ManyToManyField(to='description.Period'),
        ),
        migrations.AddField(
            model_name='contact',
            name='linked_host_notification_period',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='contact_host_nt', to='description.timeperiod'),
        ),
        migrations.AddField(
            model_name='contact',
            name='linked_host_notifications',
            field=models.ManyToManyField(blank=True, related_name='contact_host_check', to='description.Check'),
        ),
        migrations.AddField(
            model_name='contact',
            name='linked_metric_notification_period',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='contact_metric_nt', to='description.timeperiod'),
        ),
        migrations.AddField(
            model_name='contact',
            name='linked_metric_notifications',
            field=models.ManyToManyField(blank=True, related_name='contact_metric_check', to='description.Check'),
        ),
    ]