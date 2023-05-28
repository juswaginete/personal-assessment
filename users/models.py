from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

optional = {
    'null': True,
    'blank': True
}


class Profiles(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profiles")
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, **optional)
    phone_number = models.CharField(max_length=50, **optional)

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"