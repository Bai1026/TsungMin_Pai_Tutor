# 法律 RAG 系統

這是一個使用 LangChain 建立的法律問答 RAG (Retrieval-Augmented Generation) 系統。

## 設定

1. **安裝依賴套件**：
```bash
pip install streamlit pandas langchain-openai langchain-community python-dotenv
```

2. **設定 OpenAI API 金鑰**：
   
   方法一：環境變數
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
   
   方法二：建立 .env 文件
   ```bash
   cp rag/.env.example rag/.env
   # 然後編輯 .env 文件，填入您的 API 金鑰
   ```

## 使用方式

1. **執行 Streamlit 網頁介面**：
```bash
cd rag
streamlit run ui.py
```

2. **命令列檢索測試**：
```bash
cd rag
python test_data_retrieval.py
```

3. **直接使用 RAG Pipeline**：
```bash
cd rag
python index_rag.py
```

## 功能特色

- 📄 法律文件解析和索引
- 🔍 語意搜尋和檢索
- 💬 智能問答
- 📊 檢索結果分析
- 🌐 網頁介面操作

## 安全注意事項

⚠️ **重要**：請勿將 API 金鑰提交到 git repository 中
- 使用 .env 文件存放敏感資訊
- .env 文件已被 .gitignore 排除
- 使用 .env.example 作為設定範本
