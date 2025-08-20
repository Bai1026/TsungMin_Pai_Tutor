import os
from index_rag import LawRAGPipeline
from rich import print

def inspect_retrieval_data(rag_pipeline, question: str, k: int = 5):
    """
    檢查檢索到的資料片段
    
    Args:
        rag_pipeline: RAG pipeline 物件
        question: 查詢問題
        k: 檢索的片段數量
    """
    print(f"檢查問題：{question}")
    print("="*80)
    
    # 使用向量搜尋檢索相關文件
    retrieved_docs = rag_pipeline.vectorstore.similarity_search(question, k=k)
    
    print(f"檢索到 {len(retrieved_docs)} 個相關片段：\n")
    
    for i, doc in enumerate(retrieved_docs):
        print(f"片段 {i+1}:")
        print(f"標題：{doc.metadata.get('title', '未知')}")
        print(f"章節：{doc.metadata.get('section', '未知')}")
        print(f"題目編號：{doc.metadata.get('question_number', '未知')}")
        print(f"類型：{doc.metadata.get('type', '未知')}")
        print(f"內容長度：{len(doc.page_content)} 字元")
        print(f"內容預覽：")
        print("-" * 40)
        # 顯示前300個字元
        preview = doc.page_content[:300]
        print(preview)
        if len(doc.page_content) > 300:
            print("...")
        print("-" * 40)
        print()

def inspect_vectorstore_contents(rag_pipeline, max_documents: int = 10):
    """
    檢查向量資料庫中的所有文件內容
    
    Args:
        rag_pipeline: RAG pipeline 物件
        max_documents: 最大顯示文件數量
    """
    print("向量資料庫內容檢查")
    print("="*80)
    
    # 取得所有文件的資訊
    collection = rag_pipeline.vectorstore._collection
    results = collection.get(include=['documents', 'metadatas'])
    
    total_docs = len(results['documents'])
    print(f"總共有 {total_docs} 個文件片段")
    print()
    
    # 顯示前幾個文件的詳細資訊
    display_count = min(max_documents, total_docs)
    
    for i in range(display_count):
        doc_content = results['documents'][i]
        metadata = results['metadatas'][i] if results['metadatas'] else {}
        
        print(f"文件 {i+1}:")
        print(f"標題：{metadata.get('title', '未知')}")
        print(f"章節：{metadata.get('section', '未知')}")
        print(f"題目編號：{metadata.get('question_number', '未知')}")
        print(f"類型：{metadata.get('type', '未知')}")
        print(f"內容長度：{len(doc_content)} 字元")
        print(f"內容：")
        print("-" * 40)
        print(doc_content[:200])  # 顯示前200個字元
        if len(doc_content) > 200:
            print("...")
        print("-" * 40)
        print()

def test_similarity_scores(rag_pipeline, question: str, k: int = 5):
    """
    測試相似度分數
    
    Args:
        rag_pipeline: RAG pipeline 物件
        question: 查詢問題
        k: 檢索的片段數量
    """
    print(f"相似度分數測試")
    print(f"查詢問題：{question}")
    print("="*80)
    
    # 使用 similarity_search_with_score 方法取得分數
    results = rag_pipeline.vectorstore.similarity_search_with_score(question, k=k)
    
    for i, (doc, score) in enumerate(results):
        print(f"排名 {i+1} (相似度分數: {score:.4f}):")
        print(f"標題：{doc.metadata.get('title', '未知')}")
        print(f"章節：{doc.metadata.get('section', '未知')}")
        print(f"內容預覽：{doc.page_content[:150]}...")
        print("-" * 40)
        print()

def debug_full_retrieval_process(rag_pipeline, question: str):
    """
    完整的檢索過程調試
    
    Args:
        rag_pipeline: RAG pipeline 物件
        question: 查詢問題
    """
    print("完整檢索過程調試")
    print("="*80)
    
    # 1. 檢查檢索到的文件
    print("1. 檢索相關文件：")
    inspect_retrieval_data(rag_pipeline, question, k=5)
    
    # 2. 檢查相似度分數
    print("\n2. 相似度分數分析：")
    test_similarity_scores(rag_pipeline, question, k=5)
    
    # 3. 完整的 QA 過程
    print("\n3. 完整問答過程：")
    try:
        result = rag_pipeline.query(question)
        print(f"最終回答：")
        print(result['answer'])
        print("\n使用的來源文件：")
        for i, doc in enumerate(result['source_documents']):
            print(f"{i+1}. {doc.metadata.get('title', '未知')} - {doc.metadata.get('section', '未知')}")
    except Exception as e:
        print(f"查詢過程中發生錯誤：{e}")

def main():
    # 設定 OpenAI API 金鑰
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    if not OPENAI_API_KEY:
        try:
            from dotenv import load_dotenv
            load_dotenv()
            OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        except ImportError:
            pass
    
    # 初始化 RAG pipeline
    rag = LawRAGPipeline(OPENAI_API_KEY)
    
    try:
        # 載入現有索引
        rag.load_existing_index()
        
        # 如果沒有現有索引，建立新的
        if not rag.vectorstore:
            print("未找到現有索引，建立新索引...")
            data_file = "/Users/zoungming/Desktop/Codes/TsungMin_Pai_Tutor/Law_Bot/rag/data/qa.txt"
            rag.index_documents(data_file)
        
        # # 測試問題
        # test_questions = [
        #     "甲竊取他人財物後被發現，為了脫免逮捕而使用暴力，這樣的行為如何定罪？",
        #     "什麼是準強盗罪？",
        #     "竊盜罪的構成要件"
        # ]

        question = input("請輸入要檢索的問題：").strip()
        test_questions = [question]
        
        # 1. 檢查向量資料庫內容
        print("\n" + "="*100)
        inspect_vectorstore_contents(rag, max_documents=5)
        
        # 2. 對每個問題進行詳細檢索分析
        for question in test_questions:
            print("\n" + "="*100)
            debug_full_retrieval_process(rag, question)
            
            # 等待用戶確認才繼續下一個問題
            input("按 Enter 鍵繼續下一個問題...")
            
    except Exception as e:
        print(f"發生錯誤：{e}")

if __name__ == "__main__":
    main()