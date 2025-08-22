import os
import logging
from typing import Dict, List, Optional
from rich import print
from dotenv import find_dotenv, load_dotenv

# 導入我們的模組
from test_topic_module import choose_topic, topic_metadata
from rag.index_rag import LawRAGPipeline

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 載入環境變數
load_dotenv(find_dotenv())

class LawBotAgent:
    """
    法律機器人代理，整合主題選擇和 RAG 檢索功能
    """
    
    def __init__(self, openai_api_key: str = None):
        """
        初始化法律機器人代理
        
        Args:
            openai_api_key: OpenAI API 金鑰
        """
        # 取得 API 金鑰
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("未提供 OPENAI_API_KEY")
        
        # 初始化 RAG Pipeline
        self.rag_pipeline = LawRAGPipeline(self.openai_api_key)
        
        # TODO: 這邊會動態新增, 要改對應的 db
        # 主題到資料檔案的映射
        self.topic_to_file_mapping = {
            '侵害生命法益之犯罪': 'specific_offences_ch1.txt',
            '侵害健康法益之犯罪': 'qa.txt',  # 暫時使用通用資料庫
            '侵害自由法益犯罪': 'qa.txt',      # 暫時使用通用資料庫
            '侵害名譽及信用犯罪': 'qa.txt',    # 暫時使用通用資料庫
            '侵害秘密犯罪': 'qa.txt',          # 暫時使用通用資料庫
            '侵害個別財產法益之犯罪': 'specific_offences_ch6.txt', # 暫時使用通用資料庫
            'rag': 'qa.txt',                   # 一般法律諮詢
            'others': None                     # 非法律問題
        }
        
        # 資料檔案的基礎路徑
        self.data_base_path = "/Users/zoungming/Desktop/Codes/TsungMin_Pai_Tutor/Law_Bot/rag/data"
        
        logger.info("法律機器人代理初始化完成")
    
    def process_query(self, user_query: str, verbose: bool = True) -> Dict:
        """
        處理使用者查詢的主要方法
        
        Args:
            user_query: 使用者的法律問題
            verbose: 是否顯示詳細過程
            
        Returns:
            包含處理結果的字典
        """
        result = {
            'user_query': user_query,
            'chosen_topic': None,
            'data_file': None,
            'retrieved_docs': [],
            'answer': None,
            'source_documents': [],
            'error': None
        }
        
        try:
            # 步驟 1: 主題選擇
            if verbose:
                print(f"🔍 步驟 1: 分析使用者問題...")
                print(f"問題: {user_query}")
            
            chosen_topic, chosen_topic_reasoning = choose_topic(user_query)
            result['chosen_topic'] = chosen_topic
            result['chosen_topic_reasoning'] = chosen_topic_reasoning
            
            if verbose:
                print(f"✅ 選擇的主題: {chosen_topic}")
            
            # 檢查是否為非法律問題
            if chosen_topic == 'others':
                result['answer'] = "抱歉，我是法律專業助手，只能回答法律相關問題。請提出刑法相關的問題。"
                return result
            
            # 步驟 2: 取得對應的資料檔案
            data_file_name = self.topic_to_file_mapping.get(chosen_topic)
            if not data_file_name:
                result['error'] = f"未找到主題 '{chosen_topic}' 對應的資料檔案"
                return result
            
            data_file_path = os.path.join(self.data_base_path, data_file_name)
            result['data_file'] = data_file_path
            
            if verbose:
                print(f"📁 步驟 2: 載入對應資料庫...")
                print(f"資料檔案: {data_file_name}")
            
            # 檢查檔案是否存在
            if not os.path.exists(data_file_path):
                result['error'] = f"資料檔案不存在: {data_file_path}"
                return result
            
            # 步驟 3: 載入或建立向量索引
            if verbose:
                print(f"🔄 步驟 3: 載入向量索引...")
            
            # 嘗試載入現有索引
            self.rag_pipeline.load_existing_index(data_file_path)
            
            # 如果沒有現有索引，建立新的
            if not self.rag_pipeline.vectorstore:
                if verbose:
                    print(f"⚠️ 未找到現有索引，建立新索引...")
                self.rag_pipeline.index_documents(data_file_path)
            
            if verbose:
                print(f"✅ 向量索引載入完成")
            
            # 步驟 4: 檢索相關文件
            if verbose:
                print(f"🔍 步驟 4: 檢索相關文件...")
            
            retrieved_docs = self.rag_pipeline.vectorstore.similarity_search(
                user_query, 
                k=3  # 檢索前3個最相關的片段
            )
            result['retrieved_docs'] = retrieved_docs
            
            if verbose:
                print(f"✅ 檢索到 {len(retrieved_docs)} 個相關文件片段")
            
            # 步驟 5: 產生回答
            if verbose:
                print(f"🤖 步驟 5: 產生 AI 回答...")
            
            qa_result = self.rag_pipeline.query(user_query)
            result['answer'] = qa_result['answer']
            result['source_documents'] = qa_result['source_documents']
            
            if verbose:
                print(f"✅ 回答產生完成")
            
            return result
            
        except Exception as e:
            error_msg = f"處理查詢時發生錯誤: {str(e)}"
            logger.error(error_msg)
            result['error'] = error_msg
            return result
    
    def display_result(self, result: Dict):
        """
        顯示處理結果
        
        Args:
            result: process_query 回傳的結果字典
        """
        print("\n" + "="*80)
        print("🤖 法律機器人查詢結果")
        print("="*80)
        
        print(f"📝 使用者問題: {result['user_query']}")
        print(f"🎯 選擇主題: {result['chosen_topic']}")
        
        if result['data_file']:
            print(f"📁 使用資料庫: {os.path.basename(result['data_file'])}")
        
        if result['error']:
            print(f"❌ 錯誤: {result['error']}")
            return
        
        if result['retrieved_docs']:
            print(f"🔍 檢索片段數: {len(result['retrieved_docs'])}")
        
        if result['answer']:
            print(f"\n💡 AI 回答:")
            print("-" * 50)
            print(result['answer'])
            print("-" * 50)
        
        if result['source_documents']:
            print(f"\n📚 參考資料來源:")
            for i, doc in enumerate(result['source_documents'], 1):
                title = doc.metadata.get('title', '未知')
                section = doc.metadata.get('section', '未知')
                print(f"{i}. {title} - {section}")
    
    def display_detailed_retrieval(self, result: Dict):
        """
        顯示詳細的檢索結果
        
        Args:
            result: process_query 回傳的結果字典
        """
        if not result['retrieved_docs']:
            print("沒有檢索到相關文件")
            return
        
        print("\n" + "="*80)
        print("🔍 詳細檢索結果")
        print("="*80)
        
        for i, doc in enumerate(result['retrieved_docs'], 1):
            print(f"\n片段 {i}:")
            print(f"標題: {doc.metadata.get('title', '未知')}")
            print(f"章節: {doc.metadata.get('section', '未知')}")
            print(f"題目編號: {doc.metadata.get('question_number', '未知')}")
            print(f"類型: {doc.metadata.get('type', '未知')}")
            print(f"內容長度: {len(doc.page_content)} 字元")
            print("-" * 40)
            # 顯示前300個字元
            preview = doc.page_content[:300]
            print(preview)
            if len(doc.page_content) > 300:
                print("...")
            print("-" * 40)

def main():
    """
    主要執行函式，提供互動式查詢介面
    """
    try:
        # 初始化法律機器人代理
        agent = LawBotAgent()
        
        print("⚖️ 法律機器人代理已啟動")
        print("輸入 'quit' 或 'exit' 離開")
        print("輸入 'help' 查看可用指令")
        print("-" * 50)
        
        while True:
            try:
                user_input = input("\n🔍 請輸入您的法律問題: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', '退出']:
                    print("👋 再見！")
                    break
                
                if user_input.lower() in ['help', '幫助']:
                    print("""
📖 可用指令:
- 直接輸入法律問題進行查詢
- 'detailed' + 問題: 顯示詳細檢索過程
- 'help': 顯示此幫助資訊
- 'quit' 或 'exit': 離開程式

🎯 範例問題:
- 某人故意殺害他人，應該如何論處？
- 甲竊取他人財物後被發現，為了脫免逮捕而使用暴力
- 什麼是準強盜罪？
- 竊盜罪的構成要件有哪些？
                    """)
                    continue
                
                # 檢查是否要顯示詳細過程
                verbose = False
                if user_input.lower().startswith('detailed '):
                    verbose = True
                    user_input = user_input[9:]  # 移除 'detailed ' 前綴
                
                # 處理查詢
                result = agent.process_query(user_input, verbose=verbose)
                
                # 顯示結果
                agent.display_result(result)
                
                # 如果是詳細模式，也顯示檢索細節
                if verbose:
                    agent.display_detailed_retrieval(result)
                
            except KeyboardInterrupt:
                print("\n👋 再見！")
                break
            except Exception as e:
                print(f"❌ 發生錯誤: {e}")
                
    except Exception as e:
        print(f"❌ 初始化失敗: {e}")
        print("請檢查 OPENAI_API_KEY 是否已正確設定")

if __name__ == "__main__":
    main()
