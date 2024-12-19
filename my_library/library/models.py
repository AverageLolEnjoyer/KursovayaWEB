from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.CharField(max_length=10)  # Например, 'БФИ2201'
    full_name = models.CharField(max_length=100)  # ФИО

    def __str__(self):
        return self.user.username

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class BorrowedBook(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)  # Связь с пользователем
    book = models.ForeignKey(Book, on_delete=models.CASCADE)      # Связь с книгой
    deadline = models.DateField()                                  # Дата дедлайна

    def __str__(self):
        return f"{self.student.username} borrowed {self.book.title}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        StudentProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.studentprofile.save()

 # Выводим имя пользователя и email
