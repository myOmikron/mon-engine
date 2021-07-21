from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import CharField, ForeignKey, ManyToManyField, PositiveIntegerField, BooleanField, EmailField


class GlobalVariable(models.Model):
    """Represents a global variable"""
    variable = GenericRelation("GenericKVP")

    def to_dict(self):
        return self.variable.to_dict() + {"id": self.id}


class SchedulingInterval(models.Model):
    """Scheduling Interval. The value is interpreted in seconds."""
    interval = models.PositiveIntegerField(default=350)

    def __str__(self):
        return str(self.interval)


class Day(models.Model):
    """Day of the weak. Quite simple."""
    name = CharField(default="", max_length=16, unique=True)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.name == "":
            raise ValueError("Name of day can not be \"\"")
        super(Day, self).save(force_insert=force_insert, force_update=force_update, using=using,
                              update_fields=update_fields)


class Period(models.Model):
    """Specific start and stop time.

    Values can be from 0000 to 2400.
    """
    start_time = CharField(default="", max_length=4, validators=[RegexValidator("(([01][0-9]|2[0-3])[0-5][0-9]|2400)")])
    stop_time = CharField(default="", max_length=4, validators=[RegexValidator("(([01][0-9]|2[0-3])[0-5][0-9]|2400)")])

    def __str__(self):
        return f"{self.start_time}-{self.stop_time}"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if int(self.stop_time) <= int(self.start_time):
            raise ValueError("start_time has to lesser than stop_time")
        super(Period, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                 update_fields=update_fields)


class DayTimePeriod(models.Model):
    """Time period(s) of a specific day"""
    day = ForeignKey(Day, on_delete=models.CASCADE)
    periods = ManyToManyField(Period)

    def __str__(self):
        return f"{self.day} - {' '.join([str(x) for x in self.periods.all()])}"


class TimePeriod(models.Model):
    """The complete time period. Included values for all days"""
    name = CharField(default="", max_length=255, unique=True)
    time_periods = ManyToManyField(DayTimePeriod)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "time_periods": {
                x.day.name: [
                    {"start_time": y.start_time, "stop_time": y.stop_time}
                    for y in x.periods.all()
                ] for x in self.time_periods.all()
            }
        }

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.name == "":
            raise ValueError("Name of a TimePeriod can not be \"\"")
        super(TimePeriod, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                     update_fields=update_fields)


class CheckType(models.Model):
    name = CharField(default="", max_length=255, unique=True)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.name == "":
            raise ValueError("Name of a CheckType can not be \"\"")
        super(CheckType, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                    update_fields=update_fields)


class Check(models.Model):
    name = CharField(default="", max_length=255, unique=True)
    cmd = CharField(default="", max_length=1024, blank=True, null=True)
    check_type = ForeignKey(CheckType, on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "cmd": self.name if self.name else "",
            "check_type": self.check_type.name if self.check_type else ""
        }

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.name == "":
            raise ValueError("Name of a Check can not be \"\"")
        super(Check, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                update_fields=update_fields)


class Contact(models.Model):
    """Contact represents the model which holds the contact information and the contact methods that should be
        used when generating an event.
    """
    name = CharField(default="", max_length=255, unique=True)
    mail = EmailField(default="", max_length=255, null=True, blank=True)
    linked_host_notifications = ManyToManyField(Check, blank=True, related_name="contact_host_check")
    linked_host_notification_period = ForeignKey(
        TimePeriod, on_delete=models.DO_NOTHING,
        blank=True, null=True,
        related_name="contact_host_nt")
    linked_metric_notifications = ManyToManyField(Check, blank=True, related_name="contact_metric_check")
    linked_metric_notification_period = ForeignKey(
        TimePeriod, on_delete=models.DO_NOTHING,
        blank=True, null=True,
        related_name="contact_metric_nt")
    variables = GenericRelation("GenericKVP")

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "mail": self.mail,
            "linked_host_notifications": self.linked_host_notifications,
            "linked_host_notification_period": self.linked_host_notification_period_id,
            "linked_metric_notifications": self.linked_metric_notifications,
            "linked_metric_notification_period": self.linked_metric_notification_period_id,
            "variables": {y[0]: y[1] for y in (x for x in self.variables.all())}
        }

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.name == "":
            raise ValueError("Name of a Contact can not be \"\"")
        super(Contact, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                  update_fields=update_fields)


class ContactGroup(models.Model):
    """This class represents a group of contacts. Only used for grouping"""
    name = CharField(default="", max_length=255, unique=True)
    linked_contacts = ManyToManyField(Contact, blank=True)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "linked_contacts": [x.id for x in self.linked_contacts.all()]
        }

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.name == "":
            raise ValueError("Name of a ContactGroup can not be \"\"")
        super(ContactGroup, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                       update_fields=update_fields)


class HostTemplate(models.Model):
    """Template of a host"""
    name = CharField(default="", max_length=255, unique=True)
    address = CharField(default="", max_length=255, blank=True, null=True)
    linked_check = ForeignKey(Check, on_delete=models.DO_NOTHING, blank=True, null=True)
    host_templates = ManyToManyField("self", blank=True)
    scheduling_interval = ForeignKey(SchedulingInterval, on_delete=models.DO_NOTHING, blank=True, null=True)
    scheduling_period = ForeignKey(
        TimePeriod, on_delete=models.DO_NOTHING,
        blank=True, null=True,
        related_name="scheduling_ht"
    )
    notification_period = ForeignKey(
        TimePeriod, on_delete=models.DO_NOTHING,
        blank=True, null=True,
        related_name="notification_ht"
    )
    variables = GenericRelation("GenericKVP")

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "linked_check": self.linked_check_id,
            "host_templates": [x.id for x in self.host_templates.all()],
            "scheduling_interval": self.scheduling_interval_id,
            "scheduling_period": self.scheduling_period_id,
            "notification_period": self.notification_period_id,
            "variables": {y[0]: y[1] for y in (x for x in self.variables.all())}
        }

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.name == "":
            raise ValueError("Name of a HostTemplate can not be \"\"")
        super(HostTemplate, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                       update_fields=update_fields)


class Host(models.Model):
    """This class represents a host"""
    name = CharField(max_length=255, unique=True)
    address = CharField(default="", max_length=255, blank=True, null=True)
    linked_check = ForeignKey(Check, on_delete=models.DO_NOTHING, blank=True, null=True)
    disabled = BooleanField(default=False, blank=True, null=True)
    host_templates = ManyToManyField(HostTemplate, blank=True)
    scheduling_interval = ForeignKey(SchedulingInterval, on_delete=models.DO_NOTHING, blank=True, null=True)
    scheduling_period = ForeignKey(
        TimePeriod, on_delete=models.DO_NOTHING,
        blank=True, null=True,
        related_name="scheduling_h"
    )
    notification_period = ForeignKey(
        TimePeriod, on_delete=models.DO_NOTHING,
        blank=True, null=True,
        related_name="notification_h"
    )
    variables = GenericRelation("GenericKVP")

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "linked_check": self.linked_check_id,
            "disabled": self.disabled,
            "host_templates": [x.id for x in self.host_templates.all()],
            "scheduling_interval": self.scheduling_interval_id,
            "scheduling_period": self.scheduling_period_id,
            "notification_period": self.notification_period_id,
            "variables": {y[0]: y[1] for y in (x for x in self.variables.all())}
        }

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.name == "":
            raise ValueError("Name of a Host can not be \"\"")
        super(Host, self).save(force_insert=force_insert, force_update=force_update, using=using,
                               update_fields=update_fields)


class MetricTemplate(models.Model):
    """This class represents a template for a metric"""
    name = CharField(default="", max_length=255, unique=True)
    linked_check = ForeignKey(Check, on_delete=models.DO_NOTHING, blank=True, null=True)
    linked_host = ForeignKey(Host, on_delete=models.CASCADE)
    metric_templates = ManyToManyField("self", blank=True)
    scheduling_interval = ForeignKey(SchedulingInterval, on_delete=models.DO_NOTHING, blank=True, null=True)
    scheduling_period = ForeignKey(
        TimePeriod, on_delete=models.DO_NOTHING,
        blank=True, null=True,
        related_name="scheduling_mt"
    )
    notification_period = ForeignKey(
        TimePeriod, on_delete=models.DO_NOTHING,
        blank=True, null=True,
        related_name="notification_mt"
    )
    variables = GenericRelation("GenericKVP")

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "linked_check": self.linked_check_id if self.linked_check else "",
            "linked_host": self.linked_host_id if self.linked_host else "",
            "metric_templates": [x.id for x in self.metric_templates.all()],
            "scheduling_interval": self.scheduling_interval_id if self.scheduling_interval else "",
            "scheduling_period": self.scheduling_period_id if self.scheduling_period else "",
            "notification_period": self.notification_period_id if self.notification_period else "",
            "variables": {y[0]: y[1] for y in (x.to_dict() for x in self.variables.all())}
        }

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.name == "":
            raise ValueError("Name of a MetricTemplate can not be \"\"")
        super(MetricTemplate, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                         update_fields=update_fields)


class Metric(models.Model):
    """This class represents a Metric"""
    name = CharField(default="", max_length=255)
    linked_check = ForeignKey(Check, on_delete=models.DO_NOTHING, blank=True, null=True)
    linked_host = ForeignKey(Host, on_delete=models.CASCADE)
    disabled = BooleanField(default=False, blank=True, null=True)
    metric_templates = ManyToManyField(MetricTemplate, blank=True)
    scheduling_interval = ForeignKey(SchedulingInterval, on_delete=models.DO_NOTHING, blank=True, null=True)
    scheduling_period = ForeignKey(
        TimePeriod, on_delete=models.DO_NOTHING,
        blank=True, null=True,
        related_name="scheduling"
    )
    notification_period = ForeignKey(
        TimePeriod, on_delete=models.DO_NOTHING,
        blank=True, null=True,
        related_name="notification"
    )
    variables = GenericRelation("GenericKVP")

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "linked_check": self.linked_check_id if self.linked_check else "",
            "linked_host": self.linked_host_id if self.linked_host else "",
            "disabled": self.disabled,
            "metric_templates": [x.id for x in self.metric_templates.all()],
            "scheduling_interval": self.scheduling_interval_id if self.scheduling_interval else "",
            "scheduling_period": self.scheduling_period_id if self.scheduling_period else "",
            "notification_period": self.notification_period_id if self.notification_period else "",
            "variables": {y[0]: y[1] for y in (x.to_dict() for x in self.variables.all())}
        }


class Label(models.Model):
    label = CharField(default="", max_length=255, unique=True, blank=True)

    def __str__(self):
        return self.label


class GenericKVP(models.Model):
    key = ForeignKey(Label, on_delete=models.CASCADE, related_name="key")
    value = ForeignKey(Label, on_delete=models.CASCADE, related_name="value")
    referent = GenericForeignKey('content_type', 'object_id')
    content_type = ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = PositiveIntegerField()

    def __str__(self):
        return f"{self.referent} - {self.key}: {self.value}"

    def to_dict(self):
        return self.key, self.value
