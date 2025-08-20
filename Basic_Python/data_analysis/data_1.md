# Python 新手指南：資料分析 01 - 資料分析概述

**作者：** tsung-min pai  
**單位：** NTUEE

---

## 大綱

### 1 什麼是資料分析

- 資料分析的定義與重要性
- 資料驅動決策
- 資料分析的類型

### 2 Python 在資料科學中的地位

- 為什麼選擇 Python
- Python vs 其他工具
- Python 資料科學生態系統

### 3 資料分析的工作流程

- 問題定義
- 資料收集與清理
- 探索性資料分析
- 模型建立與驗證
- 結果解釋與呈現

### 4 常用的資料分析函式庫介紹

- NumPy：數值運算基礎
- Pandas：資料操作工具
- Matplotlib & Seaborn：視覺化函式庫
- Scikit-learn：機器學習工具

---

## 什麼是資料分析

**資料分析的定義：**
資料分析是從原始資料中提取有意義的見解和模式的過程。它涉及檢查、清理、轉換和建模資料，以發現有用的資訊、得出結論並支援決策制定。

**為什麼資料分析重要？**

- 🎯 **改善決策品質**：基於事實而非直覺做決定
- 💰 **降低成本**：找出效率不彰的環節
- 📈 **發現機會**：識別新的商業機會或趨勢
- 🔍 **風險管理**：提前識別潛在問題
- 🎭 **了解客戶**：深入洞察客戶行為和需求

```python
# 資料分析的簡單範例
import pandas as pd
import numpy as np

# 假設我們有一個銷售資料集
sales_data = {
    '月份': ['1月', '2月', '3月', '4月', '5月'],
    '銷售額': [100000, 120000, 95000, 140000, 160000],
    '訂單數': [150, 180, 140, 200, 220]
}

df = pd.DataFrame(sales_data)
print("銷售資料：")
print(df)

# 簡單的分析
print(f"\n平均月銷售額：{df['銷售額'].mean():,.0f} 元")
print(f"總銷售額：{df['銷售額'].sum():,.0f} 元")
print(f"銷售額成長率：{((df['銷售額'].iloc[-1] - df['銷售額'].iloc[0]) / df['銷售額'].iloc[0] * 100):.1f}%")
```

---

## 資料分析的類型

**描述性分析 (Descriptive Analytics)：**

- **目標**：了解「發生了什麼」
- **方法**：統計摘要、圖表、報表
- **範例**：月銷售報告、網站流量統計

```python
# 描述性分析範例
import pandas as pd
import numpy as np

# 建立範例資料
np.random.seed(42)
student_scores = {
    '數學': np.random.normal(75, 15, 100),
    '英文': np.random.normal(80, 12, 100),
    '物理': np.random.normal(70, 18, 100)
}

scores_df = pd.DataFrame(student_scores)

# 描述性統計
print("學生成績描述性統計：")
print(scores_df.describe())

# 相關性分析
print("\n科目間相關性：")
print(scores_df.corr())
```

**診斷性分析 (Diagnostic Analytics)：**

- **目標**：了解「為什麼發生」
- **方法**：相關性分析、因果分析
- **範例**：為什麼某產品銷量下降

**預測性分析 (Predictive Analytics)：**

- **目標**：預測「將會發生什麼」
- **方法**：機器學習、時間序列分析
- **範例**：預測下個月的銷售額

**規範性分析 (Prescriptive Analytics)：**

- **目標**：建議「應該做什麼」
- **方法**：最佳化演算法、模擬
- **範例**：最佳定價策略、庫存管理

---

## Python 在資料科學中的地位

**為什麼選擇 Python？**

**1. 簡潔易學的語法：**

```python
# Python 程式碼簡潔直觀
data = [1, 2, 3, 4, 5]
squared = [x**2 for x in data]
average = sum(squared) / len(squared)
print(f"平方數的平均值：{average}")
```

**2. 豐富的函式庫生態系統：**

```python
# 只需幾行程式碼就能完成複雜分析
import pandas as pd
import matplotlib.pyplot as plt

# 讀取資料、分析、視覺化
df = pd.read_csv('data.csv')
df.groupby('category').mean().plot(kind='bar')
plt.show()
```

**3. 強大的社群支援：**

- 📚 豐富的學習資源
- 💬 活躍的開發者社群
- 🔧 持續更新的函式庫

**Python vs 其他工具比較：**

| 特性         | Python | R    | Excel | SQL  |
| ------------ | ------ | ---- | ----- | ---- |
| 學習難度     | 中等   | 中等 | 簡單  | 中等 |
| 程式設計能力 | 強     | 強   | 弱    | 有限 |
| 資料處理規模 | 大     | 大   | 小-中 | 大   |
| 視覺化功能   | 強     | 強   | 中等  | 有限 |
| 機器學習     | 強     | 強   | 有限  | 有限 |
| 產業採用度   | 高     | 中等 | 高    | 高   |

**使用場景建議：**

- **Python**：全方位資料科學專案、機器學習、自動化
- **R**：統計分析、學術研究
- **Excel**：簡單分析、快速原型、商業報告
- **SQL**：資料庫查詢、資料倉儲

---

## 資料分析的工作流程

**1. 問題定義 (Problem Definition)：**

```python
# 範例：定義分析目標
analysis_goals = {
    "主要問題": "哪些因素影響客戶滿意度？",
    "次要問題": [
        "不同年齡層的滿意度是否有差異？",
        "服務品質如何影響滿意度？",
        "價格敏感度如何？"
    ],
    "成功指標": "能夠識別影響滿意度的前3大因素"
}

print("分析目標：")
for key, value in analysis_goals.items():
    print(f"{key}: {value}")
```

**2. 資料收集 (Data Collection)：**

```python
# 資料來源類型
data_sources = {
    "內部資料": ["銷售記錄", "客戶資料庫", "網站日誌"],
    "外部資料": ["市場調查", "政府統計", "第三方API"],
    "資料格式": ["CSV", "JSON", "Excel", "資料庫", "API"]
}

# 資料收集範例
import pandas as pd
import requests

# 從CSV讀取
# df = pd.read_csv('customer_data.csv')

# 從API取得資料
# response = requests.get('https://api.example.com/data')
# data = response.json()
```

**3. 資料清理 (Data Cleaning)：**

```python
import pandas as pd
import numpy as np

# 建立包含問題的範例資料
dirty_data = pd.DataFrame({
    'name': ['Alice', 'Bob', None, 'Diana', 'Eve'],
    'age': [25, -5, 30, 200, 28],  # 包含不合理值
    'salary': [50000, 60000, None, 75000, 'unknown'],  # 混合類型
    'city': ['台北', 'TAIPEI', '台北 ', '高雄', '台中']  # 格式不一致
})

print("原始資料（包含問題）：")
print(dirty_data)
print(f"\n資料形狀：{dirty_data.shape}")
print(f"缺失值統計：\n{dirty_data.isnull().sum()}")

# 資料清理步驟
def clean_data(df):
    # 1. 處理缺失值
    df = df.dropna(subset=['name'])  # 刪除姓名為空的行

    # 2. 處理異常值
    df = df[(df['age'] >= 0) & (df['age'] <= 120)]  # 合理年齡範圍

    # 3. 處理資料類型
    df['salary'] = pd.to_numeric(df['salary'], errors='coerce')

    # 4. 標準化格式
    df['city'] = df['city'].str.strip().str.upper()

    return df

cleaned_data = clean_data(dirty_data.copy())
print("\n清理後的資料：")
print(cleaned_data)
```

**4. 探索性資料分析 (EDA)：**

```python
# 探索性資料分析範例
def perform_eda(df):
    print("=== 探索性資料分析 ===")

    # 基本資訊
    print(f"資料維度：{df.shape}")
    print(f"欄位類型：\n{df.dtypes}")

    # 統計摘要
    print(f"\n數值變數統計：\n{df.describe()}")

    # 類別變數統計
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        print(f"\n{col} 的分布：\n{df[col].value_counts()}")

# perform_eda(cleaned_data)
```

**5. 資料分析與建模：**

```python
# 分析範例：相關性分析
def analyze_relationships(df):
    # 計算相關係數
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 1:
        correlation_matrix = df[numeric_cols].corr()
        print("相關性矩陣：")
        print(correlation_matrix)

    # 分組分析
    if 'city' in df.columns and 'salary' in df.columns:
        city_salary = df.groupby('city')['salary'].agg(['mean', 'count'])
        print(f"\n各城市薪資統計：\n{city_salary}")

# analyze_relationships(cleaned_data)
```

**6. 結果解釋與呈現：**

```python
# 結果呈現範例
def present_findings(df):
    findings = {
        "關鍵發現": [
            "年齡與薪資呈現正相關關係",
            "台北地區薪資水準較高",
            "資料品質需要改善（缺失值較多）"
        ],
        "建議行動": [
            "建立更完善的資料收集流程",
            "針對不同城市制定差異化策略",
            "深入分析薪資影響因素"
        ]
    }

    print("=== 分析結果 ===")
    for category, items in findings.items():
        print(f"\n{category}：")
        for i, item in enumerate(items, 1):
            print(f"{i}. {item}")

# present_findings(cleaned_data)
```

---

## 常用的資料分析函式庫介紹

**NumPy - 數值運算基礎：**

```python
import numpy as np

# NumPy 的優勢：高效的數值運算
print("=== NumPy 範例 ===")

# 建立陣列
arr = np.array([1, 2, 3, 4, 5])
print(f"陣列：{arr}")

# 向量化運算（比迴圈快很多）
squared = arr ** 2
print(f"平方：{squared}")

# 統計函式
print(f"平均值：{np.mean(arr)}")
print(f"標準差：{np.std(arr)}")

# 多維陣列
matrix = np.array([[1, 2, 3], [4, 5, 6]])
print(f"矩陣形狀：{matrix.shape}")
print(f"矩陣：\n{matrix}")
```

**Pandas - 資料操作工具：**

```python
import pandas as pd

print("\n=== Pandas 範例 ===")

# 建立 DataFrame
data = {
    'product': ['A', 'B', 'C', 'A', 'B'],
    'sales': [100, 150, 200, 120, 180],
    'region': ['North', 'South', 'North', 'South', 'North']
}

df = pd.DataFrame(data)
print("原始資料：")
print(df)

# 分組聚合
grouped = df.groupby('product')['sales'].sum()
print(f"\n各產品總銷售：\n{grouped}")

# 篩選資料
high_sales = df[df['sales'] > 120]
print(f"\n高銷售記錄：\n{high_sales}")
```

**Matplotlib - 視覺化基礎：**

```python
import matplotlib.pyplot as plt
import numpy as np

print("\n=== Matplotlib 範例 ===")

# 建立簡單圖表
x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.figure(figsize=(10, 6))
plt.plot(x, y, label='sin(x)', linewidth=2)
plt.title('正弦函數圖', fontsize=16)
plt.xlabel('x', fontsize=12)
plt.ylabel('sin(x)', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)

# 注意：在實際環境中使用 plt.show() 顯示圖表
# plt.show()
print("圖表已建立（在實際環境中會顯示）")
```

**Seaborn - 進階視覺化：**

```python
import seaborn as sns
import matplotlib.pyplot as plt

print("\n=== Seaborn 範例 ===")

# 使用 Seaborn 的內建資料集
# tips = sns.load_dataset('tips')

# 建立範例資料
tips_data = {
    'total_bill': [16.99, 10.34, 21.01, 23.68, 24.59],
    'tip': [1.01, 1.66, 3.50, 3.31, 3.61],
    'day': ['Sun', 'Sun', 'Sun', 'Sat', 'Sat']
}

tips = pd.DataFrame(tips_data)
print("餐廳小費資料：")
print(tips)

# Seaborn 讓複雜圖表變得簡單
plt.figure(figsize=(8, 6))
# sns.scatterplot(data=tips, x='total_bill', y='tip', hue='day')
# plt.title('餐費與小費關係')
print("散點圖已建立（在實際環境中會顯示）")
```

---

## 函式庫安裝與設定

**安裝必要套件：**

```bash
# 基礎套件
pip install numpy pandas matplotlib seaborn

# 進階套件
pip install scikit-learn jupyter notebook

# 或使用 conda
conda install numpy pandas matplotlib seaborn scikit-learn jupyter
```

**匯入慣例：**

```python
# 標準匯入慣例
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 設定顯示選項
pd.set_option('display.max_columns', None)  # 顯示所有欄位
pd.set_option('display.precision', 2)      # 小數點後2位

# Matplotlib 中文字型設定（避免亂碼）
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

print("函式庫匯入完成，環境設定完畢！")
```

---

## 實用工具與最佳實務

**Jupyter Notebook 使用技巧：**

```python
# Jupyter 魔術指令
# %timeit - 測量執行時間
# %matplotlib inline - 內嵌圖表
# %load_ext autoreload - 自動重新載入模組

# 在 Jupyter 中顯示所有輸出
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

print("Jupyter 環境最佳化完成")
```

**程式碼組織最佳實務：**

```python
# 良好的程式碼結構
def load_data(file_path):
    """載入資料的函式"""
    try:
        df = pd.read_csv(file_path)
        print(f"成功載入 {len(df)} 筆記錄")
        return df
    except FileNotFoundError:
        print(f"找不到檔案：{file_path}")
        return None

def clean_data(df):
    """清理資料的函式"""
    # 記錄原始資料筆數
    original_count = len(df)

    # 清理步驟
    df = df.dropna()

    # 記錄清理結果
    final_count = len(df)
    print(f"資料清理完成：{original_count} -> {final_count} 筆記錄")

    return df

def analyze_data(df):
    """分析資料的函式"""
    # 分析邏輯
    results = {}
    return results

# 主要執行流程
def main():
    # df = load_data('data.csv')
    # if df is not None:
    #     df_clean = clean_data(df)
    #     results = analyze_data(df_clean)
    #     return results
    pass

print("分析框架已建立")
```

---

## 總結與下一步

**本章重點回顧：**

1. **資料分析的重要性**：在現代商業和科學研究中不可或缺
2. **Python 的優勢**：簡潔語法、豐富生態系統、強大社群
3. **分析工作流程**：從問題定義到結果呈現的系統化方法
4. **核心工具**：NumPy、Pandas、Matplotlib、Seaborn

**接下來的學習計畫：**

```python
learning_path = {
    "第2章": "深入學習 NumPy 數值運算",
    "第3章": "掌握 Pandas 資料處理技巧",
    "第4章": "建立專業的資料視覺化",
    "第5章": "完成完整的資料分析專案"
}

print("學習路徑：")
for chapter, topic in learning_path.items():
    print(f"{chapter}: {topic}")
```

**練習建議：**

1. 安裝並測試所有必要的函式庫
2. 找一個有興趣的資料集進行初步探索
3. 練習使用 Jupyter Notebook
4. 嘗試重現本章的所有範例程式碼

準備好深入 NumPy 的世界了嗎？讓我們繼續下一章的學習！

---

## Q&A

**Q: 我完全沒有程式設計背景，能學會資料分析嗎？**
A: 當然可以！Python 的語法相對簡單，而且我們會從基礎開始。重要的是邏輯思維和對資料的好奇心。

**Q: 學習資料分析需要很強的數學背景嗎？**
A: 基礎的統計概念會很有幫助，但不需要高深的數學。我們會在需要時介紹相關概念。

**Q: 除了 Python，我還需要學習其他工具嗎？**
A: Python 已經能覆蓋大部分需求，但了解 SQL 和 Excel 會讓你更全面。

**Q: 如何找到練習用的資料集？**
A: 推薦 Kaggle、UCI Machine Learning Repository、政府開放資料平台等。

有任何問題嗎？
