from django import forms
from .models import Book, BorrowedBook, StudentProfile
from django.contrib.auth.models import User, Group

class BorrowedBookForm(forms.ModelForm):
    class Meta:
        model = BorrowedBook
        fields = ['student', 'book', 'deadline']  # Добавляем поле student
        widgets = {
            'book': forms.Select(choices=[(book.id, book.title) for book in Book.objects.filter(available=True)]),
        }
    def __init__(self, *args, **kwargs):
        super(BorrowedBookForm, self).__init__(*args, **kwargs)
        self.fields['student'].queryset = StudentProfile.objects.all()  # Отображаем всех студентов
        self.fields['book'].queryset = Book.objects.filter(available=True)  # Отображаем только доступные книги
        self.fields['deadline'].widget = forms.SelectDateWidget()  # Используем виджет для выбора даты

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'available']


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    group_name = forms.CharField(max_length=100, required=True, label="Group Name")

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'group_name']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            # Получаем или создаем группу по имени
            group_name = self.cleaned_data['group_name']
            group, created = Group.objects.get_or_create(name=group_name)
            # Добавляем пользователя в группу
            user.groups.add(group)
        return user
