# Python 新手指南：06 檔案處理與資料輸入輸出

**作者：** Tsung-Min Pai  
**單位：** NTUEE

---

## 大綱

### 1 檔案基礎操作

- 開啟與關閉檔案
- 讀取檔案內容
- 寫入檔案內容

### 2 檔案模式與編碼

- 不同的檔案模式
- 文字編碼處理
- 二進位檔案操作

### 3 CSV 檔案處理

- 讀取 CSV 檔案
- 寫入 CSV 檔案
- 使用 csv 模組

### 4 JSON 資料處理

- JSON 格式介紹
- 讀取與寫入 JSON
- 資料轉換

---

## 檔案基礎操作

**開啟檔案：**

```python
# 基本語法
file = open("filename.txt", "mode")
# 使用完畢後記得關閉
file.close()
```

**安全的檔案操作 (推薦)：**

```python
# 使用 with 語句，自動關閉檔案
with open("filename.txt", "r") as file:
    content = file.read()
    print(content)
# 離開 with 區塊時自動關閉檔案
```

---

## 讀取檔案內容

**讀取整個檔案：**

```python
with open("data.txt", "r", encoding="utf-8") as file:
    content = file.read()
    print(content)
```

**逐行讀取：**

```python
with open("data.txt", "r", encoding="utf-8") as file:
    for line in file:
        print(line.strip())  # strip() 移除換行符號
```

**讀取所有行到列表：**

```python
with open("data.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()
    for line in lines:
        print(line.strip())
```

---

## 寫入檔案內容

**寫入文字檔案：**

```python
# 覆寫模式 (會清空原有內容)
with open("output.txt", "w", encoding="utf-8") as file:
    file.write("Hello, World!\n")
    file.write("這是第二行\n")
```

**附加模式：**

```python
# 附加模式 (在檔案結尾新增內容)
with open("output.txt", "a", encoding="utf-8") as file:
    file.write("這是新增的內容\n")
```

**寫入多行：**

```python
lines = ["第一行\n", "第二行\n", "第三行\n"]
with open("output.txt", "w", encoding="utf-8") as file:
    file.writelines(lines)
```

---

## 檔案模式與編碼

**常用檔案模式：**

| 模式 | 描述       | 用途                     |
| ---- | ---------- | ------------------------ |
| "r"  | 讀取模式   | 讀取現有檔案             |
| "w"  | 寫入模式   | 建立新檔案或覆寫現有檔案 |
| "a"  | 附加模式   | 在檔案結尾新增內容       |
| "r+" | 讀寫模式   | 讀取和寫入現有檔案       |
| "rb" | 二進位讀取 | 讀取二進位檔案           |
| "wb" | 二進位寫入 | 寫入二進位檔案           |

**編碼處理：**

```python
# 指定編碼 (建議做法)
with open("chinese.txt", "r", encoding="utf-8") as file:
    content = file.read()

# 處理編碼錯誤
try:
    with open("data.txt", "r", encoding="utf-8") as file:
        content = file.read()
except UnicodeDecodeError:
    # 嘗試其他編碼
    with open("data.txt", "r", encoding="big5") as file:
        content = file.read()
```

---

## 實用檔案操作

**檢查檔案是否存在：**

```python
import os

filename = "data.txt"
if os.path.exists(filename):
    print(f"檔案 {filename} 存在")
    with open(filename, "r") as file:
        content = file.read()
else:
    print(f"檔案 {filename} 不存在")
```

**取得檔案資訊：**

```python
import os

filename = "data.txt"
if os.path.exists(filename):
    file_size = os.path.getsize(filename)
    print(f"檔案大小：{file_size} 位元組")

    # 取得修改時間
    import time
    mod_time = os.path.getmtime(filename)
    readable_time = time.ctime(mod_time)
    print(f"最後修改時間：{readable_time}")
```

---

## CSV 檔案處理

**CSV 檔案範例 (students.csv)：**

```
姓名,年齡,科系
張小明,20,資訊工程
李小華,21,電機工程
王小美,19,機械工程
```

**讀取 CSV 檔案：**

```python
import csv

with open("students.csv", "r", encoding="utf-8") as file:
    csv_reader = csv.reader(file)

    # 讀取標題行
    headers = next(csv_reader)
    print(f"欄位：{headers}")

    # 讀取資料行
    for row in csv_reader:
        print(f"姓名：{row[0]}, 年齡：{row[1]}, 科系：{row[2]}")
```

---

## CSV 字典讀取

**使用 DictReader：**

```python
import csv

with open("students.csv", "r", encoding="utf-8") as file:
    csv_reader = csv.DictReader(file)

    for row in csv_reader:
        print(f"姓名：{row['姓名']}")
        print(f"年齡：{row['年齡']}")
        print(f"科系：{row['科系']}")
        print("-" * 20)
```

**寫入 CSV 檔案：**

```python
import csv

students = [
    ["陳小明", 22, "化學工程"],
    ["林小雅", 20, "生物醫學"],
    ["黃小強", 21, "土木工程"]
]

with open("new_students.csv", "w", newline="", encoding="utf-8") as file:
    csv_writer = csv.writer(file)

    # 寫入標題
    csv_writer.writerow(["姓名", "年齡", "科系"])

    # 寫入資料
    csv_writer.writerows(students)
```

---

## JSON 資料處理

**JSON 格式範例：**

```json
{
  "name": "張小明",
  "age": 25,
  "skills": ["Python", "JavaScript", "HTML"],
  "is_student": true,
  "address": {
    "city": "台北",
    "district": "信義區"
  }
}
```

**讀取 JSON 檔案：**

```python
import json

with open("person.json", "r", encoding="utf-8") as file:
    data = json.load(file)

    print(f"姓名：{data['name']}")
    print(f"年齡：{data['age']}")
    print(f"技能：{', '.join(data['skills'])}")
    print(f"城市：{data['address']['city']}")
```

---

## JSON 資料寫入

**寫入 JSON 檔案：**

```python
import json

# 準備資料
person_data = {
    "name": "李小華",
    "age": 23,
    "skills": ["Java", "C++", "SQL"],
    "is_student": False,
    "grades": {
        "math": 95,
        "english": 88,
        "science": 92
    }
}

# 寫入 JSON 檔案
with open("person_output.json", "w", encoding="utf-8") as file:
    json.dump(person_data, file, ensure_ascii=False, indent=2)
```

**JSON 字串處理：**

```python
import json

# Python 物件轉 JSON 字串
data = {"name": "王小美", "age": 24}
json_string = json.dumps(data, ensure_ascii=False)
print(json_string)

# JSON 字串轉 Python 物件
json_string = '{"name": "陳小明", "age": 26}'
data = json.loads(json_string)
print(data["name"])
```

---

## 實用範例：學生成績管理

**建立學生成績檔案：**

```python
import json

def save_student_data(filename, students):
    """儲存學生資料到 JSON 檔案"""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(students, file, ensure_ascii=False, indent=2)
        print(f"學生資料已儲存到 {filename}")
    except Exception as e:
        print(f"儲存失敗：{e}")

def load_student_data(filename):
    """從 JSON 檔案載入學生資料"""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"檔案 {filename} 不存在")
        return []
    except Exception as e:
        print(f"載入失敗：{e}")
        return []

# 範例資料
students = [
    {
        "name": "張小明",
        "id": "B10901001",
        "grades": {"數學": 95, "英文": 88, "物理": 92}
    },
    {
        "name": "李小華",
        "id": "B10901002",
        "grades": {"數學": 87, "英文": 94, "物理": 89}
    }
]

# 儲存和載入
save_student_data("students.json", students)
loaded_students = load_student_data("students.json")

for student in loaded_students:
    print(f"學生：{student['name']}")
    avg_grade = sum(student['grades'].values()) / len(student['grades'])
    print(f"平均分數：{avg_grade:.1f}")
```

---

## 檔案路徑處理

**使用 pathlib (推薦)：**

```python
from pathlib import Path

# 建立路徑物件
file_path = Path("data") / "students.txt"

# 檢查檔案是否存在
if file_path.exists():
    print("檔案存在")

# 建立目錄
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)  # exist_ok=True 避免目錄已存在時出錯

# 取得檔案資訊
if file_path.exists():
    print(f"檔案名稱：{file_path.name}")
    print(f"副檔名：{file_path.suffix}")
    print(f"父目錄：{file_path.parent}")
```

---

## 錯誤處理與最佳實務

**安全的檔案操作：**

```python
def safe_read_file(filename):
    """安全地讀取檔案"""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"錯誤：檔案 {filename} 不存在")
        return None
    except PermissionError:
        print(f"錯誤：沒有權限讀取 {filename}")
        return None
    except UnicodeDecodeError:
        print(f"錯誤：檔案 {filename} 編碼問題")
        return None
    except Exception as e:
        print(f"未知錯誤：{e}")
        return None

def safe_write_file(filename, content):
    """安全地寫入檔案"""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"成功寫入 {filename}")
        return True
    except PermissionError:
        print(f"錯誤：沒有權限寫入 {filename}")
        return False
    except Exception as e:
        print(f"寫入失敗：{e}")
        return False

# 使用範例
content = safe_read_file("example.txt")
if content:
    print("檔案內容：", content)

success = safe_write_file("output.txt", "測試內容")
if success:
    print("檔案寫入成功")
```

---

## 總結與 Q&A

我們已經涵蓋了 Python 檔案處理的重要概念！

- **檔案基礎操作**：使用 `with` 語句安全地開啟和關閉檔案。
- **不同格式處理**：處理純文字、CSV 和 JSON 檔案。
- **編碼與錯誤處理**：正確處理中文編碼和各種例外情況。
- **實用技巧**：檔案路徑處理和最佳實務。

有任何問題嗎？
