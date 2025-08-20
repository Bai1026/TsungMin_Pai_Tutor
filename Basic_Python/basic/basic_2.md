# Python 新手指南：02 流程控制

**作者：** tsung-min pai  
**單位：** NTUEE

---

## 大綱

### 1 條件判斷 (Conditional Statements)

- if / elif / else
- 比較運算子
- 邏輯運算子

### 2 迴圈 (Loops)

- for 迴圈
- while 迴圈
- break 與 continue

---

## 條件判斷 (Conditional Statements)

讓程式根據不同的條件執行不同的程式碼區塊。這是程式能做出「決策」的基礎。

```python
# 語法：
if 條件:
    # 條件為 True 時執行的程式碼
elif 另一個條件:
    # 另一個條件為 True 時執行的程式碼
else:
    # 所有條件都為 False 時執行的程式碼
```

---

## 條件判斷範例

```python
age = 20

if age >= 18:
    print("您已是成年人。")
else:
    print("您是未成年人。")

score = 85

if score >= 90:
    print("優等")
elif score >= 80:
    print("甲等")
else:
    print("普通")
```

---

## 比較運算子 (Comparison Operators)

用於比較兩個值，並返回 `True` 或 `False` 的布林值。

| 運算子 | 描述       | 範例       | 結果    |
| ------ | ---------- | ---------- | ------- |
| ==     | 等於       | `5 == 5`   | `True`  |
| !=     | 不等於     | `5 != 6`   | `True`  |
| >      | 大於       | `10 > 5`   | `True`  |
| <      | 小於       | `10 < 5`   | `False` |
| >=     | 大於或等於 | `10 >= 10` | `True`  |
| <=     | 小於或等於 | `10 <= 9`  | `False` |

---

## 邏輯運算子 (Logical Operators)

用於結合多個條件，形成更複雜的布林表達式。

| 運算子 | 描述           | 範例            | 結果    |
| ------ | -------------- | --------------- | ------- |
| and    | 兩個條件都為真 | `True and True` | `True`  |
| or     | 任一條件為真   | `True or False` | `True`  |
| not    | 反轉布林值     | `not True`      | `False` |

---

## 迴圈 (Loops)

迴圈讓程式能夠重複執行一段程式碼，直到滿足特定條件為止。

```python
# 語法：
for 變數 in 可迭代物件:
    # 執行程式碼

while 條件:
    # 條件為 True 時重複執行的程式碼
```

---

## for 迴圈範例

`for` 迴圈通常用於遍歷序列，例如列表 (list)、元組 (tuple) 或字串 (string)。

```python
# 遍歷一個列表
fruits = ["apple", "banana", "cherry"]
for x in fruits:
    print(x)

# 遍歷一個數字範圍 (從 0 到 4)
for i in range(5):
    print(i)
```

---

## while 迴圈範例

`while` 迴圈只要條件為 `True`，就會一直執行。

```python
i = 1
while i < 6:
    print(i)
    i += 1
```

---

## break 與 continue

用於控制迴圈的執行流程。

- `break`: 立即停止當前迴圈的執行。
- `continue`: 跳過當前迭代，直接進入下一個迭代。

---

## break 與 continue 範例

```python
# break 範例
for i in range(10):
    if i == 5:
        break
    print(i) # 輸出 0, 1, 2, 3, 4

# continue 範例
for i in range(10):
    if i % 2 == 0:
        continue # 跳過偶數
    print(i) # 輸出 1, 3, 5, 7, 9
```

---

## 總結與 Q&A

我們已經涵蓋了 Python 的基本流程控制！

- **條件判斷**：使用 `if`, `elif`, `else` 做出決策。
- **迴圈**：使用 `for` 或 `while` 重複執行任務。
- **運算子**：使用比較和邏輯運算子來建立條件。

有任何問題嗎？
