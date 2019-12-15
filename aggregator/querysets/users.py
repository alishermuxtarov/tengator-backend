from django.contrib.auth import models

from aggregator.utils.helpers import integers_only


class UsersManager(models.UserManager):
    def sign_in(self, phone, country):
        from aggregator.models import ConfirmationCode

        phone = integers_only(phone)
        user, created = self.get_or_create(username=phone, defaults={'password': ''})

        confirmation = ConfirmationCode.objects.create(
            user=user,
            phone=phone,
            created_by=user,
            type=ConfirmationCode.AUTHENTICATION
        )
        confirmation.send()
        return user, confirmation.code
