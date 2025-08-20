# Python 新手指南：07 物件導向程式設計基礎

**作者：** Tsung-Min Pai  
**單位：** NTUEE

---

## 大綱

### 1 類別與物件

- 類別的定義
- 物件的建立
- 屬性與方法

### 2 建構函式與初始化

- **init** 方法
- 實例屬性
- 類別屬性

### 3 封裝與存取控制

- 私有屬性
- getter 和 setter
- 屬性裝飾器

### 4 繼承與多型

- 基本繼承
- 方法覆寫
- super() 函式

---

## 類別與物件

**什麼是類別？**

- 類別是建立物件的藍圖或模板
- 定義了物件的屬性和行為
- 使用 `class` 關鍵字定義

**什麼是物件？**

- 物件是類別的實例
- 每個物件都有自己的屬性值
- 可以呼叫類別定義的方法

```python
# 定義一個簡單的類別
class Student:
    def __init__(self, name, age):
        self.name = name  # 實例屬性
        self.age = age

    def introduce(self):  # 實例方法
        print(f"我是 {self.name}，今年 {self.age} 歲")

# 建立物件
student1 = Student("張小明", 20)
student2 = Student("李小華", 21)

# 呼叫方法
student1.introduce()  # 輸出: 我是 張小明，今年 20 歲
student2.introduce()  # 輸出: 我是 李小華，今年 21 歲
```

---

## 建構函式與初始化

\***\*init** 方法：\*\*

- 建構函式，在建立物件時自動呼叫
- 用來初始化物件的屬性
- `self` 參數代表物件本身

```python
class Car:
    def __init__(self, brand, model, year):
        self.brand = brand      # 品牌
        self.model = model      # 型號
        self.year = year        # 年份
        self.mileage = 0        # 里程數，預設為 0

    def drive(self, distance):
        self.mileage += distance
        print(f"{self.brand} {self.model} 行駛了 {distance} 公里")

    def get_info(self):
        return f"{self.year} {self.brand} {self.model}, 里程數: {self.mileage} 公里"

# 建立汽車物件
my_car = Car("Toyota", "Camry", 2020)
print(my_car.get_info())  # 2020 Toyota Camry, 里程數: 0 公里

my_car.drive(100)
print(my_car.get_info())  # 2020 Toyota Camry, 里程數: 100 公里
```

---

## 實例屬性與類別屬性

**實例屬性：**

- 每個物件獨有的屬性
- 在 `__init__` 方法中使用 `self.` 定義

**類別屬性：**

- 所有物件共享的屬性
- 在類別內直接定義，不在方法內

```python
class BankAccount:
    # 類別屬性 - 所有帳戶共享
    bank_name = "台灣銀行"
    interest_rate = 0.01

    def __init__(self, account_holder, initial_balance=0):
        # 實例屬性 - 每個帳戶獨有
        self.account_holder = account_holder
        self.balance = initial_balance
        self.transaction_history = []

    def deposit(self, amount):
        self.balance += amount
        self.transaction_history.append(f"存款: +{amount}")
        print(f"存款 {amount} 元，餘額: {self.balance} 元")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            self.transaction_history.append(f"提款: -{amount}")
            print(f"提款 {amount} 元，餘額: {self.balance} 元")
        else:
            print("餘額不足")

    def get_account_info(self):
        print(f"銀行: {BankAccount.bank_name}")
        print(f"帳戶持有人: {self.account_holder}")
        print(f"餘額: {self.balance} 元")

# 建立銀行帳戶
account1 = BankAccount("張小明", 1000)
account2 = BankAccount("李小華", 500)

account1.deposit(200)
account1.withdraw(300)
account1.get_account_info()
```

---

## 封裝與存取控制

**私有屬性：**

- 使用雙底線 `__` 開頭
- 只能在類別內部存取
- 提供資料保護

```python
class Student:
    def __init__(self, name, student_id):
        self.name = name                # 公開屬性
        self.__student_id = student_id  # 私有屬性
        self.__grades = []              # 私有屬性

    def add_grade(self, subject, score):
        if 0 <= score <= 100:
            self.__grades.append({"subject": subject, "score": score})
            print(f"已新增 {subject}: {score} 分")
        else:
            print("分數必須在 0-100 之間")

    def get_average(self):
        if not self.__grades:
            return 0
        total = sum(grade["score"] for grade in self.__grades)
        return total / len(self.__grades)

    def get_student_id(self):  # getter 方法
        return self.__student_id

    def get_grades(self):      # getter 方法
        return self.__grades.copy()  # 回傳副本，避免外部修改

# 使用範例
student = Student("王小美", "B10901001")
student.add_grade("數學", 95)
student.add_grade("英文", 88)

print(f"學號: {student.get_student_id()}")
print(f"平均分數: {student.get_average():.1f}")

# 無法直接存取私有屬性
# print(student.__student_id)  # 這會引發 AttributeError
```

---

## 屬性裝飾器

**使用 @property 裝飾器：**

```python
class Circle:
    def __init__(self, radius):
        self.__radius = radius

    @property
    def radius(self):
        """取得半徑"""
        return self.__radius

    @radius.setter
    def radius(self, value):
        """設定半徑"""
        if value > 0:
            self.__radius = value
        else:
            raise ValueError("半徑必須大於 0")

    @property
    def area(self):
        """計算面積 (唯讀屬性)"""
        return 3.14159 * self.__radius ** 2

    @property
    def circumference(self):
        """計算周長 (唯讀屬性)"""
        return 2 * 3.14159 * self.__radius

# 使用範例
circle = Circle(5)
print(f"半徑: {circle.radius}")           # 5
print(f"面積: {circle.area:.2f}")         # 78.54
print(f"周長: {circle.circumference:.2f}") # 31.42

circle.radius = 10  # 使用 setter
print(f"新半徑: {circle.radius}")         # 10
print(f"新面積: {circle.area:.2f}")       # 314.16

# circle.area = 100  # 這會引發 AttributeError，因為 area 是唯讀的
```

---

## 基本繼承

**繼承的概念：**

- 子類別可以繼承父類別的屬性和方法
- 使用 `class ChildClass(ParentClass):` 語法
- 促進程式碼重用

```python
class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def eat(self):
        print(f"{self.name} 正在吃東西")

    def sleep(self):
        print(f"{self.name} 正在睡覺")

    def make_sound(self):
        print(f"{self.name} 發出聲音")

class Dog(Animal):  # Dog 繼承 Animal
    def __init__(self, name, age, breed):
        super().__init__(name, age)  # 呼叫父類別的建構函式
        self.breed = breed

    def make_sound(self):  # 方法覆寫
        print(f"{self.name} 汪汪叫")

    def fetch(self):  # 子類別特有的方法
        print(f"{self.name} 正在撿球")

class Cat(Animal):  # Cat 繼承 Animal
    def __init__(self, name, age, color):
        super().__init__(name, age)
        self.color = color

    def make_sound(self):  # 方法覆寫
        print(f"{self.name} 喵喵叫")

    def climb(self):  # 子類別特有的方法
        print(f"{self.name} 正在爬樹")

# 使用範例
dog = Dog("小白", 3, "黃金獵犬")
cat = Cat("小花", 2, "橘色")

dog.eat()        # 繼承自 Animal
dog.make_sound() # 覆寫的方法
dog.fetch()      # Dog 特有的方法

cat.sleep()      # 繼承自 Animal
cat.make_sound() # 覆寫的方法
cat.climb()      # Cat 特有的方法
```

---

## 多型與方法覆寫

**多型的概念：**

- 不同的物件可以有相同的介面
- 相同的方法呼叫，不同的物件有不同的行為

```python
class Shape:
    def __init__(self, name):
        self.name = name

    def area(self):
        raise NotImplementedError("子類別必須實作 area 方法")

    def perimeter(self):
        raise NotImplementedError("子類別必須實作 perimeter 方法")

class Rectangle(Shape):
    def __init__(self, width, height):
        super().__init__("矩形")
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

class Circle(Shape):
    def __init__(self, radius):
        super().__init__("圓形")
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2

    def perimeter(self):
        return 2 * 3.14159 * self.radius

# 多型的展示
shapes = [
    Rectangle(5, 3),
    Circle(4),
    Rectangle(10, 2)
]

for shape in shapes:
    print(f"{shape.name}:")
    print(f"  面積: {shape.area():.2f}")
    print(f"  周長: {shape.perimeter():.2f}")
    print()
```

---

## 實用範例：圖書館管理系統

```python
class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_borrowed = False
        self.borrower = None

    def borrow(self, borrower_name):
        if not self.is_borrowed:
            self.is_borrowed = True
            self.borrower = borrower_name
            print(f"《{self.title}》已借給 {borrower_name}")
            return True
        else:
            print(f"《{self.title}》已被 {self.borrower} 借走")
            return False

    def return_book(self):
        if self.is_borrowed:
            print(f"《{self.title}》已由 {self.borrower} 歸還")
            self.is_borrowed = False
            self.borrower = None
            return True
        else:
            print(f"《{self.title}》未被借出")
            return False

    def get_info(self):
        status = f"已借給 {self.borrower}" if self.is_borrowed else "可借閱"
        return f"《{self.title}》- 作者: {self.author}, ISBN: {self.isbn}, 狀態: {status}"

class Library:
    def __init__(self, name):
        self.name = name
        self.books = []

    def add_book(self, book):
        self.books.append(book)
        print(f"已新增書籍：《{book.title}》")

    def find_book(self, title):
        for book in self.books:
            if book.title == title:
                return book
        return None

    def borrow_book(self, title, borrower_name):
        book = self.find_book(title)
        if book:
            return book.borrow(borrower_name)
        else:
            print(f"找不到書籍：《{title}》")
            return False

    def return_book(self, title):
        book = self.find_book(title)
        if book:
            return book.return_book()
        else:
            print(f"找不到書籍：《{title}》")
            return False

    def list_books(self):
        print(f"\n{self.name} 書籍清單：")
        for book in self.books:
            print(f"  {book.get_info()}")

# 使用範例
library = Library("市立圖書館")

# 新增書籍
book1 = Book("Python 程式設計", "張三", "978-1234567890")
book2 = Book("資料結構與演算法", "李四", "978-0987654321")
book3 = Book("機器學習入門", "王五", "978-1122334455")

library.add_book(book1)
library.add_book(book2)
library.add_book(book3)

# 列出所有書籍
library.list_books()

# 借書
library.borrow_book("Python 程式設計", "小明")
library.borrow_book("資料結構與演算法", "小華")

# 再次列出書籍
library.list_books()

# 還書
library.return_book("Python 程式設計")

# 最終書籍狀態
library.list_books()
```

---

## 總結與 Q&A

我們已經涵蓋了 Python 物件導向程式設計的基礎概念！

- **類別與物件**：學會定義類別和建立物件實例。
- **封裝**：使用私有屬性和屬性裝飾器保護資料。
- **繼承**：透過繼承重用程式碼並建立類別階層。
- **多型**：同一介面，不同實作的程式設計概念。

有任何問題嗎？
