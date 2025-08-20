# Chapter 4: 函式

**作者：** Tsung-Min Pai  
**單位：** NTUEE

---

## 大綱

### 1 函式 (Functions)

- 函式的定義與特性
- 函式的建立與呼叫
- 參數與回傳值

### 2 參數類型

- 位置參數
- 關鍵字參數
- 預設參數

### 3 變數範圍 (Scope)

- 區域變數
- 全域變數

### 4 內建函式

- 常用內建函式
- 匯入模組

---

## 函式 (Functions)

**定義：** 一個可重複使用的程式碼區塊，用來執行特定的任務。函式可以接收輸入（參數），處理資料，並回傳結果。

**特性：**

- **可重複使用：** 一次定義，多次呼叫。
- **模組化：** 將複雜的程式碼分解成小的、可管理的部分。
- **抽象化：** 隱藏實作細節，專注於功能。

---

## 函式的建立與呼叫

**建立函式：**

```python
def greet():
    print("您好！歡迎使用 Python！")
```

**呼叫函式：**

```python
greet()  # 輸出: 您好！歡迎使用 Python！
```

**帶參數的函式：**

```python
def greet_user(name):
    print(f"您好，{name}！")

greet_user("Tsung-min")  # 輸出: 您好，Tsung-min！
```

**回傳值的函式：**

```python
def add_numbers(a, b):
    return a + b

result = add_numbers(5, 3)
print(result)  # 輸出: 8
```

---

## 參數類型

**位置參數：**

```python
def introduce(name, age, city):
    print(f"我是 {name}，今年 {age} 歲，住在 {city}。")

introduce("Tsung-min", 25, "台北")
```

**關鍵字參數：**

```python
introduce(age=25, name="Tsung-min", city="台北")
```

**預設參數：**

```python
def greet_user(name, greeting="您好"):
    print(f"{greeting}，{name}！")

greet_user("Tsung-min")  # 輸出: 您好，Tsung-min！
greet_user("Tsung-min", "早安")  # 輸出: 早安，Tsung-min！
```

---

## 多個參數與回傳值

**多個參數：**

```python
def calculate_area(length, width):
    area = length * width
    return area

result = calculate_area(10, 5)
print(f"面積是：{result}")  # 輸出: 面積是：50
```

**多個回傳值：**

```python
def get_name_age():
    name = "Tsung-min"
    age = 25
    return name, age

user_name, user_age = get_name_age()
print(f"姓名：{user_name}，年齡：{user_age}")
```

---

## 變數範圍 (Scope)

**區域變數：**

```python
def my_function():
    x = 10  # 區域變數
    print(x)

my_function()  # 輸出: 10
# print(x)  # 這會引發 NameError，因為 x 不在此範圍內
```

**全域變數：**

```python
x = 20  # 全域變數

def my_function():
    print(x)  # 可以存取全域變數

my_function()  # 輸出: 20
print(x)  # 輸出: 20
```

**修改全域變數：**

```python
count = 0  # 全域變數

def increment():
    global count
    count += 1

increment()
print(count)  # 輸出: 1
```

---

## 內建函式

Python 提供許多內建函式，可以直接使用：

**常用內建函式：**

```python
# len() - 取得長度
my_list = [1, 2, 3, 4, 5]
print(len(my_list))  # 輸出: 5

# max() 和 min() - 最大值和最小值
print(max(my_list))  # 輸出: 5
print(min(my_list))  # 輸出: 1

# sum() - 總和
print(sum(my_list))  # 輸出: 15

# type() - 資料型態
print(type(my_list))  # 輸出: <class 'list'>
```

---

## 更多內建函式

**字串相關：**

```python
# str() - 轉換為字串
number = 123
text = str(number)
print(text)  # 輸出: "123"

# int() - 轉換為整數
text = "456"
number = int(text)
print(number)  # 輸出: 456

# float() - 轉換為浮點數
text = "3.14"
number = float(text)
print(number)  # 輸出: 3.14
```

**其他實用函式：**

```python
# range() - 產生數字序列
for i in range(5):
    print(i)  # 輸出: 0, 1, 2, 3, 4

# enumerate() - 取得索引和值
fruits = ["蘋果", "香蕉", "橘子"]
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")
```

---

## 匯入模組

Python 有豐富的標準函式庫，可以透過 `import` 匯入使用：

**匯入整個模組：**

```python
import math

result = math.sqrt(16)
print(result)  # 輸出: 4.0

pi_value = math.pi
print(pi_value)  # 輸出: 3.141592653589793
```

**匯入特定函式：**

```python
from math import sqrt, pi

result = sqrt(25)
print(result)  # 輸出: 5.0
print(pi)  # 輸出: 3.141592653589793
```

**使用別名：**

```python
import math as m

result = m.pow(2, 3)
print(result)  # 輸出: 8.0
```

---

## 實用範例

**計算機函式：**

```python
def calculator(operation, a, b):
    if operation == "加":
        return a + b
    elif operation == "減":
        return a - b
    elif operation == "乘":
        return a * b
    elif operation == "除":
        if b != 0:
            return a / b
        else:
            return "錯誤：不能除以零"
    else:
        return "不支援的運算"

print(calculator("加", 10, 5))  # 輸出: 15
print(calculator("除", 10, 0))  # 輸出: 錯誤：不能除以零
```

---

## 總結與 Q&A

我們已經涵蓋了 Python 函式的基本概念！

- **函式定義**：使用 `def` 關鍵字建立可重複使用的程式碼區塊。
- **參數與回傳值**：函式可以接收輸入並回傳結果。
- **變數範圍**：了解區域變數和全域變數的差異。
- **內建函式**：善用 Python 提供的內建函式和模組。

有任何問題嗎？
