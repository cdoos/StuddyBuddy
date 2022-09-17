from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User
from place.models import Place


class Appointment(models.Model):
    topic = models.CharField(max_length=50, blank=True, null=True)
    subject = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    offline_mode = models.BooleanField(default=True, blank=True, null=True)
    meeting_link = models.CharField(max_length=255, blank=True, null=True)
    host_username = models.CharField(max_length=50, blank=True, null=True)
    place_name = models.CharField(blank=True, null=True, max_length=60)
    users = models.ManyToManyField(
        User,
        verbose_name=_("User"),
        related_name="appointments",
        db_table="users_appointments",
    )
    host = models.ForeignKey(
        User,
        verbose_name=_("Host"),
        on_delete=models.PROTECT,
        related_name="host_appointments",
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.topic}"
