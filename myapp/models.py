from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db import models
class Todo(models.Model):
    task_name=models.CharField(max_length=230)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    date=models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return self.task_name
