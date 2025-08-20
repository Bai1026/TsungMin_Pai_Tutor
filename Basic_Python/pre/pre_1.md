# Python 新手指南：00-A 終端機指令指南

**作者：** tsung-min pai
**單位：** NTUEE

---

## 大綱

### 1 終端機基礎

- 什麼是終端機
- 開啟終端機
- 基本概念與術語

### 2 檔案系統導航

- 目錄結構
- 路徑概念
- 基本導航指令

### 3 檔案與目錄操作

- 建立、刪除、移動
- 檔案權限管理
- 檔案內容檢視

### 4 Python 開發相關指令

- Python 環境管理
- 套件安裝與管理
- 版本控制基礎

---

## 終端機基礎

**什麼是終端機？**

- 文字介面的系統操作工具
- 透過指令與作業系統互動
- 比圖形介面更有效率且功能強大

**開啟終端機：**

**macOS：**

```bash
# 方法 1：Spotlight 搜尋
按 Cmd+Space，輸入 "Terminal"

# 方法 2：Launchpad
Launchpad > 其他 > 終端機

# 方法 3：Finder
應用程式 > 工具程式 > 終端機
```

**Linux：**

```bash
# 方法 1：快捷鍵
Ctrl+Alt+T

# 方法 2：應用程式選單
應用程式 > 系統工具 > 終端機

# 方法 3：右鍵選單
在桌面或檔案管理器中右鍵 > "在終端機中開啟"
```

---

## 基本概念與術語

**重要概念：**

- **Shell**：命令列解譯器（如 bash, zsh）
- **工作目錄**：目前所在的資料夾位置
- **根目錄**：檔案系統的最上層目錄（/）
- **家目錄**：使用者的個人資料夾（~）

**提示符號解讀：**

```bash
# macOS/Linux 一般格式
username@hostname:current_directory$

# 範例
tsung-min@MacBook:~/Documents$

# 符號意義
~ = 家目錄
/ = 根目錄或路徑分隔符號
$ = 一般使用者提示符號
# = root 使用者提示符號
```

---

## 檔案系統導航

**查看當前位置：**

```bash
# 顯示目前工作目錄的完整路徑
pwd
# 輸出範例：/Users/tsung-min/Documents
```

**列出檔案和目錄：**

```bash
# 基本列表
ls

# 詳細資訊列表
ls -l

# 包含隱藏檔案
ls -a

# 詳細資訊 + 隱藏檔案
ls -la

# 以人類易讀格式顯示檔案大小
ls -lh

# 按修改時間排序
ls -lt

# 遞迴顯示所有子目錄內容
ls -R
```

**目錄切換：**

```bash
# 切換到指定目錄
cd Documents

# 切換到上一層目錄
cd ..

# 切換到上兩層目錄
cd ../..

# 切換到家目錄
cd ~
# 或直接
cd

# 切換到根目錄
cd /

# 回到上一個工作目錄
cd -

# 使用絕對路徑
cd /Users/tsung-min/Documents

# 使用相對路徑
cd ./subfolder
```

---

## 路徑概念

**絕對路徑 vs 相對路徑：**

```bash
# 絕對路徑（從根目錄開始）
/Users/tsung-min/Documents/project.py

# 相對路徑（從目前位置開始）
./project.py          # 目前目錄下的檔案
../Documents/file.txt  # 上一層目錄的 Documents 資料夾
~/Desktop/notes.txt    # 家目錄下的 Desktop 資料夾
```

**特殊目錄符號：**

```bash
.   # 目前目錄
..  # 上一層目錄
~   # 家目錄
/   # 根目錄
-   # 上一個工作目錄
```

---

## 檔案與目錄操作

**建立目錄：**

```bash
# 建立單一目錄
mkdir project

# 建立多個目錄
mkdir dir1 dir2 dir3

# 建立巢狀目錄（自動建立上層目錄）
mkdir -p project/src/utils

# 設定目錄權限
mkdir -m 755 secure_folder
```

**建立檔案：**

```bash
# 建立空檔案
touch file.txt

# 建立多個檔案
touch file1.txt file2.txt file3.txt

# 使用 echo 建立含內容的檔案
echo "Hello World" > greeting.txt

# 追加內容到檔案
echo "Second line" >> greeting.txt
```

**複製檔案和目錄：**

```bash
# 複製檔案
cp source.txt destination.txt

# 複製檔案到目錄
cp file.txt ~/Documents/

# 複製多個檔案
cp file1.txt file2.txt ~/backup/

# 複製目錄（遞迴）
cp -r source_folder destination_folder

# 保持檔案屬性的複製
cp -p file.txt backup_file.txt

# 互動式複製（覆蓋前詢問）
cp -i source.txt destination.txt
```

**移動和重新命名：**

```bash
# 重新命名檔案
mv old_name.txt new_name.txt

# 移動檔案到目錄
mv file.txt ~/Documents/

# 移動並重新命名
mv old_file.txt ~/Documents/new_file.txt

# 移動目錄
mv old_folder ~/Documents/new_folder

# 移動多個檔案
mv *.txt ~/Documents/
```

**刪除檔案和目錄：**

```bash
# 刪除檔案
rm file.txt

# 刪除多個檔案
rm file1.txt file2.txt

# 互動式刪除（刪除前詢問）
rm -i important_file.txt

# 強制刪除（不詢問）
rm -f file.txt

# 刪除空目錄
rmdir empty_folder

# 遞迴刪除目錄及其內容
rm -r folder_name

# 強制遞迴刪除
rm -rf folder_name

# 安全刪除（移到垃圾桶，僅限 macOS）
trash file.txt
```

---

## 檔案內容檢視

**查看檔案內容：**

```bash
# 顯示完整檔案內容
cat file.txt

# 顯示檔案前幾行
head file.txt
head -n 20 file.txt  # 前 20 行

# 顯示檔案後幾行
tail file.txt
tail -n 10 file.txt  # 後 10 行

# 即時追蹤檔案變化（如日誌檔）
tail -f log.txt

# 分頁查看大檔案
less file.txt
# 在 less 中：空白鍵向下翻頁，b 向上翻頁，q 退出

# 另一個分頁工具
more file.txt
```

**搜尋檔案內容：**

```bash
# 在檔案中搜尋文字
grep "search_term" file.txt

# 忽略大小寫搜尋
grep -i "python" file.txt

# 搜尋多個檔案
grep "function" *.py

# 遞迴搜尋目錄中的所有檔案
grep -r "import" ./project/

# 顯示行號
grep -n "def" main.py

# 顯示比對前後的行
grep -C 3 "error" log.txt
```

---

## 檔案權限管理

**查看檔案權限：**

```bash
# 詳細列出檔案權限
ls -l file.txt

# 輸出範例解讀：
# -rw-r--r-- 1 user group 1024 Oct 15 10:30 file.txt
# ↑ ↑ ↑ ↑     ↑    ↑     ↑    ↑              ↑
# │ │ │ │     │    │     │    │              檔名
# │ │ │ │     │    │     │    修改時間
# │ │ │ │     │    │     檔案大小
# │ │ │ │     │    群組
# │ │ │ │     擁有者
# │ │ │ 其他使用者權限 (r--)
# │ │ 群組權限 (r--)
# │ 擁有者權限 (rw-)
# 檔案類型 (- 表示一般檔案，d 表示目錄)
```

**修改檔案權限：**

```bash
# 使用數字模式設定權限
chmod 755 script.py   # rwxr-xr-x
chmod 644 data.txt    # rw-r--r--
chmod 600 secret.txt  # rw-------

# 使用符號模式修改權限
chmod +x script.py    # 新增執行權限
chmod -w file.txt     # 移除寫入權限
chmod u+w file.txt    # 擁有者新增寫入權限
chmod g-r file.txt    # 群組移除讀取權限
chmod o=r file.txt    # 其他使用者只有讀取權限

# 遞迴修改目錄權限
chmod -R 755 project_folder/
```

**權限數字對照表：**

```
數字  二進位  權限    說明
0     000     ---     無權限
1     001     --x     僅執行
2     010     -w-     僅寫入
3     011     -wx     寫入+執行
4     100     r--     僅讀取
5     101     r-x     讀取+執行
6     110     rw-     讀取+寫入
7     111     rwx     完整權限
```

---

## Python 開發相關指令

**Python 版本管理：**

```bash
# 檢查 Python 版本
python --version
python3 --version

# 檢查 Python 安裝路徑
which python
which python3

# 檢查所有已安裝的 Python 版本
ls /usr/bin/python*
```

**執行 Python 程式：**

```bash
# 執行 Python 檔案
python script.py
python3 script.py

# 直接啟動 Python 互動式介面
python
python3

# 執行 Python 模組
python -m http.server 8000  # 啟動簡單 HTTP 伺服器
python -m pip install numpy # 使用模組方式執行 pip
```

**虛擬環境管理：**

```bash
# 建立虛擬環境
python3 -m venv myproject_env

# 啟動虛擬環境
source myproject_env/bin/activate

# 確認虛擬環境已啟動（提示符號會改變）
(myproject_env) username@hostname:~$

# 停用虛擬環境
deactivate

# 刪除虛擬環境
rm -rf myproject_env
```

**套件管理：**

```bash
# 安裝套件
pip install numpy
pip3 install pandas

# 升級套件
pip install --upgrade requests

# 列出已安裝套件
pip list
pip freeze

# 產生需求檔案
pip freeze > requirements.txt

# 從需求檔案安裝
pip install -r requirements.txt

# 解除安裝套件
pip uninstall matplotlib
```

---

## 進階終端機技巧

**歷史指令：**

```bash
# 查看指令歷史
history

# 重複執行上一個指令
!!

# 重複執行指令歷史中的特定指令
!123  # 執行編號 123 的指令

# 搜尋指令歷史
Ctrl+R  # 然後輸入關鍵字

# 清除指令歷史
history -c
```

**指令組合與重新導向：**

```bash
# 指令管線（將前一個指令的輸出傳給下一個）
ls -la | grep ".py"
cat file.txt | grep "import" | wc -l

# 輸出重新導向
ls > file_list.txt        # 覆蓋寫入
ls >> file_list.txt       # 追加寫入
python script.py 2> error.log  # 錯誤輸出重新導向

# 同時重新導向標準輸出和錯誤輸出
python script.py > output.log 2>&1
python script.py &> combined.log

# 丟棄輸出
python script.py > /dev/null 2>&1
```

**背景執行：**

```bash
# 在背景執行指令
python long_running_script.py &

# 查看背景工作
jobs

# 將背景工作調回前台
fg %1  # 調回工作編號 1

# 將前台工作放到背景
Ctrl+Z  # 暫停工作
bg %1   # 在背景繼續執行
```

**檔案搜尋：**

```bash
# 搜尋檔案
find . -name "*.py"              # 搜尋 .py 檔案
find . -type f -name "main*"     # 搜尋檔名以 main 開頭的檔案
find . -type d -name "test*"     # 搜尋目錄名以 test 開頭的資料夾

# 依檔案大小搜尋
find . -size +100M               # 搜尋大於 100MB 的檔案
find . -size -1k                 # 搜尋小於 1KB 的檔案

# 依修改時間搜尋
find . -mtime -7                 # 搜尋 7 天內修改的檔案
find . -mtime +30                # 搜尋 30 天前修改的檔案

# 快速檔案搜尋（需要預先建立資料庫）
locate "*.py"
updatedb  # 更新搜尋資料庫（需要 root 權限）
```

---

## 系統資訊與監控

**系統資訊：**

```bash
# 顯示系統資訊
uname -a        # 完整系統資訊
uname -s        # 作業系統名稱
uname -r        # 核心版本

# 檢查作業系統版本
cat /etc/os-release  # Linux
sw_vers              # macOS

# 檢查磁碟使用量
df -h           # 檔案系統使用量
du -h           # 目錄使用量
du -sh *        # 當前目錄下各項目的大小
```

**程序監控：**

```bash
# 顯示執行中的程序
ps aux          # 所有程序詳細資訊
ps aux | grep python  # 只顯示 Python 程序

# 即時程序監控
top             # 傳統監控工具
htop            # 進階監控工具（需額外安裝）

# 殺死程序
kill PID        # 終止指定 PID 的程序
killall python # 終止所有 Python 程序
```

**網路相關：**

```bash
# 檢查網路連線
ping google.com
ping -c 4 8.8.8.8  # 只 ping 4 次

# 檢查端口是否開啟
netstat -an | grep :8000
lsof -i :8000       # 查看使用 8000 port 的程序

# 下載檔案
curl -O https://example.com/file.zip
wget https://example.com/file.zip  # Linux 通常預裝
```

---

## 版本控制基礎 (Git)

**Git 基本設定：**

```bash
# 設定使用者資訊
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 檢查設定
git config --list
```

**基本 Git 操作：**

```bash
# 初始化 Git 儲存庫
git init

# 複製遠端儲存庫
git clone https://github.com/user/repo.git

# 檢查狀態
git status

# 加入檔案到暫存區
git add file.py
git add .           # 加入所有變更

# 提交變更
git commit -m "Add new feature"

# 查看提交歷史
git log
git log --oneline   # 簡潔格式

# 推送到遠端
git push origin main

# 從遠端拉取更新
git pull origin main
```

---

## 常用快捷鍵

**編輯快捷鍵：**

```bash
Ctrl+A    # 移到行首
Ctrl+E    # 移到行尾
Ctrl+U    # 刪除游標前的所有文字
Ctrl+K    # 刪除游標後的所有文字
Ctrl+W    # 刪除游標前的一個單字
Ctrl+L    # 清除螢幕
```

**移動快捷鍵：**

```bash
Ctrl+B    # 向左移動一個字元
Ctrl+F    # 向右移動一個字元
Alt+B     # 向左移動一個單字
Alt+F     # 向右移動一個單字
```

**歷史快捷鍵：**

```bash
Ctrl+R    # 搜尋指令歷史
Ctrl+P    # 上一個指令
Ctrl+N    # 下一個指令
↑         # 上一個指令
↓         # 下一個指令
```

---

## 實用指令組合範例

**Python 開發工作流程：**

```bash
# 建立專案目錄結構
mkdir -p myproject/{src,tests,docs,data}
cd myproject

# 建立虛擬環境
python3 -m venv venv
source venv/bin/activate

# 安裝開發相依套件
pip install black pytest flake8
pip freeze > requirements.txt

# 建立基本檔案
touch src/__init__.py src/main.py
touch tests/__init__.py tests/test_main.py
touch README.md .gitignore

# 初始化 Git
git init
git add .
git commit -m "Initial project setup"
```

**檔案整理範例：**

```bash
# 找出大檔案並移到備份目錄
find . -size +100M -exec mv {} ~/backup/ \;

# 清理暫存檔案
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +

# 按副檔名整理檔案
mkdir -p sorted/{images,documents,code}
mv *.{jpg,png,gif} sorted/images/
mv *.{pdf,doc,txt} sorted/documents/
mv *.{py,js,html} sorted/code/
```

**系統維護範例：**

```bash
# 檢查磁碟使用量並清理
du -sh * | sort -hr | head -10  # 找出最大的檔案/目錄
df -h                           # 檢查磁碟空間

# 清理系統暫存（macOS）
sudo rm -rf /tmp/*
sudo rm -rf ~/Library/Caches/*

# 更新套件（Linux）
sudo apt update && sudo apt upgrade -y  # Ubuntu/Debian
sudo yum update -y                      # CentOS/RHEL
```

---

## 疑難排解

**常見問題與解決方法：**

**權限問題：**

```bash
# 錯誤：Permission denied
# 解決：檢查並修改權限
ls -la file.txt
chmod +x script.py
sudo chown username:group file.txt
```

**找不到指令：**

```bash
# 錯誤：command not found
# 解決：檢查 PATH 或安裝套件
which python3
echo $PATH
export PATH=/usr/local/bin:$PATH
```

**檔案不存在：**

```bash
# 錯誤：No such file or directory
# 解決：確認路徑和檔名
pwd
ls -la
find . -name "filename*"
```

---

## 總結與 Q&A

我們已經涵蓋了終端機的完整指南！

- **基礎導航**：目錄切換、檔案列表、路徑概念
- **檔案操作**：建立、複製、移動、刪除、權限管理
- **Python 開發**：環境管理、套件安裝、程式執行
- **進階技巧**：指令組合、歷史搜尋、背景執行

掌握這些終端機技能將大幅提升你的開發效率！

有任何問題嗎？
