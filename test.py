from django.contrib.auth.models import Group

group1 = Group.objects.get(id=1)

print(group1)