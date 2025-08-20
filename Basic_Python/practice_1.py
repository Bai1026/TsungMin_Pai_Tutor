#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 基礎練習題：變數、資料型態、語法
作者：TsungMin Pai
日期：2025.08.18

本檔案包含了 Python 基礎概念的練習題，涵蓋：
- 變數宣告與賦值
- 基本資料型態（int, float, str, bool）
- 型態轉換
- 基本輸入輸出
- 算術運算子
- 程式碼註解
"""

print("=" * 60)
print("Python 基礎練習題 - 變數、資料型態、語法")
print("=" * 60)

# ========== 練習 1：變數宣告與賦值 ==========
print("\n【練習 1】變數宣告與賦值")
print("-" * 30)

# TODO: 建立以下變數並賦值
# 學生姓名（字串）
student_name = "王小明"

# 學生年齡（整數）
student_age = 20

# 學生身高（浮點數，單位：公分）
student_height = 175.5

# 是否及格（布林值）
is_passed = True

# 列印所有變數
print(f"姓名：{student_name}")
print(f"年齡：{student_age}")
print(f"身高：{student_height} 公分")
print(f"是否及格：{is_passed}")

# ========== 練習 2：型態檢查與轉換 ==========
print("\n【練習 2】型態檢查與轉換")
print("-" * 30)

# 檢查變數型態
print(f"student_name 的型態：{type(student_name)}")
print(f"student_age 的型態：{type(student_age)}")
print(f"student_height 的型態：{type(student_height)}")
print(f"is_passed 的型態：{type(is_passed)}")

# TODO: 進行型態轉換
age_str = str(student_age)          # 整數轉字串
height_int = int(student_height)    # 浮點數轉整數
age_float = float(student_age)      # 整數轉浮點數

print(f"\n轉換後：")
print(f"年齡（字串）：'{age_str}'，型態：{type(age_str)}")
print(f"身高（整數）：{height_int}，型態：{type(height_int)}")
print(f"年齡（浮點數）：{age_float}，型態：{type(age_float)}")

# ========== 練習 3：使用者輸入與輸出 ==========
print("\n【練習 3】使用者輸入與輸出")
print("-" * 30)

# TODO: 取得使用者輸入（取消註解以執行）
# print("請輸入您的資訊：")
# user_name = input("您的姓名：")
# user_age = int(input("您的年齡："))
# user_score = float(input("您的分數："))

# 使用預設值進行展示
user_name = "張小美"
user_age = 22
user_score = 87.5

print(f"\n您輸入的資訊：")
print(f"姓名：{user_name}")
print(f"年齡：{user_age} 歲")
print(f"分數：{user_score} 分")

# ========== 練習 4：算術運算子 ==========
print("\n【練習 4】算術運算子")
print("-" * 30)

# 定義兩個數字
num1 = 15
num2 = 4

print(f"數字 1：{num1}")
print(f"數字 2：{num2}")
print(f"\n運算結果：")

# TODO: 進行各種運算
addition = num1 + num2          # 加法
subtraction = num1 - num2       # 減法
multiplication = num1 * num2    # 乘法
division = num1 / num2          # 除法（浮點數）
floor_division = num1 // num2   # 整數除法
remainder = num1 % num2         # 取餘數
power = num1 ** num2            # 次方

print(f"{num1} + {num2} = {addition}")
print(f"{num1} - {num2} = {subtraction}")
print(f"{num1} × {num2} = {multiplication}")
print(f"{num1} ÷ {num2} = {division}")
print(f"{num1} // {num2} = {floor_division} （整數除法）")
print(f"{num1} % {num2} = {remainder} （餘數）")
print(f"{num1} ** {num2} = {power} （{num1} 的 {num2} 次方）")

# ========== 練習 5：複合賦值運算子 ==========
print("\n【練習 5】複合賦值運算子")
print("-" * 30)

# 初始值
counter = 10
print(f"初始值：counter = {counter}")

# TODO: 使用複合賦值運算子
counter += 5    # 等同於 counter = counter + 5
print(f"counter += 5 後：{counter}")

counter -= 3    # 等同於 counter = counter - 3
print(f"counter -= 3 後：{counter}")

counter *= 2    # 等同於 counter = counter * 2
print(f"counter *= 2 後：{counter}")

counter //= 4   # 等同於 counter = counter // 4
print(f"counter //= 4 後：{counter}")

# ========== 練習 6：字串操作 ==========
print("\n【練習 6】字串操作")
print("-" * 30)

first_name = "小明"
last_name = "王"
birth_year = 2003
current_year = 2025

# TODO: 字串連接與格式化
full_name = last_name + first_name  # 字串連接
age = current_year - birth_year     # 計算年齡

print(f"姓氏：{last_name}")
print(f"名字：{first_name}")
print(f"全名：{full_name}")
print(f"年齡：{age} 歲")

# 使用不同的字串格式化方法
print(f"\nf-string 格式化：{full_name} 今年 {age} 歲")
print("format() 方法：{} 今年 {} 歲".format(full_name, age))
print("% 格式化：%s 今年 %d 歲" % (full_name, age))

# ========== 練習 7：布林運算 ==========
print("\n【練習 7】布林運算")
print("-" * 30)

score1 = 85
score2 = 92
passing_score = 60

# TODO: 比較運算
is_score1_passed = score1 >= passing_score
is_score2_passed = score2 >= passing_score
is_score1_higher = score1 > score2

print(f"分數 1：{score1}")
print(f"分數 2：{score2}")
print(f"及格分數：{passing_score}")
print(f"\n比較結果：")
print(f"分數 1 及格：{is_score1_passed}")
print(f"分數 2 及格：{is_score2_passed}")
print(f"分數 1 較高：{is_score1_higher}")

# ========== 練習 8：實際應用：簡單計算機 ==========
print("\n【練習 8】實際應用：簡單計算機")
print("-" * 30)

# TODO: 建立一個簡單的計算機程式
print("=== 簡單計算機 ===")

# 使用預設值（實際使用時可改為 input()）
number1 = 25.5
number2 = 7.2

print(f"數字 1：{number1}")
print(f"數字 2：{number2}")

# 執行所有基本運算
add_result = number1 + number2
sub_result = number1 - number2
mul_result = number1 * number2
div_result = number1 / number2 if number2 != 0 else "無法除以零"

print(f"\n計算結果：")
print(f"{number1} + {number2} = {add_result}")
print(f"{number1} - {number2} = {sub_result}")
print(f"{number1} × {number2} = {mul_result}")
print(f"{number1} ÷ {number2} = {div_result}")

# ========== 練習 9：錯誤處理：型態轉換 ==========
print("\n【練習 9】錯誤處理：型態轉換")
print("-" * 30)

# TODO: 處理型態轉換可能產生的錯誤
test_strings = ["123", "45.67", "abc", ""]

for test_str in test_strings:
    print(f"\n測試字串：'{test_str}'")
    
    # 嘗試轉換為整數
    try:
        int_result = int(test_str)
        print(f"  轉換為整數：{int_result}")
    except ValueError:
        print(f"  轉換為整數：失敗（無法轉換）")
    
    # 嘗試轉換為浮點數
    try:
        float_result = float(test_str)
        print(f"  轉換為浮點數：{float_result}")
    except ValueError:
        print(f"  轉換為浮點數：失敗（無法轉換）")

# ========== 練習 10：挑戰題：個人資訊管理系統 ==========
print("\n【練習 10】挑戰題：個人資訊管理系統")
print("-" * 30)

# TODO: 建立一個簡單的個人資訊管理系統
print("=== 個人資訊管理系統 ===")

# 個人基本資訊
person_id = 1001
person_name = "李大華"
person_age = 28
person_height = 170.0
person_weight = 65.5
is_student = False
monthly_salary = 45000

# 計算衍生資訊
bmi = person_weight / ((person_height / 100) ** 2)  # BMI 計算
annual_salary = monthly_salary * 12                  # 年薪計算

# 判斷 BMI 等級
if bmi < 18.5:
    bmi_category = "體重過輕"
elif bmi < 24:
    bmi_category = "正常範圍"
elif bmi < 27:
    bmi_category = "過重"
else:
    bmi_category = "肥胖"

# 顯示完整資訊
print(f"\n【個人檔案】")
print(f"編號：{person_id}")
print(f"姓名：{person_name}")
print(f"年齡：{person_age} 歲")
print(f"身高：{person_height} 公分")
print(f"體重：{person_weight} 公斤")
print(f"學生身份：{'是' if is_student else '否'}")
print(f"月薪：NT$ {monthly_salary:,}")

print(f"\n【計算結果】")
print(f"BMI：{bmi:.2f} ({bmi_category})")
print(f"年薪：NT$ {annual_salary:,}")

# ========== 練習完成 ==========
print("\n" + "=" * 60)
print("🎉 恭喜！您已完成所有 Python 基礎練習題")
print("=" * 60)

"""
練習重點回顧：
1. 變數的宣告、賦值與命名
2. 四種基本資料型態：int, float, str, bool
3. 型態檢查與轉換
4. print() 和 input() 函式的使用
5. 算術運算子與複合賦值運算子
6. 字串操作與格式化
7. 比較運算與布林值
8. 基本錯誤處理
9. 實際應用範例

建議後續練習：
- 嘗試修改變數值，觀察程式執行結果
- 練習使用 input() 函式建立互動式程式
- 嘗試更複雜的數學計算
- 練習不同的字串格式化方法
- 建立更多實用的小程式