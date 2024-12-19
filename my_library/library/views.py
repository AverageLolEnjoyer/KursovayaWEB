from django.shortcuts import render, get_object_or_404, redirect
from .forms import BookForm, BorrowedBookForm
from django.contrib.auth.decorators import user_passes_test
from .models import Book, BorrowedBook, StudentProfile, StudentProfile
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test


@login_required
def index(request):
    books = Book.objects.all()  # Получаем все книги из базы данных
    return render(request, 'library/index.html', {'user': request.user, 'books': books})
@user_passes_test(lambda u: u.is_superuser)
def student_list(request):
    # Получаем всех студентов и их задолженные книги
    students = StudentProfile.objects.all()
    borrowed_books = BorrowedBook.objects.select_related('book').filter(student__in=students)

    # Создаем словарь для хранения задолженных книг по студентам
    student_books = {}
    for student in students:
        student_books[student] = borrowed_books.filter(student=student)

    return render(request, 'library/student_list.html', {'student_books': student_books})

@user_passes_test(lambda u: u.is_superuser)
def delete_borrowed_book(request, borrowed_book_id):
    borrowed_book = get_object_or_404(BorrowedBook, id=borrowed_book_id)
    borrowed_book.delete()
    book = borrowed_book.book
    book.available = True
    book.save()
    return redirect('index')  # Перенаправление на страницу со списком задолженностей

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = BookForm()
    return render(request, 'library/add_book.html', {'form': form})
@user_passes_test(lambda u: u.is_superuser)
def add_borrowed_book(request):
    available_books = Book.objects.filter(available=True)  # Получаем только доступные книги
    if request.method == 'POST':
        form = BorrowedBookForm(request.POST)
        if form.is_valid():
            borrowed_book = form.save(commit=False)
            # Получаем профиль студента из формы
            student_profile = form.cleaned_data['student']
            borrowed_book.student = student_profile

            # Получаем выбранную книгу из формы
            selected_book_id = form.cleaned_data['book'].id
            borrowed_book.book = Book.objects.get(id=selected_book_id)
            borrowed_book.save()

            # Обновляем статус доступности книги
            book = borrowed_book.book
            book.available = False
            book.save()

            return redirect('index')
    else:
        form = BorrowedBookForm()

    return render(request, 'library/add_borrowed_book.html', {
        'form': form,
        'available_books': available_books
    })
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def user_profile(request):
    return render(request, 'library/user_profile.html', {'user': request.user})

@login_required

def student_dashboard(request):
    # Получаем профиль студента, связанный с текущим пользователем
    student_profile = get_object_or_404(StudentProfile, user=request.user)

    # Получаем заимствованные книги для этого студента
    borrowed_books = BorrowedBook.objects.filter(student=student_profile)

    return render(request, 'library/student_dashboard.html', {'borrowed_books': borrowed_books})


def search_book(request):
    query = request.GET.get('q')
    if query:
        # Ищем книгу по заголовку или автору
        book = Book.objects.filter(title__icontains=query) | Book.objects.filter(author__icontains=query)

        if book.exists():
            # Если найдены книги, возвращаем первую из них
            return render(request, 'library/book_detail.html', {'book': book.first()})

    return render(request, 'search.html', {'error': 'Книга не найдена.'})