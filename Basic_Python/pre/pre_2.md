# Python 新手指南：00-B 開發環境設定

**作者：** Tsung-Min Pai
**單位：** NTUEE

---

## 大綱

### 1 pip 套件管理器

- pip 的安裝與基本使用
- 套件安裝與管理
- requirements.txt 的使用

### 2 Miniconda 環境管理

- Miniconda 安裝與設定
- conda 環境建立與管理
- conda vs pip 的差異

### 3 Visual Studio Code

- VSCode 安裝與設定
- Python 擴充套件安裝
- 除錯與開發技巧

### 4 Google Colab

- Colab 基本介紹
- 線上程式碼執行
- 檔案上傳與下載

---

## pip 套件管理器

**什麼是 pip？**

- Python 的標準套件管理工具
- 用於安裝、升級和移除 Python 套件
- 從 Python Package Index (PyPI) 下載套件

**檢查 pip 是否已安裝：**

```bash
# 檢查 pip 版本
pip --version

# 如果沒有安裝 pip (Windows)
python -m ensurepip --upgrade

# 升級 pip 到最新版本
python -m pip install --upgrade pip
```

---

## pip 基本指令

**安裝套件：**

```bash
# 安裝最新版本
pip install numpy

# 安裝特定版本
pip install numpy==1.21.0

# 安裝版本範圍
pip install "numpy>=1.20.0,<1.22.0"

# 從 requirements.txt 安裝
pip install -r requirements.txt

# 安裝開發版本
pip install git+https://github.com/user/repo.git
```

**管理套件：**

```bash
# 列出已安裝套件
pip list

# 顯示套件資訊
pip show numpy

# 升級套件
pip install --upgrade numpy

# 解除安裝套件
pip uninstall numpy

# 檢查過期套件
pip list --outdated
```

**產生 requirements.txt：**

```bash
# 產生當前環境的所有套件清單
pip freeze > requirements.txt
pip list --format=freeze > requirements.txt

# 只產生專案直接相依的套件
pip-tools 或手動編輯
```

---

## requirements.txt 最佳實務

**requirements.txt 範例：**

```
# 資料處理
numpy==1.21.0
pandas==1.3.0

# 網路請求
requests==2.25.1

# 資料視覺化
matplotlib==3.4.2
seaborn==0.11.2

# 機器學習
scikit-learn==0.24.2

# 開發工具
pytest==6.2.4
black==21.6b0
```

**使用 requirements.txt：**

```bash
# 安裝所有相依套件
pip install -r requirements.txt

# 在新環境中重建相同環境
pip install -r requirements.txt --no-deps  # 不安裝相依性
```

---

## Miniconda 環境管理

**什麼是 Miniconda？**

- 輕量級的 Python 發行版
- 包含 conda 套件管理器
- 支援建立獨立的 Python 環境
- 比 Anaconda 更小巧，可按需安裝套件

**Miniconda 安裝步驟：**

**Windows：**

```bash
# 1. 下載 Miniconda installer
# 前往 https://docs.conda.io/en/latest/miniconda.html

# 2. 執行 installer，建議選項：
# - Add Miniconda3 to PATH (勾選)
# - Register Miniconda3 as default Python (勾選)

# 3. 驗證安裝
conda --version
```

**macOS/Linux：**

```bash
# 1. 下載安裝腳本
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# 2. 執行安裝
bash Miniconda3-latest-Linux-x86_64.sh

# 3. 重新載入 shell
source ~/.bashrc

# 4. 驗證安裝
conda --version
```

---

## conda 環境管理

**建立和管理環境：**

```bash
# 建立新環境
conda create --name myproject python=3.9

# 建立環境並安裝套件
conda create --name dataproject python=3.9 numpy pandas

# 啟動環境
conda activate myproject

# 停用環境
conda deactivate

# 列出所有環境
conda env list

# 刪除環境
conda remove --name myproject --all
```

**在環境中管理套件：**

```bash
# 啟動環境後安裝套件
conda activate myproject
conda install numpy pandas matplotlib

# 從 conda-forge 安裝
conda install -c conda-forge scikit-learn

# 混合使用 conda 和 pip
conda install numpy  # 優先使用 conda
pip install some-package  # 如果 conda 沒有則使用 pip

# 匯出環境設定
conda env export > environment.yml

# 從設定檔建立環境
conda env create -f environment.yml
```

---

## environment.yml 範例

```yaml
name: dataproject
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.9
  - numpy=1.21.0
  - pandas=1.3.0
  - matplotlib=3.4.2
  - scikit-learn=0.24.2
  - pip
  - pip:
      - requests==2.25.1
      - seaborn==0.11.2
```

---

## conda vs pip 比較

| 特性           | conda                            | pip             |
| -------------- | -------------------------------- | --------------- |
| 套件來源       | Anaconda repository, conda-forge | PyPI            |
| 相依性處理     | 更好的相依性解析                 | 基本相依性處理  |
| 非 Python 套件 | 支援 (如 C/C++ 函式庫)           | 僅 Python 套件  |
| 環境管理       | 內建環境管理                     | 需要 virtualenv |
| 安裝速度       | 較慢但更穩定                     | 較快            |
| 套件數量       | 較少但品質高                     | 最多最全面      |

**建議使用策略：**

```bash
# 1. 優先使用 conda 安裝主要套件
conda install numpy pandas matplotlib

# 2. 使用 pip 安裝 conda 沒有的套件
pip install specific-package

# 3. 保持環境清潔
conda clean --all  # 清理暫存
```

---

## Visual Studio Code 設定

**VSCode 安裝：**

1. 前往 https://code.visualstudio.com/
2. 下載對應作業系統的安裝檔
3. 執行安裝程式

**必裝 Python 擴充套件：**

```bash
# 在 VSCode 中按 Ctrl+Shift+X 開啟擴充套件面板，搜尋安裝：

1. Python (Microsoft) - 基本 Python 支援
2. Pylance - 進階語言伺服器
3. Python Debugger - 除錯功能
4. autoDocstring - 自動產生文件字串
5. Black Formatter - 程式碼格式化
6. isort - 匯入語句排序
```

**VSCode Python 設定：**

**settings.json 設定：**

```json
{
  "python.defaultInterpreterPath": "python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length", "88"],
  "python.sortImports.args": ["--profile", "black"],
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  },
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 1000
}
```

---

## VSCode Python 開發技巧

**選擇 Python 直譯器：**

```bash
# 方法 1：使用指令面板
Ctrl+Shift+P → "Python: Select Interpreter"

# 方法 2：點擊狀態列的 Python 版本
# 狀態列右下角會顯示當前 Python 版本

# 方法 3：workspace 設定
# 在專案根目錄建立 .vscode/settings.json
{
    "python.pythonPath": "/path/to/your/python"
}
```

**除錯設定：**

**.vscode/launch.json 範例：**

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "justMyCode": true
    },
    {
      "name": "Python: Django",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/manage.py",
      "args": ["runserver"],
      "django": true
    }
  ]
}
```

**除錯快捷鍵：**

```bash
F9          # 設定/移除中斷點
F5          # 開始除錯
F10         # 逐行執行 (Step Over)
F11         # 進入函式 (Step Into)
Shift+F11   # 跳出函式 (Step Out)
Ctrl+F5     # 執行不除錯
```

---

## VSCode 實用快捷鍵

```bash
# 檔案操作
Ctrl+N          # 新檔案
Ctrl+O          # 開啟檔案
Ctrl+S          # 儲存
Ctrl+Shift+S    # 另存新檔

# 編輯操作
Ctrl+/          # 註解/取消註解
Ctrl+Shift+K    # 刪除整行
Alt+Up/Down     # 移動行
Shift+Alt+Up/Down  # 複製行

# 搜尋與取代
Ctrl+F          # 搜尋
Ctrl+H          # 取代
Ctrl+Shift+F    # 全域搜尋

# 終端機
Ctrl+`          # 開啟/關閉終端機
Ctrl+Shift+`    # 新增終端機
```

---

## Google Colab 介紹

**什麼是 Google Colab？**

- Google 提供的免費 Jupyter 筆記本環境
- 預裝常用 Python 套件
- 提供免費 GPU/TPU 運算資源
- 支援即時協作

**存取 Google Colab：**

```bash
# 1. 前往 https://colab.research.google.com/
# 2. 使用 Google 帳號登入
# 3. 點擊 "新增筆記本" 開始使用
```

**Colab 基本操作：**

```python
# 在 Colab 中執行 Python 程式碼
print("Hello, Google Colab!")

# 安裝套件
!pip install package_name

# 檢查 GPU 可用性
import torch
print(torch.cuda.is_available())

# 檢查系統資訊
!nvidia-smi  # GPU 資訊
!df -h      # 磁碟空間
!free -h    # 記憶體使用量
```

---

## Colab 檔案操作

**上傳檔案：**

```python
from google.colab import files

# 上傳檔案
uploaded = files.upload()

# 列出上傳的檔案
import os
print(os.listdir('.'))
```

**下載檔案：**

```python
from google.colab import files

# 建立檔案
with open('example.txt', 'w') as f:
    f.write('Hello, World!')

# 下載檔案
files.download('example.txt')
```

**Google Drive 整合：**

```python
from google.colab import drive

# 掛載 Google Drive
drive.mount('/content/drive')

# 存取 Drive 中的檔案
import os
os.chdir('/content/drive/MyDrive')
print(os.listdir('.'))
```

---

## Colab 進階功能

**使用 GPU/TPU：**

```python
# 1. 前往 "執行階段" > "變更執行階段類型"
# 2. 選擇 "GPU" 或 "TPU"
# 3. 點擊 "儲存"

# 驗證 GPU
import tensorflow as tf
print("GPU 可用:", tf.config.list_physical_devices('GPU'))

# 驗證 TPU
try:
    tpu = tf.distribute.cluster_resolver.TPUClusterResolver()
    print('TPU 可用:', tpu.cluster_spec().as_dict()['worker'])
except ValueError:
    print('TPU 不可用')
```

**Colab 魔術指令：**

```python
# 顯示所有魔術指令
%lsmagic

# 測量執行時間
%time print("Hello")
%%time
# 整個儲存格的執行時間

# 執行 shell 指令
!ls -la
!pwd

# 顯示變數資訊
%whos

# 載入外部 Python 檔案
%load filename.py
```

---

## 開發環境選擇指南

**本地開發 (VSCode + conda)：**
✅ 適合正式專案開發
✅ 完整的除錯功能
✅ 版本控制整合
✅ 自訂開發環境
❌ 需要安裝設定時間

**線上開發 (Google Colab)：**
✅ 免費 GPU/TPU 資源
✅ 無需安裝設定
✅ 適合機器學習實驗
✅ 即時協作功能
❌ 工作階段會過期
❌ 檔案管理較不便

**建議使用策略：**

- **學習階段**：使用 Colab 快速上手
- **小型實驗**：Colab 進行概念驗證
- **正式開發**：本地環境 + VSCode
- **機器學習**：Colab 訓練 + 本地開發

---

## 環境設定檢查清單

**基本環境：**

```bash
□ Python 3.8+ 安裝完成
□ pip 可正常使用
□ 能建立虛擬環境
□ VSCode 安裝並設定完成
□ Python 擴充套件正常運作
```

**進階環境：**

```bash
□ Miniconda 安裝完成
□ conda 環境管理正常
□ Git 安裝並設定
□ Google Colab 帳號可用
□ 常用套件安裝測試
```

**驗證安裝腳本：**

```python
#!/usr/bin/env python3
"""
開發環境驗證腳本
"""

def check_python():
    import sys
    print(f"Python 版本: {sys.version}")
    return sys.version_info >= (3, 8)

def check_packages():
    required_packages = ['numpy', 'pandas', 'matplotlib']
    installed = []
    missing = []

    for package in required_packages:
        try:
            __import__(package)
            installed.append(package)
        except ImportError:
            missing.append(package)

    print(f"已安裝套件: {installed}")
    if missing:
        print(f"缺少套件: {missing}")
    return len(missing) == 0

def main():
    print("=== Python 開發環境檢查 ===")

    # 檢查 Python 版本
    if check_python():
        print("✅ Python 版本符合要求")
    else:
        print("❌ Python 版本過舊，請升級至 3.8+")

    # 檢查套件
    if check_packages():
        print("✅ 必要套件已安裝")
    else:
        print("❌ 請安裝缺少的套件")

    print("\n環境檢查完成！")

if __name__ == "__main__":
    main()
```

---

## 總結與 Q&A

我們已經涵蓋了 Python 開發環境的完整設定！

- **pip**：Python 套件管理的基礎工具
- **Miniconda**：環境管理和相依性解決方案
- **VSCode**：功能強大的程式碼編輯器
- **Google Colab**：雲端開發和機器學習平台

選擇適合自己的開發環境，開始你的 Python 學習之旅！

有任何問題嗎？
