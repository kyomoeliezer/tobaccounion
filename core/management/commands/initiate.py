import os
from django.db import migrations
import bcrypt
from auths.models import User,Staff

DJANGO_SU_NAME = os.environ.get('DJANGO_SU_NAME')
DJANGO_SU_EMAIL = os.environ.get('DJANGO_SU_EMAIL')
DJANGO_SU_PASSWORD = os.environ.get('DJANGO_SU_PASSWORD')


from django.core.management.base import BaseCommand, CommandError
#from basic.views import basic_update #import_dnb_error_codes,import_musoni_dnb_datatable,import_musoni_journal_accounts,import_loanfee_datable,import_payment_datable
class Command(BaseCommand):
    help = 'Create first user'

    def handle(self, *args, **options):
        if not User.objects.first():
            hash_password = bcrypt.hashpw(
                DJANGO_SU_PASSWORD.encode("utf-8"), bcrypt.gensalt()
            )
            hashed_password = hash_password.decode("utf8")
            superuser = User.objects.create(
                username=DJANGO_SU_NAME,
                password=hashed_password)
            superuser.save()
            Staff.objects.create(user=superuser,full_name=DJANGO_SU_NAME,phone_number=DJANGO_SU_EMAIL,is_active=True,is_superuser=True,is_staff=True)


        else:
            hash_password = bcrypt.hashpw(
                DJANGO_SU_PASSWORD.encode("utf-8"), bcrypt.gensalt()
            )
            hashed_password = hash_password.decode("utf8")
            usr=User.objects.filter(username=DJANGO_SU_NAME).update(password=hashed_password,is_active=True,is_superuser=True,is_staff=True)


        self.stdout.write('Successful created the superuser,and initated the the basic setting')

