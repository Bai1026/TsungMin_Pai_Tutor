# Python 新手指南：01 變數、資料型態、語法

**作者：** Tsung-Min Pai  
**單位：** NTUEE

---

## 大綱

### 1 變數

- 定義
- 宣告與初始化
- 賦值
- 命名慣例

### 2 資料型態

### 3 語法

- print()
- input()
- 運算子

### 4 進階 print() 技巧

- f-string 格式化
- rich 函式庫
- JSON 格式輸出
- 除錯技巧

---

## print()

- 用於將資料輸出到標準輸出設備，通常是終端機或命令提示字元。
- 這是一個內建函式，用於向使用者顯示訊息或進行除錯。

```python
# 印出一個字串
print("Python 很有趣！")

# 印出變數的值
name = "Tsung-min"
print(name)
```

---

## f-string 格式化

**f-string 是 Python 3.6+ 的現代字串格式化方法：**

```python
# 基本 f-string 用法
name = "Tsung-min"
age = 25
print(f"我是 {name}，今年 {age} 歲")  # 輸出: 我是 Tsung-min，今年 25 歲

# 在 f-string 中進行計算
price = 100
quantity = 3
print(f"總價是 {price * quantity} 元")  # 輸出: 總價是 300 元

# 格式化數字
pi = 3.14159
print(f"圓周率約為 {pi:.2f}")  # 輸出: 圓周率約為 3.14

# 格式化百分比
score = 0.85
print(f"及格率：{score:.1%}")  # 輸出: 及格率：85.0%
```

**與舊式格式化的比較：**

```python
name = "王小明"
score = 95

# 舊式方法 (較複雜)
print("學生 %s 的分數是 %d" % (name, score))

# .format() 方法
print("學生 {} 的分數是 {}".format(name, score))

# f-string (推薦)
print(f"學生 {name} 的分數是 {score}")
```

---

## rich 函式庫的 print()

**安裝 rich：**

```bash
pip install rich
```

**rich.print() 與一般 print() 的差異：**

```python
# 一般的 print()
print("這是普通的文字")
print({"name": "張三", "age": 25, "skills": ["Python", "JavaScript"]})

# 從 rich 匯入 print
from rich import print

# rich 的 print() 有更好的顯示效果
print("這是 [bold red]粗體紅色[/bold red] 文字")
print({"name": "張三", "age": 25, "skills": ["Python", "JavaScript"]})

# rich 自動美化資料結構
data = {
    "使用者資訊": {
        "姓名": "李小華",
        "年齡": 22,
        "技能": ["Python", "機器學習", "資料分析"],
        "專案": [
            {"名稱": "網站開發", "完成": True},
            {"名稱": "AI 聊天機器人", "完成": False}
        ]
    }
}
print(data)  # rich 會自動產生彩色、縮排的輸出
```

---

## JSON 格式輸出展示

**使用 json.dumps() 美化輸出：**

```python
import json

# 複雜的資料結構
student_data = {
    "基本資訊": {
        "姓名": "陳小美",
        "學號": "B10901001",
        "科系": "資訊工程學系"
    },
    "成績": {
        "數學": 95,
        "英文": 88,
        "程式設計": 92
    },
    "選修課程": ["機器學習", "資料結構", "演算法"]
}

# 一般 print (較難閱讀)
print("一般 print:")
print(student_data)

print("\n" + "="*50 + "\n")

# JSON 格式化輸出 (較易閱讀)
print("JSON 格式化輸出:")
print(json.dumps(student_data, ensure_ascii=False, indent=2))

print("\n" + "="*50 + "\n")

# rich print (最美觀)
from rich import print as rprint
print("Rich print 輸出:")
rprint(student_data)
```

---

## 新手常見的 print() 錯誤

**錯誤 1：忘記換行符號**

```python
# 錯誤：沒有換行，輸出會擠在一起
print("第一行", end="")
print("第二行")
# 輸出: 第一行第二行

# 正確：明確加入換行符號
print("第一行")
print("第二行")
# 輸出:
# 第一行
# 第二行

# 或者使用 \n
print("第一行\n第二行")
```

**錯誤 2：字串與變數連接類型錯誤**

```python
name = "小明"
age = 20

# 錯誤：無法直接串接字串和數字
# print("我是" + name + "，今年" + age + "歲")  # TypeError

# 正確方法 1：轉換類型
print("我是" + name + "，今年" + str(age) + "歲")

# 正確方法 2：使用逗號分隔
print("我是", name, "，今年", age, "歲")

# 正確方法 3：使用 f-string (推薦)
print(f"我是{name}，今年{age}歲")
```

**錯誤 3：引號配對錯誤**

```python
# 錯誤：引號不匹配
# print("Hello World')  # SyntaxError

# 正確
print("Hello World")
print('Hello World')

# 字串中包含引號的處理
print("他說：'今天天氣很好'")
print('他說："今天天氣很好"')
print("他說：\"今天天氣很好\"")  # 使用跳脫字元
```

**錯誤 4：忘記括號**

```python
# 錯誤：Python 3 必須使用括號
# print "Hello World"  # SyntaxError

# 正確
print("Hello World")
```

---

## 除錯技巧

**技巧 1：使用 print(0/0) 快速除錯**

```python
def calculate_something():
    x = 10
    y = 20

    print(0/0)  # 這會立即停止程式並顯示錯誤，用來檢查程式執行到這裡

    result = x + y
    return result

# 當你想知道程式是否執行到某個位置時，使用 print(0/0)
# 程式會在這裡停止並顯示 ZeroDivisionError
```

**技巧 2：使用 print() 追蹤變數值**

```python
def debug_example():
    numbers = [1, 2, 3, 4, 5]
    total = 0

    for i, num in enumerate(numbers):
        print(f"第 {i+1} 次迴圈: num={num}, total={total}")  # 追蹤變數
        total += num
        print(f"  加法後: total={total}")  # 追蹤計算結果

    return total

result = debug_example()
print(f"最終結果: {result}")
```

**技巧 3：使用分隔線讓輸出更清楚**

```python
print("=" * 50)
print("開始處理資料")
print("=" * 50)

# 你的程式碼

print("-" * 30)
print("處理完成")
print("-" * 30)
```

**技巧 4：print() 的進階參數**

```python
# end 參數：控制結尾字元
print("載入中", end="")
for i in range(3):
    print(".", end="")
print(" 完成!")  # 輸出: 載入中... 完成!

# sep 參數：控制分隔字元
print("蘋果", "香蕉", "橘子", sep=" | ")  # 輸出: 蘋果 | 香蕉 | 橘子

# file 參數：輸出到檔案
with open("log.txt", "w") as file:
    print("這是日誌訊息", file=file)  # 輸出到檔案而不是終端機
```

---

## 實用的 print() 格式化範例

```python
# 表格式輸出
print(f"{'姓名':<10} {'年齡':<5} {'科系':<15}")
print("-" * 35)
print(f"{'張小明':<10} {20:<5} {'資訊工程':<15}")
print(f"{'李小華':<10} {21:<5} {'電機工程':<15}")

# 進度顯示
total = 100
current = 45
percentage = current / total * 100
bar_length = 20
filled_length = int(bar_length * current // total)
bar = "█" * filled_length + "░" * (bar_length - filled_length)
print(f"進度: |{bar}| {percentage:.1f}% ({current}/{total})")

# 多行字串輸出
text = """
這是一個多行字串的範例，
可以包含多行內容，
保持原有的格式和縮排。
"""
print(text)
```

---

## 註解 (Comments)

在程式碼中，註解用於解釋程式碼的功能，對編譯器來說是無效的。單行註解使用 `#` 開頭。

```python
# 這是一個單行註解
name = "Tsung-min"  # 這個變數儲存使用者的名字
print(name)
```

---

## 多行註解

多行註解通常用於解釋較複雜的程式碼區塊或函式。在 Python 中，多行註解可以使用三個雙引號或單引號來建立。

```python
"""
這是一個多行註解的範例。
它可以用來解釋程式碼區塊的作用。
這個區塊計算圓的面積和周長。
"""

radius = 5
area = 3.14 * radius * radius
circumference = 2 * 3.14 * radius

print("圓的面積:", area)
print("圓的周長:", circumference)
```
