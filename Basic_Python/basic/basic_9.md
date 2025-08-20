# Python 新手指南：09 資料結構進階應用

**作者：** tsung-min pai  
**單位：** NTUEE

---

## 大綱

### 1 進階串列操作

- 串列推導式
- 多維串列
- 串列的進階方法

### 2 字典進階技巧

- 字典推導式
- 預設字典
- 有序字典

### 3 集合與元組應用

- 集合運算
- 具名元組
- 凍結集合

### 4 資料結構最佳實務

- 效能比較
- 記憶體使用
- 選擇適當的資料結構

---

## 進階串列操作

**串列推導式 (List Comprehensions)：**

```python
# 基本語法：[expression for item in iterable if condition]

# 基本範例
numbers = [1, 2, 3, 4, 5]
squares = [x**2 for x in numbers]
print(squares)  # [1, 4, 9, 16, 25]

# 帶條件的推導式
even_squares = [x**2 for x in numbers if x % 2 == 0]
print(even_squares)  # [4, 16]

# 處理字串
words = ["python", "java", "javascript", "go"]
upper_words = [word.upper() for word in words if len(word) > 4]
print(upper_words)  # ['PYTHON', 'JAVASCRIPT']

# 巢狀推導式
matrix = [[i*j for j in range(1, 4)] for i in range(1, 4)]
print(matrix)  # [[1, 2, 3], [2, 4, 6], [3, 6, 9]]
```

**多維串列操作：**

```python
# 建立二維串列
rows, cols = 3, 4
matrix = [[0 for _ in range(cols)] for _ in range(rows)]
print(matrix)  # [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

# 避免的錯誤做法
# wrong_matrix = [[0] * cols] * rows  # 所有行都指向同一個串列物件

# 填充資料
for i in range(rows):
    for j in range(cols):
        matrix[i][j] = i * cols + j + 1

print(matrix)  # [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]

# 矩陣轉置
transposed = [[matrix[i][j] for i in range(rows)] for j in range(cols)]
print(transposed)  # [[1, 5, 9], [2, 6, 10], [3, 7, 11], [4, 8, 12]]

# 使用 zip 轉置（更簡潔）
transposed_zip = list(zip(*matrix))
print(transposed_zip)  # [(1, 5, 9), (2, 6, 10), (3, 7, 11), (4, 8, 12)]
```

**串列的進階方法：**

```python
# 擴展串列
list1 = [1, 2, 3]
list2 = [4, 5, 6]
list1.extend(list2)
print(list1)  # [1, 2, 3, 4, 5, 6]

# 插入元素
numbers = [1, 3, 5]
numbers.insert(1, 2)  # 在索引 1 插入 2
print(numbers)  # [1, 2, 3, 5]

# 移除元素的不同方法
numbers = [1, 2, 3, 2, 4, 2, 5]
numbers.remove(2)      # 移除第一個 2
print(numbers)         # [1, 3, 2, 4, 2, 5]

popped = numbers.pop() # 移除並回傳最後一個元素
print(popped)          # 5
print(numbers)         # [1, 3, 2, 4, 2]

del numbers[1]         # 刪除指定索引的元素
print(numbers)         # [1, 2, 4, 2]

# 計數和搜尋
count_2 = numbers.count(2)
print(f"2 出現了 {count_2} 次")

index_2 = numbers.index(2)
print(f"2 第一次出現在索引 {index_2}")

# 反轉和排序
numbers.reverse()
print(numbers)  # [2, 4, 2, 1]

numbers.sort()
print(numbers)  # [1, 2, 2, 4]

# 清空串列
numbers.clear()
print(numbers)  # []
```

---

## 字典進階技巧

**字典推導式 (Dictionary Comprehensions)：**

```python
# 基本語法：{key_expression: value_expression for item in iterable if condition}

# 基本範例
numbers = [1, 2, 3, 4, 5]
squares_dict = {x: x**2 for x in numbers}
print(squares_dict)  # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# 從兩個串列建立字典
keys = ['name', 'age', 'city']
values = ['Alice', 25, 'Taipei']
person = {k: v for k, v in zip(keys, values)}
print(person)  # {'name': 'Alice', 'age': 25, 'city': 'Taipei'}

# 帶條件的字典推導式
words = ['apple', 'banana', 'cherry', 'date']
word_lengths = {word: len(word) for word in words if len(word) > 4}
print(word_lengths)  # {'apple': 5, 'banana': 6, 'cherry': 6}

# 轉換現有字典
original = {'a': 1, 'b': 2, 'c': 3}
doubled = {k: v*2 for k, v in original.items()}
print(doubled)  # {'a': 2, 'b': 4, 'c': 6}
```

**預設字典 (defaultdict)：**

```python
from collections import defaultdict

# 使用 defaultdict 避免 KeyError
# 傳統方法
word_count = {}
text = "hello world hello python world"
for word in text.split():
    if word in word_count:
        word_count[word] += 1
    else:
        word_count[word] = 1
print(word_count)  # {'hello': 2, 'world': 2, 'python': 1}

# 使用 defaultdict 簡化
word_count_default = defaultdict(int)  # 預設值為 0
for word in text.split():
    word_count_default[word] += 1
print(dict(word_count_default))  # {'hello': 2, 'world': 2, 'python': 1}

# 其他預設值類型
groups = defaultdict(list)  # 預設值為空串列
groups['fruits'].append('apple')
groups['fruits'].append('banana')
groups['vegetables'].append('carrot')
print(dict(groups))  # {'fruits': ['apple', 'banana'], 'vegetables': ['carrot']}

# 巢狀 defaultdict
nested = defaultdict(lambda: defaultdict(int))
nested['A']['x'] = 1
nested['A']['y'] = 2
nested['B']['z'] = 3
print(dict(nested))  # {'A': defaultdict(<class 'int'>, {'x': 1, 'y': 2}), 'B': defaultdict(<class 'int'>, {'z': 3})}
```

**有序字典 (OrderedDict)：**

```python
from collections import OrderedDict

# Python 3.7+ 的字典已經保持插入順序，但 OrderedDict 提供額外功能
ordered_dict = OrderedDict()
ordered_dict['first'] = 1
ordered_dict['second'] = 2
ordered_dict['third'] = 3

print(ordered_dict)  # OrderedDict([('first', 1), ('second', 2), ('third', 3)])

# 移動到末尾
ordered_dict.move_to_end('first')
print(ordered_dict)  # OrderedDict([('second', 2), ('third', 3), ('first', 1)])

# 移動到開頭
ordered_dict.move_to_end('third', last=False)
print(ordered_dict)  # OrderedDict([('third', 3), ('second', 2), ('first', 1)])

# 彈出最後或最前面的項目
last_item = ordered_dict.popitem(last=True)
print(last_item)  # ('first', 1)

first_item = ordered_dict.popitem(last=False)
print(first_item)  # ('third', 3)
```

---

## 集合與元組應用

**集合運算：**

```python
# 建立集合
set_a = {1, 2, 3, 4, 5}
set_b = {4, 5, 6, 7, 8}

# 聯集（所有元素）
union = set_a | set_b  # 或 set_a.union(set_b)
print(f"聯集: {union}")  # {1, 2, 3, 4, 5, 6, 7, 8}

# 交集（共同元素）
intersection = set_a & set_b  # 或 set_a.intersection(set_b)
print(f"交集: {intersection}")  # {4, 5}

# 差集（A 中有但 B 中沒有）
difference = set_a - set_b  # 或 set_a.difference(set_b)
print(f"差集 A-B: {difference}")  # {1, 2, 3}

# 對稱差集（不在交集中的元素）
symmetric_diff = set_a ^ set_b  # 或 set_a.symmetric_difference(set_b)
print(f"對稱差集: {symmetric_diff}")  # {1, 2, 3, 6, 7, 8}

# 子集和超集檢查
small_set = {2, 3}
print(f"{small_set} 是 {set_a} 的子集: {small_set.issubset(set_a)}")  # True
print(f"{set_a} 是 {small_set} 的超集: {set_a.issuperset(small_set)}")  # True

# 檢查是否無交集
set_c = {9, 10}
print(f"{set_a} 和 {set_c} 無交集: {set_a.isdisjoint(set_c)}")  # True
```

**具名元組 (namedtuple)：**

```python
from collections import namedtuple

# 建立具名元組類別
Point = namedtuple('Point', ['x', 'y'])
Student = namedtuple('Student', ['name', 'age', 'grade'])

# 建立實例
p1 = Point(3, 4)
p2 = Point(x=1, y=2)

student1 = Student('Alice', 20, 'A')
student2 = Student(name='Bob', age=21, grade='B')

# 存取方式
print(f"點 p1: x={p1.x}, y={p1.y}")  # 點 p1: x=3, y=4
print(f"學生: {student1.name}, 年齡: {student1.age}")  # 學生: Alice, 年齡: 20

# 具名元組是不可變的
# p1.x = 5  # 這會引發 AttributeError

# 建立新的具名元組（修改值）
p3 = p1._replace(x=5)
print(f"新點 p3: x={p3.x}, y={p3.y}")  # 新點 p3: x=5, y=4

# 轉換為字典
student_dict = student1._asdict()
print(student_dict)  # {'name': 'Alice', 'age': 20, 'grade': 'A'}

# 取得欄位名稱
print(Point._fields)  # ('x', 'y')
print(Student._fields)  # ('name', 'age', 'grade')
```

**凍結集合 (frozenset)：**

```python
# 建立不可變集合
mutable_set = {1, 2, 3, 4}
frozen = frozenset(mutable_set)

print(frozen)  # frozenset({1, 2, 3, 4})

# frozenset 可以作為字典的鍵或集合的元素
nested_sets = {
    frozenset([1, 2]): 'group_a',
    frozenset([3, 4]): 'group_b'
}
print(nested_sets)  # {frozenset({1, 2}): 'group_a', frozenset({3, 4}): 'group_b'}

# 集合運算仍然可用
frozen_a = frozenset([1, 2, 3])
frozen_b = frozenset([2, 3, 4])
intersection = frozen_a & frozen_b
print(intersection)  # frozenset({2, 3})
```

---

## 資料結構效能比較

**時間複雜度比較：**

```python
import time
import random

def time_operation(operation, data_size=100000):
    """測量操作的執行時間"""
    start_time = time.time()
    operation()
    end_time = time.time()
    return end_time - start_time

# 準備測試資料
test_data = list(range(100000))
random.shuffle(test_data)

# 串列 vs 集合的查找效能
test_list = test_data.copy()
test_set = set(test_data)

def list_lookup():
    return 50000 in test_list

def set_lookup():
    return 50000 in test_set

list_time = time_operation(list_lookup)
set_time = time_operation(set_lookup)

print(f"串列查找時間: {list_time:.6f} 秒")
print(f"集合查找時間: {set_time:.6f} 秒")
print(f"集合快了 {list_time/set_time:.1f} 倍")
```

**記憶體使用比較：**

```python
import sys

# 比較不同資料結構的記憶體使用
data = list(range(1000))

list_size = sys.getsizeof(data)
tuple_size = sys.getsizeof(tuple(data))
set_size = sys.getsizeof(set(data))
dict_size = sys.getsizeof({i: i for i in data})

print(f"串列記憶體使用: {list_size} 位元組")
print(f"元組記憶體使用: {tuple_size} 位元組")
print(f"集合記憶體使用: {set_size} 位元組")
print(f"字典記憶體使用: {dict_size} 位元組")
```

---

## 實用資料結構範例

**計數器 (Counter)：**

```python
from collections import Counter

# 字元計數
text = "hello world"
char_count = Counter(text)
print(char_count)  # Counter({'l': 3, 'o': 2, 'h': 1, 'e': 1, ' ': 1, 'w': 1, 'r': 1, 'd': 1})

# 單字計數
words = "the quick brown fox jumps over the lazy dog the fox".split()
word_count = Counter(words)
print(word_count)  # Counter({'the': 3, 'fox': 2, 'quick': 1, 'brown': 1, ...})

# 最常見的元素
most_common = word_count.most_common(3)
print(f"最常見的3個單字: {most_common}")

# 更新計數
more_words = "the cat and the dog".split()
word_count.update(more_words)
print(word_count.most_common(3))

# 數學運算
counter1 = Counter(['a', 'b', 'c', 'a'])
counter2 = Counter(['a', 'b', 'b', 'd'])

print(f"加法: {counter1 + counter2}")  # Counter({'a': 3, 'b': 3, 'c': 1, 'd': 1})
print(f"減法: {counter1 - counter2}")  # Counter({'c': 1, 'a': 1})
print(f"交集: {counter1 & counter2}")  # Counter({'a': 1, 'b': 1})
print(f"聯集: {counter1 | counter2}")  # Counter({'a': 2, 'b': 2, 'c': 1, 'd': 1})
```

**雙向佇列 (deque)：**

```python
from collections import deque

# 建立雙向佇列
dq = deque([1, 2, 3])

# 兩端都可以快速新增/移除
dq.appendleft(0)  # 左邊新增
dq.append(4)      # 右邊新增
print(dq)  # deque([0, 1, 2, 3, 4])

left_item = dq.popleft()  # 左邊移除
right_item = dq.pop()     # 右邊移除
print(f"移除的元素: {left_item}, {right_item}")
print(dq)  # deque([1, 2, 3])

# 旋轉
dq.rotate(1)   # 向右旋轉
print(dq)      # deque([3, 1, 2])

dq.rotate(-2)  # 向左旋轉
print(dq)      # deque([2, 3, 1])

# 限制大小的 deque（環形緩衝區）
limited_dq = deque(maxlen=3)
for i in range(5):
    limited_dq.append(i)
    print(f"新增 {i}: {limited_dq}")
# 輸出會顯示只保留最後 3 個元素
```

---

## 資料結構選擇指南

**什麼時候使用什麼：**

**串列 (list)：**

- 需要有序的可變序列
- 需要透過索引存取元素
- 允許重複元素
- 需要在任意位置插入/刪除

**元組 (tuple)：**

- 需要不可變的有序序列
- 作為字典的鍵
- 回傳多個值
- 確保資料不會被意外修改

**字典 (dict)：**

- 需要鍵值對映射
- 快速查找、新增、刪除
- 鍵必須是不可變類型

**集合 (set)：**

- 需要唯一元素
- 快速成員檢查
- 集合運算（聯集、交集等）

**效能比較表格：**

| 操作       | 串列   | 元組 | 字典 | 集合 |
| ---------- | ------ | ---- | ---- | ---- |
| 存取元素   | O(1)   | O(1) | O(1) | -    |
| 搜尋元素   | O(n)   | O(n) | O(1) | O(1) |
| 新增元素   | O(1)\* | -    | O(1) | O(1) |
| 刪除元素   | O(n)   | -    | O(1) | O(1) |
| 記憶體使用 | 中等   | 低   | 高   | 中等 |

\*註：串列的 append() 是 O(1)，但 insert() 是 O(n)

---

## 實際應用範例

**學生成績管理系統：**

```python
from collections import defaultdict, namedtuple, Counter

# 定義學生資料結構
Student = namedtuple('Student', ['id', 'name', 'class_name'])
Grade = namedtuple('Grade', ['student_id', 'subject', 'score'])

class GradeManager:
    def __init__(self):
        self.students = {}  # student_id -> Student
        self.grades = defaultdict(list)  # student_id -> [Grade, ...]
        self.class_students = defaultdict(set)  # class_name -> {student_id, ...}

    def add_student(self, student_id, name, class_name):
        """新增學生"""
        student = Student(student_id, name, class_name)
        self.students[student_id] = student
        self.class_students[class_name].add(student_id)

    def add_grade(self, student_id, subject, score):
        """新增成績"""
        if student_id not in self.students:
            raise ValueError(f"學生 {student_id} 不存在")

        grade = Grade(student_id, subject, score)
        self.grades[student_id].append(grade)

    def get_student_average(self, student_id):
        """計算學生平均分數"""
        if student_id not in self.grades:
            return 0

        scores = [grade.score for grade in self.grades[student_id]]
        return sum(scores) / len(scores) if scores else 0

    def get_class_statistics(self, class_name):
        """取得班級統計資訊"""
        if class_name not in self.class_students:
            return {}

        student_ids = self.class_students[class_name]
        averages = [self.get_student_average(sid) for sid in student_ids]
        averages = [avg for avg in averages if avg > 0]  # 排除沒有成績的學生

        if not averages:
            return {}

        return {
            'class_name': class_name,
            'student_count': len(student_ids),
            'class_average': sum(averages) / len(averages),
            'highest_average': max(averages),
            'lowest_average': min(averages)
        }

    def get_subject_distribution(self, subject):
        """取得科目分數分布"""
        scores = []
        for student_grades in self.grades.values():
            for grade in student_grades:
                if grade.subject == subject:
                    scores.append(grade.score)

        if not scores:
            return {}

        # 分數區間統計
        score_ranges = Counter()
        for score in scores:
            if score >= 90:
                score_ranges['A (90-100)'] += 1
            elif score >= 80:
                score_ranges['B (80-89)'] += 1
            elif score >= 70:
                score_ranges['C (70-79)'] += 1
            elif score >= 60:
                score_ranges['D (60-69)'] += 1
            else:
                score_ranges['F (0-59)'] += 1

        return {
            'subject': subject,
            'total_students': len(scores),
            'average_score': sum(scores) / len(scores),
            'score_distribution': dict(score_ranges)
        }

# 使用範例
manager = GradeManager()

# 新增學生
manager.add_student('S001', '張小明', '資工一A')
manager.add_student('S002', '李小華', '資工一A')
manager.add_student('S003', '王小美', '資工一B')

# 新增成績
manager.add_grade('S001', '數學', 85)
manager.add_grade('S001', '英文', 92)
manager.add_grade('S001', '程式設計', 88)

manager.add_grade('S002', '數學', 78)
manager.add_grade('S002', '英文', 85)
manager.add_grade('S002', '程式設計', 95)

manager.add_grade('S003', '數學', 92)
manager.add_grade('S003', '英文', 88)

# 查詢結果
print(f"S001 平均分數: {manager.get_student_average('S001'):.1f}")
print(f"資工一A 班級統計: {manager.get_class_statistics('資工一A')}")
print(f"數學科分數分布: {manager.get_subject_distribution('數學')}")
```

---

## 總結與 Q&A

我們已經涵蓋了 Python 資料結構的進階應用！

- **進階操作**：推導式、多維結構、專門的資料類型
- **效能考量**：了解不同資料結構的時間和空間複雜度
- **實際應用**：學會在真實專案中選擇和使用適當的資料結構
- **最佳實務**：掌握各種資料結構的使用時機和注意事項

有任何問題嗎？
