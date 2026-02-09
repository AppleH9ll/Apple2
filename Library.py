from abc import ABC, abstractmethod
from datetime import datetime
from typing import List


class Person(ABC):
    def __init__(self, name, person_id):
        self.__name = name
        self.__id = person_id
    
    @abstractmethod
    def get_menu_options(self):
        pass
    
    @property
    def name(self):
        return self.__name
    
    @property
    def id(self):
        return self.__id


class User(Person):
    def __init__(self, name, person_id):
        super().__init__(name, person_id)
        self.__borrowed_books = []
    
    def get_menu_options(self):
        return [
            "Просмотреть доступные книги",
            "Взять книгу",
            "Вернуться в главное меню"
        ]
    
    def borrow_book(self, book):
        if book.is_available:
            self.__borrowed_books.append(book)
            book.borrow()
            return True
        return False
    
    def get_borrowed_books(self):
        return self.__borrowed_books


class Librarian(Person):
    def __init__(self, name, person_id):
        super().__init__(name, person_id)
    
    def get_menu_options(self):
        return [
            "Добавить новую книгу",
            "Удалить книгу из системы",
            "Зарегистрировать нового пользователя",
            "Просмотреть список всех пользователей",
            "Просмотреть список всех книг",
            "Вернуться в главное меню"
        ]


class Book:
    def __init__(self, title, author, isbn):
        self.__title = title
        self.__author = author
        self.__isbn = isbn
        self.__is_available = True
        self.__borrow_date = None
    
    @property
    def title(self):
        return self.__title
    
    @property
    def author(self):
        return self.__author
    
    @property
    def isbn(self):
        return self.__isbn
    
    @property
    def is_available(self):
        return self.__is_available
    
    def borrow(self):
        if self.__is_available:
            self.__is_available = False
            self.__borrow_date = datetime.now()
            return True
        return False
    
    def return_book(self):
        self.__is_available = True
        self.__borrow_date = None
    
    def get_status(self):
        if self.__is_available:
            return "Доступна"
        return "Выдана"


class LibrarySystem:
    def __init__(self):
        self.__books = []
        self.__users = []
        self.__librarians = []
        self.__current_person = None
        self.__setup_initial_data()
    
    def __setup_initial_data(self):
        librarian = Librarian("Анна Иванова", "L001")
        self.__librarians.append(librarian)
        
        self.__books.append(Book("Мастер и Маргарита", "Михаил Булгаков", "9785170906440"))
        self.__books.append(Book("Преступление и наказание", "Федор Достоевский", "9785041039048"))
        self.__books.append(Book("1984", "Джордж Оруэлл", "9785170908338"))
        
        self.__users.append(User("Иван Петров", "U001"))
        self.__users.append(User("Мария Сидорова", "U002"))
    
    def add_book(self, book):
        self.__books.append(book)
    
    def remove_book(self, isbn):
        for book in self.__books:
            if book.isbn == isbn:
                self.__books.remove(book)
                return True
        return False
    
    def register_user(self, name, user_id):
        user = User(name, user_id)
        self.__users.append(user)
        return user
    
    def get_all_users(self):
        return self.__users
    
    def get_all_books(self):
        return self.__books
    
    def get_available_books(self):
        available = []
        for book in self.__books:
            if book.is_available:
                available.append(book)
        return available
    
    def find_book_by_isbn(self, isbn):
        for book in self.__books:
            if book.isbn == isbn:
                return book
        return None
    
    def find_user_by_id(self, user_id):
        for user in self.__users:
            if user.id == user_id:
                return user
        return None
    
    def find_librarian_by_id(self, librarian_id):
        for librarian in self.__librarians:
            if librarian.id == librarian_id:
                return librarian
        return None
    
    def set_current_person(self, person):
        self.__current_person = person
    
    def get_current_person(self):
        return self.__current_person


class LibraryApp:
    def __init__(self):
        self.system = LibrarySystem()
        self.start()
    
    def display_menu(self, options, title):
        print(f"\n{title}")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
    
    def display_books(self, books, title):
        print(f"\n{title}")
        if not books:
            print("Книги не найдены")
            return
        
        for i, book in enumerate(books, 1):
            status = book.get_status()
            print(f"{i}. {book.title} - {book.author} (ISBN: {book.isbn}) | Статус: {status}")
    
    def display_users(self, users, title):
        print(f"\n{title}")
        if not users:
            print("Пользователи не найдены")
            return
        
        for i, user in enumerate(users, 1):
            borrowed_count = len(user.get_borrowed_books())
            print(f"{i}. {user.name} (ID: {user.id}) | Книг на руках: {borrowed_count}")
    
    def start(self):
        while True:
            print("\nБиблиотечная система")
            print("1. Войти как библиотекарь")
            print("2. Войти как пользователь")
            print("3. Выход")
            
            choice = input("Выберите действие: ")
            
            if choice == "1":
                self.librarian_login()
            elif choice == "2":
                self.user_login()
            elif choice == "3":
                print("Завершение работы")
                break
            else:
                print("Неверный выбор")
    
    def librarian_login(self):
        librarian_id = input("Введите ID библиотекаря: ")
        librarian = self.system.find_librarian_by_id(librarian_id)
        
        if not librarian:
            print("Библиотекарь с таким ID не найден")
            return
        
        self.system.set_current_person(librarian)
        self.librarian_menu(librarian)
    
    def librarian_menu(self, librarian):
        while True:
            self.display_menu(librarian.get_menu_options(), f"Библиотекарь: {librarian.name}")
            
            choice = input("Выберите действие: ")
            
            if choice == "1":
                self.add_book()
            elif choice == "2":
                self.remove_book()
            elif choice == "3":
                self.register_user()
            elif choice == "4":
                self.display_users(self.system.get_all_users(), "Зарегистрированные пользователи")
            elif choice == "5":
                self.display_books(self.system.get_all_books(), "Все книги в системе")
            elif choice == "6":
                break
            else:
                print("Неверный выбор")
    
    def add_book(self):
        print("\nДобавление новой книги")
        title = input("Введите название книги: ")
        author = input("Введите автора: ")
        isbn = input("Введите ISBN: ")
        
        if not title or not author or not isbn:
            print("Все поля должны быть заполнены")
            return
        
        existing_book = self.system.find_book_by_isbn(isbn)
        if existing_book:
            print("Книга с таким ISBN уже существует")
            return
        
        book = Book(title, author, isbn)
        self.system.add_book(book)
        print(f"Книга '{title}' успешно добавлена")
    
    def remove_book(self):
        isbn = input("Введите ISBN книги для удаления: ")
        
        if self.system.remove_book(isbn):
            print("Книга успешно удалена")
        else:
            print("Книга с таким ISBN не найдена")
    
    def register_user(self):
        print("\nРегистрация нового пользователя")
        name = input("Введите имя пользователя: ")
        user_id = input("Введите ID пользователя: ")
        
        if not name or not user_id:
            print("Все поля должны быть заполнены")
            return
        
        existing_user = self.system.find_user_by_id(user_id)
        if existing_user:
            print("Пользователь с таким ID уже существует")
            return
        
        self.system.register_user(name, user_id)
        print(f"Пользователь '{name}' успешно зарегистрирован")
    
    def user_login(self):
        user_id = input("Введите ID пользователя: ")
        user = self.system.find_user_by_id(user_id)
        
        if not user:
            print("Пользователь с таким ID не найден")
            return
        
        self.system.set_current_person(user)
        self.user_menu(user)
    
    def user_menu(self, user):
        while True:
            self.display_menu(user.get_menu_options(), f"Пользователь: {user.name}")
            
            choice = input("Выберите действие: ")
            
            if choice == "1":
                available_books = self.system.get_available_books()
                self.display_books(available_books, "Доступные книги")
            elif choice == "2":
                self.borrow_book(user)
            elif choice == "3":
                break
            else:
                print("Неверный выбор")
    
    def borrow_book(self, user):
        isbn = input("Введите ISBN книги, которую хотите взять: ")
        book = self.system.find_book_by_isbn(isbn)
        
        if not book:
            print("Книга с таким ISBN не найдена")
            return
        
        if not book.is_available:
            print("Эта книга уже выдана")
            return
        
        if user.borrow_book(book):
            print(f"Вы взяли книгу: '{book.title}'")
        else:
            print("Не удалось взять книгу")


if __name__ == "__main__":
    app = LibraryApp()