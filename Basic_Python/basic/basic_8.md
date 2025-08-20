# Python 新手指南：08 模組與套件

**作者：** tsung-min pai  
**單位：** NTUEE

---

## 大綱

### 1 模組 (Modules)

- 模組的概念
- 匯入模組
- 建立自訂模組

### 2 套件 (Packages)

- 套件的結構
- **init**.py 檔案
- 套件的匯入

### 3 標準函式庫

- 常用內建模組
- datetime 模組
- random 模組
- os 模組

### 4 第三方套件管理

- pip 套件管理器
- virtual environment
- requirements.txt

---

## 模組 (Modules)

**什麼是模組？**

- 模組是包含 Python 程式碼的檔案
- 可以定義函式、類別和變數
- 允許程式碼重用和組織

**為什麼要使用模組？**

- **程式碼重用**：避免重複撰寫相同的程式碼
- **組織性**：將相關功能分組
- **命名空間**：避免變數名稱衝突
- **可維護性**：easier to maintain and debug

```python
# 範例：math 模組的使用
import math

print(math.pi)        # 圓周率
print(math.sqrt(16))  # 平方根
print(math.sin(math.pi/2))  # 正弦函式
```

---

## 匯入模組的方法

**方法 1：匯入整個模組**

```python
import math
result = math.sqrt(25)
print(result)  # 5.0
```

**方法 2：匯入特定函式**

```python
from math import sqrt, pi
result = sqrt(25)
print(result)  # 5.0
print(pi)     # 3.141592653589793
```

**方法 3：使用別名**

```python
import math as m
result = m.sqrt(25)
print(result)  # 5.0

# 或是給函式取別名
from math import sqrt as square_root
result = square_root(25)
print(result)  # 5.0
```

**方法 4：匯入所有內容 (不建議)**

```python
from math import *
result = sqrt(25)  # 可以直接使用，但可能造成命名衝突
```

---

## 建立自訂模組

**建立 calculator.py 模組：**

```python
# calculator.py
"""
簡單的計算機模組
提供基本的數學運算函式
"""

def add(a, b):
    """加法函式"""
    return a + b

def subtract(a, b):
    """減法函式"""
    return a - b

def multiply(a, b):
    """乘法函式"""
    return a * b

def divide(a, b):
    """除法函式"""
    if b != 0:
        return a / b
    else:
        raise ValueError("除數不能為零")

# 模組變數
PI = 3.14159

# 模組層級的程式碼
print(f"Calculator 模組已載入，PI = {PI}")
```

**使用自訂模組：**

```python
# main.py
import calculator

# 使用模組中的函式
result1 = calculator.add(10, 5)
result2 = calculator.multiply(3, 4)

print(f"10 + 5 = {result1}")
print(f"3 × 4 = {result2}")
print(f"PI = {calculator.PI}")

# 或使用 from import
from calculator import add, subtract

result3 = add(20, 10)
result4 = subtract(20, 10)
print(f"20 + 10 = {result3}")
print(f"20 - 10 = {result4}")
```

---

## 模組搜尋路徑

**Python 如何找到模組：**

```python
import sys

# 檢視模組搜尋路徑
for path in sys.path:
    print(path)

# 新增自訂路徑
sys.path.append('/path/to/your/modules')
```

**檢查模組位置：**

```python
import math
print(math.__file__)  # 顯示模組檔案位置

import calculator
print(calculator.__doc__)  # 顯示模組說明文件
```

---

## 套件 (Packages)

**什麼是套件？**

- 套件是包含多個模組的目錄
- 必須包含 `__init__.py` 檔案
- 可以建立階層式的模組結構

**套件結構範例：**

```
mypackage/
    __init__.py
    math_utils/
        __init__.py
        basic.py
        advanced.py
    string_utils/
        __init__.py
        formatter.py
        validator.py
```

---

## 建立套件

**建立 math_utils 套件：**

**math_utils/**init**.py：**

```python
"""
數學工具套件
"""
print("Math Utils 套件已載入")

# 可以在這裡定義套件層級的變數和函式
__version__ = "1.0.0"
__author__ = "Tsung-min Pai"
```

**math_utils/basic.py：**

```python
"""
基本數學運算
"""

def power(base, exponent):
    """計算次方"""
    return base ** exponent

def factorial(n):
    """計算階乘"""
    if n < 0:
        raise ValueError("階乘不能為負數")
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def is_prime(n):
    """檢查是否為質數"""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True
```

**math_utils/advanced.py：**

```python
"""
進階數學運算
"""
import math

def gcd(a, b):
    """計算最大公因數"""
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    """計算最小公倍數"""
    return abs(a * b) // gcd(a, b)

def distance(point1, point2):
    """計算兩點間距離"""
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
```

---

## 使用套件

**匯入套件中的模組：**

```python
# 方法 1：匯入特定模組
from math_utils import basic

result1 = basic.power(2, 3)
result2 = basic.factorial(5)
print(f"2^3 = {result1}")
print(f"5! = {result2}")

# 方法 2：匯入特定函式
from math_utils.basic import power, is_prime
from math_utils.advanced import gcd, distance

print(f"3^4 = {power(3, 4)}")
print(f"17 是質數: {is_prime(17)}")
print(f"gcd(12, 8) = {gcd(12, 8)}")
print(f"距離: {distance((0, 0), (3, 4))}")

# 方法 3：使用套件資訊
import math_utils
print(f"套件版本: {math_utils.__version__}")
print(f"作者: {math_utils.__author__}")
```

---

## 常用標準函式庫

**datetime 模組：**

```python
import datetime

# 取得當前時間
now = datetime.datetime.now()
print(f"現在時間: {now}")

# 建立特定日期
birthday = datetime.date(1995, 5, 15)
print(f"生日: {birthday}")

# 日期運算
today = datetime.date.today()
age_days = today - birthday
print(f"活了 {age_days.days} 天")

# 格式化日期
formatted_date = now.strftime("%Y年%m月%d日 %H:%M:%S")
print(f"格式化日期: {formatted_date}")

# 解析字串為日期
date_string = "2023-12-25"
parsed_date = datetime.datetime.strptime(date_string, "%Y-%m-%d")
print(f"解析的日期: {parsed_date}")
```

---

## random 模組

```python
import random

# 產生隨機數
print(f"0-1之間的隨機數: {random.random()}")
print(f"1-10之間的整數: {random.randint(1, 10)}")
print(f"1-100之間的浮點數: {random.uniform(1, 100)}")

# 從序列中隨機選擇
colors = ["紅", "綠", "藍", "黃", "紫"]
print(f"隨機顏色: {random.choice(colors)}")

# 隨機抽樣
numbers = list(range(1, 11))
sample = random.sample(numbers, 3)
print(f"隨機抽樣3個數字: {sample}")

# 打亂列表
deck = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
random.shuffle(deck)
print(f"洗牌後: {deck}")

# 設定隨機種子（用於重現結果）
random.seed(42)
print(f"固定種子的隨機數: {random.randint(1, 100)}")
```

---

## os 模組

```python
import os

# 取得當前工作目錄
current_dir = os.getcwd()
print(f"當前目錄: {current_dir}")

# 列出目錄內容
files = os.listdir(".")
print(f"當前目錄檔案: {files}")

# 檢查檔案/目錄是否存在
if os.path.exists("example.txt"):
    print("檔案存在")
else:
    print("檔案不存在")

# 取得檔案資訊
if os.path.exists("example.txt"):
    file_size = os.path.getsize("example.txt")
    print(f"檔案大小: {file_size} 位元組")

# 建立目錄
if not os.path.exists("new_folder"):
    os.mkdir("new_folder")
    print("目錄已建立")

# 環境變數
home_dir = os.environ.get("HOME", "未找到HOME變數")
print(f"家目錄: {home_dir}")

# 路徑操作
file_path = os.path.join("folder", "subfolder", "file.txt")
print(f"組合路徑: {file_path}")

# 分離路徑和檔名
directory, filename = os.path.split(file_path)
print(f"目錄: {directory}, 檔名: {filename}")
```

---

## 第三方套件管理

**使用 pip 安裝套件：**

```bash
# 安裝套件
pip install requests
pip install numpy
pip install pandas

# 安裝特定版本
pip install django==3.2.0

# 升級套件
pip upgrade requests

# 解除安裝套件
pip uninstall requests

# 列出已安裝套件
pip list

# 顯示套件資訊
pip show numpy
```

**使用 requirements.txt：**

```bash
# 產生 requirements.txt
pip freeze > requirements.txt

# 從 requirements.txt 安裝
pip install -r requirements.txt
```

**requirements.txt 範例：**

```
numpy==1.21.0
pandas==1.3.0
requests==2.25.1
matplotlib==3.4.2
```

---

## Virtual Environment (虛擬環境)

**為什麼需要虛擬環境？**

- 隔離不同專案的相依套件
- 避免版本衝突
- 方便部署

**建立和使用虛擬環境：**

```bash
# 建立虛擬環境
python -m venv myproject_env

# 啟動虛擬環境 (Windows)
myproject_env\Scripts\activate

# 啟動虛擬環境 (macOS/Linux)
source myproject_env/bin/activate

# 停用虛擬環境
deactivate

# 刪除虛擬環境
rm -rf myproject_env
```

---

## 實用範例：專案結構

**建立一個完整的專案結構：**

```
my_project/
    requirements.txt
    main.py
    config/
        __init__.py
        settings.py
    utils/
        __init__.py
        file_handler.py
        data_processor.py
    tests/
        __init__.py
        test_utils.py
```

**utils/file_handler.py：**

```python
"""
檔案處理工具
"""
import os
import json

def read_json_file(filepath):
    """讀取 JSON 檔案"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"檔案 {filepath} 不存在")
        return None
    except json.JSONDecodeError:
        print(f"檔案 {filepath} 不是有效的 JSON 格式")
        return None

def write_json_file(filepath, data):
    """寫入 JSON 檔案"""
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"寫入檔案時發生錯誤: {e}")
        return False

def ensure_directory(directory):
    """確保目錄存在"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"目錄 {directory} 已建立")
```

**main.py：**

```python
"""
主程式
"""
from utils.file_handler import read_json_file, write_json_file
from config.settings import DEFAULT_CONFIG

def main():
    # 讀取設定檔
    config = read_json_file("config.json")
    if config is None:
        config = DEFAULT_CONFIG
        write_json_file("config.json", config)
        print("已建立預設設定檔")

    print("程式開始執行...")
    print(f"設定: {config}")

if __name__ == "__main__":
    main()
```

---

## 最佳實務

**模組和套件的命名慣例：**

- 使用小寫字母和底線
- 避免與內建模組同名
- 選擇有意義的名稱

**良好的模組結構：**

```python
"""
模組說明文件
"""

# 匯入標準函式庫
import os
import sys

# 匯入第三方函式庫
import requests
import numpy as np

# 匯入本地模組
from .utils import helper_function

# 模組層級常數
DEFAULT_TIMEOUT = 30

# 模組層級變數
_private_variable = "私有變數"

# 函式定義
def public_function():
    """公開函式"""
    pass

def _private_function():
    """私有函式"""
    pass

# 主要執行程式碼
if __name__ == "__main__":
    # 只有直接執行此模組時才會執行
    print("模組被直接執行")
```

---

## 總結與 Q&A

我們已經涵蓋了 Python 模組與套件的重要概念！

- **模組**：學會建立和使用模組來組織程式碼。
- **套件**：了解如何建立套件結構和使用 `__init__.py`。
- **標準函式庫**：熟悉常用的內建模組如 datetime、random、os。
- **套件管理**：掌握 pip 和虛擬環境的使用。

有任何問題嗎？
