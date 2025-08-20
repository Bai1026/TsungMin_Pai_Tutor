# Python 新手指南：05 錯誤處理與除錯

**作者：** Tsung-Min Pai  
**單位：** NTUEE

---

## 大綱

### 1 錯誤類型 (Error Types)

- 語法錯誤
- 執行時期錯誤
- 邏輯錯誤

### 2 例外處理 (Exception Handling)

- try/except 語句
- finally 語句
- else 語句

### 3 常見例外類型

- ValueError
- TypeError
- IndexError
- KeyError

### 4 除錯技巧 (Debugging)

- print() 除錯
- 使用除錯器
- 程式碼檢查

---

## 錯誤類型 (Error Types)

程式設計過程中會遇到三種主要的錯誤類型：

**語法錯誤 (Syntax Errors)：**

- 程式碼不符合 Python 語法規則
- 程式無法執行

**執行時期錯誤 (Runtime Errors)：**

- 程式碼語法正確，但執行時發生錯誤
- 也稱為例外 (Exceptions)

**邏輯錯誤 (Logic Errors)：**

- 程式碼可以執行，但結果不如預期
- 最難發現和修正的錯誤類型

---

## 語法錯誤範例

```python
# 語法錯誤範例
print("Hello World"  # 缺少右括號
# SyntaxError: unexpected EOF while parsing

if True  # 缺少冒號
    print("條件為真")
# SyntaxError: invalid syntax

def my_function()
    return "Hello"  # 缺少冒號
# SyntaxError: invalid syntax
```

---

## 執行時期錯誤範例

```python
# 除零錯誤
result = 10 / 0
# ZeroDivisionError: division by zero

# 索引超出範圍
my_list = [1, 2, 3]
print(my_list[5])
# IndexError: list index out of range

# 類型錯誤
number = "123"
result = number + 5
# TypeError: can only concatenate str (not "int") to str
```

---

## 例外處理 (Exception Handling)

使用 `try/except` 語句來處理可能發生的錯誤：

**基本語法：**

```python
try:
    # 可能發生錯誤的程式碼
    pass
except:
    # 處理錯誤的程式碼
    pass
```

**實際範例：**

```python
try:
    number = int(input("請輸入一個數字："))
    result = 10 / number
    print(f"結果是：{result}")
except:
    print("發生錯誤！")
```

---

## 捕捉特定例外

**捕捉特定例外類型：**

```python
try:
    number = int(input("請輸入一個數字："))
    result = 10 / number
    print(f"結果是：{result}")
except ValueError:
    print("請輸入有效的數字！")
except ZeroDivisionError:
    print("不能除以零！")
```

**捕捉多種例外：**

```python
try:
    # 一些程式碼
    pass
except (ValueError, TypeError) as e:
    print(f"發生錯誤：{e}")
```

---

## finally 和 else 語句

**finally 語句：**

```python
try:
    file = open("data.txt", "r")
    content = file.read()
except FileNotFoundError:
    print("檔案不存在！")
finally:
    # 無論是否有錯誤都會執行
    print("清理資源")
    if 'file' in locals():
        file.close()
```

**else 語句：**

```python
try:
    number = int(input("請輸入一個數字："))
except ValueError:
    print("無效的數字！")
else:
    # 沒有例外時執行
    print(f"您輸入的數字是：{number}")
finally:
    print("程式結束")
```

---

## 常見例外類型

**ValueError：**

```python
try:
    age = int("abc")  # 無法轉換為整數
except ValueError as e:
    print(f"數值錯誤：{e}")
```

**TypeError：**

```python
try:
    result = "Hello" + 123  # 字串無法與整數相加
except TypeError as e:
    print(f"類型錯誤：{e}")
```

**IndexError：**

```python
try:
    my_list = [1, 2, 3]
    print(my_list[10])  # 索引超出範圍
except IndexError as e:
    print(f"索引錯誤：{e}")
```

---

## 更多常見例外

**KeyError：**

```python
try:
    my_dict = {"name": "Tsung-min", "age": 25}
    print(my_dict["city"])  # 鍵不存在
except KeyError as e:
    print(f"鍵錯誤：{e}")
```

**FileNotFoundError：**

```python
try:
    with open("nonexistent.txt", "r") as file:
        content = file.read()
except FileNotFoundError as e:
    print(f"檔案錯誤：{e}")
```

**AttributeError：**

```python
try:
    my_string = "Hello"
    my_string.append("World")  # 字串沒有 append 方法
except AttributeError as e:
    print(f"屬性錯誤：{e}")
```

---

## 自訂例外

**建立自訂例外：**

```python
class CustomError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def check_age(age):
    if age < 0:
        raise CustomError("年齡不能為負數")
    elif age > 150:
        raise CustomError("年齡不能超過150歲")
    return True

try:
    check_age(-5)
except CustomError as e:
    print(f"自訂錯誤：{e}")
```

---

## 除錯技巧 (Debugging)

**使用 print() 除錯：**

```python
def calculate_average(numbers):
    print(f"輸入的數字：{numbers}")  # 除錯資訊

    total = sum(numbers)
    print(f"總和：{total}")  # 除錯資訊

    count = len(numbers)
    print(f"數量：{count}")  # 除錯資訊

    average = total / count
    return average

result = calculate_average([10, 20, 30])
print(f"平均值：{result}")
```

---

## 程式碼檢查技巧

**檢查資料類型：**

```python
def safe_divide(a, b):
    # 檢查輸入類型
    if not isinstance(a, (int, float)):
        raise TypeError("第一個參數必須是數字")
    if not isinstance(b, (int, float)):
        raise TypeError("第二個參數必須是數字")

    # 檢查除零
    if b == 0:
        raise ValueError("除數不能為零")

    return a / b

try:
    result = safe_divide(10, "2")
except (TypeError, ValueError) as e:
    print(f"錯誤：{e}")
```

---

## 最佳實務

**具體的例外處理：**

```python
# 好的做法
try:
    user_input = input("請輸入數字：")
    number = int(user_input)
    result = 100 / number
except ValueError:
    print("請輸入有效的整數")
except ZeroDivisionError:
    print("數字不能為零")

# 避免的做法
try:
    # 一堆程式碼
    pass
except:  # 捕捉所有例外
    print("發生錯誤")  # 太籠統
```

---

## 實用範例：檔案處理

**安全的檔案處理：**

```python
def read_config_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"設定檔 {filename} 不存在")
        return None
    except PermissionError:
        print(f"沒有權限讀取 {filename}")
        return None
    except UnicodeDecodeError:
        print(f"檔案 {filename} 編碼錯誤")
        return None
    except Exception as e:
        print(f"讀取檔案時發生未知錯誤：{e}")
        return None

# 使用範例
config = read_config_file("config.txt")
if config:
    print("設定檔讀取成功")
else:
    print("使用預設設定")
```

---

## 總結與 Q&A

我們已經涵蓋了 Python 錯誤處理的重要概念！

- **錯誤類型**：了解語法錯誤、執行時期錯誤和邏輯錯誤。
- **例外處理**：使用 `try/except/finally/else` 處理錯誤。
- **常見例外**：熟悉 Python 中常見的例外類型。
- **除錯技巧**：學會使用各種除錯方法找出問題。

有任何問題嗎？
