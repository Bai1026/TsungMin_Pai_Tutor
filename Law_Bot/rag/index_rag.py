import os
from typing import List, Dict
import re
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain.schema import Document
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# 使用 Gemini 相關的匯入
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings

class LawRAGPipeline:
    def __init__(self, google_api_key: str = None, persist_directory: str = None):
        """
        初始化法律 RAG Pipeline (使用 Gemini)
        
        Args:
            google_api_key: Google API 金鑰
            persist_directory: 向量資料庫儲存目錄（如果不指定，會根據檔案名稱自動產生）
        """
        
        # 如果沒有提供 API 金鑰，嘗試從環境變數載入
        if not google_api_key:
            # 嘗試載入多個可能的 .env 檔案位置
            env_paths = [
                ".env",                                    # 當前目錄
                "../.env",                                # 上層目錄
                "/Users/zoungming/Desktop/Codes/TsungMin_Pai_Tutor/Law_Bot/.env",  # 專案根目錄
                "/Users/zoungming/Desktop/Codes/TsungMin_Pai_Tutor/Law_Bot/rag/.env"  # rag 目錄
            ]
            
            for env_path in env_paths:
                if os.path.exists(env_path):
                    print(f"📁 載入環境變數檔案：{env_path}")
                    load_dotenv(env_path)
                    break
            else:
                print("⚠️ 未找到 .env 檔案，嘗試使用系統環境變數")
            
            # 嘗試取得 API 金鑰
            google_api_key = (
                os.getenv("GEMINI_API_KEY") or 
                os.getenv("GOOGLE_API_KEY")
            )
            
            if not google_api_key:
                raise ValueError("未找到 GEMINI_API_KEY 或 GOOGLE_API_KEY。請設定環境變數或直接傳入 api_key 參數")
        
        # 設定環境變數
        os.environ["GOOGLE_API_KEY"] = google_api_key
        
        print(f"🔑 使用 API 金鑰：{google_api_key[:10]}...{google_api_key[-5:]}")
        
        try:
            # 使用 Gemini 的 embedding 模型
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001"  # Gemini 的 embedding 模型
            )
            print("✅ Embedding 模型初始化成功")
        except Exception as e:
            print(f"❌ Embedding 模型初始化失敗：{e}")
            raise
        
        self.persist_directory = persist_directory
        self.vectorstore = None
        self.qa_chain = None
        
        # 法律專用的文本分割器設定
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200,
            chunk_overlap=200,
            separators=["\n\n", "\n", "。", "；", "，", " ", ""]
        )
    
    def parse_law_document(self, text: str) -> List[Document]:
        """
        解析法律考試文件，按題目分割
        
        Args:
            text: 原始文本
            
        Returns:
            Document 列表
        """
        documents = []
        
        # 更靈活的題目分割模式
        patterns = [
            r'\d+\.\s*\d+[年]?[^0-9]*?\d+',  # 原始模式
            r'\d+\.\s*[^\n]*',  # 簡化模式：數字.開頭
            r'【.*?】',  # 標題模式
            r'第\d+題',  # 題目編號
        ]
        
        # 先嘗試原始模式
        matches = []
        for pattern in patterns:
            matches = list(re.finditer(pattern, text))
            if matches:
                print(f"使用模式找到 {len(matches)} 個匹配：{pattern}")
                break
        
        if not matches:
            # 如果沒有找到特定模式，按段落分割
            print("未找到特定題目模式，按段落分割")
            paragraphs = text.split('\n\n')
            for i, para in enumerate(paragraphs):
                if para.strip() and len(para.strip()) > 50:  # 過濾太短的段落
                    doc = Document(
                        page_content=para.strip(),
                        metadata={
                            "title": f"段落 {i+1}",
                            "section": "文件內容",
                            "question_number": i + 1,
                            "type": "法律文件"
                        }
                    )
                    documents.append(doc)
        else:
            # 按找到的模式分割
            for i, match in enumerate(matches):
                start = match.start()
                end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
                
                question_text = text[start:end].strip()
                
                if question_text:  # 確保內容不為空
                    # 提取題目標題
                    title_match = re.match(r'([^\n]*)', question_text)
                    title = title_match.group(1) if title_match else f"題目 {i+1}"
                    
                    # 分析題目結構
                    sections = self._extract_sections(question_text)
                    
                    # 為每個部分建立文件
                    for section_name, section_content in sections.items():
                        if section_content.strip():
                            doc = Document(
                                page_content=section_content,
                                metadata={
                                    "title": title,
                                    "section": section_name,
                                    "question_number": i + 1,
                                    "type": "法律考古題"
                                }
                            )
                            documents.append(doc)
        
        print(f"解析出 {len(documents)} 個文件片段")
        return documents
    
    def _extract_sections(self, question_text: str) -> Dict[str, str]:
        """
        提取題目的不同部分（題目、答題架構、爭點記憶等）
        
        Args:
            question_text: 題目文本
            
        Returns:
            各部分內容的字典
        """
        sections = {}
        
        # 提取主要案例事實
        fact_patterns = [
            r'(甲.*?請問.*?罪責？)',
            r'(甲.*?試問.*?如何\?)',
            r'(甲.*?請.*?分析)',
            r'(甲.*?)',  # 更寬鬆的匹配
        ]
        
        for pattern in fact_patterns:
            fact_match = re.search(pattern, question_text, re.DOTALL)
            if fact_match:
                sections["案例事實"] = fact_match.group(1)
                break
        
        # 提取答題架構
        structure_pattern = r'【答題架構】(.*?)(?:【爭點記憶】|$)'
        structure_match = re.search(structure_pattern, question_text, re.DOTALL)
        if structure_match:
            sections["答題架構"] = structure_match.group(1)
        
        # 提取爭點記憶
        points_pattern = r'【爭點記憶】(.*?)(?=\d+\.|$)'
        points_match = re.search(points_pattern, question_text, re.DOTALL)
        if points_match:
            sections["爭點記憶"] = points_match.group(1)
        
        # 如果沒有明確結構，就把整個內容當作一個部分
        if not sections:
            sections["完整內容"] = question_text
            
        return sections
    
    def _get_persist_directory(self, file_path: str) -> str:
        """
        根據檔案路徑生成對應的資料庫目錄路徑
        
        Args:
            file_path: 資料檔案路徑
            
        Returns:
            資料庫目錄路徑
        """
        # 取得檔案名稱（不含副檔名）
        file_name = Path(file_path).stem
        
        # 建立對應的資料庫目錄路徑
        db_path = f"./rag_db/{file_name}_db"
        
        print(f"自動生成資料庫路徑：{db_path}")
        return db_path
    
    def index_documents(self, file_path: str):
        """
        為文件建立向量索引
        
        Args:
            file_path: 文件檔案路徑
        """
        try:
            # 設定資料庫目錄
            self.persist_directory = self._get_persist_directory(file_path)
            
            # 載入文件
            print("載入文件...")
            documents = self.parse_law_document_from_file(file_path)
            
            if not documents:
                print("⚠️ 未解析出任何文件片段")
                return
            
            # 分割文本
            print("分割文本...")
            splits = self.text_splitter.split_documents(documents)
            print(f"分割後共 {len(splits)} 個片段")
            
            # 建立向量索引
            print("建立向量索引...")
            self.vectorstore = Chroma.from_documents(
                documents=splits,
                embedding=self.embeddings,
                persist_directory=self.persist_directory
            )
            
            # 儲存索引
            self.vectorstore.persist()
            
            # 設定問答鏈
            self._setup_qa_chain()
            
            print(f"✅ 向量索引建立完成，共 {len(splits)} 個片段")
            print(f"📁 索引儲存位置：{self.persist_directory}")
            
        except Exception as e:
            print(f"發生錯誤：{e}")
            print("\n建議檢查：")
            print("1. 文件路徑是否正確")
            print("2. 文件編碼是否正確")
            print("3. API 金鑰是否有效")
            print("4. 網路連線是否正常")
            raise
    
    def load_existing_index(self, file_path: str = None):
        """
        載入現有的向量索引
        
        Args:
            file_path: 原始資料檔案路徑（用於生成資料庫路徑）
        """
        if file_path:
            self.persist_directory = self._get_persist_directory(file_path)
        
        if not self.persist_directory:
            print("錯誤：未指定資料庫路徑，請先呼叫 index_documents() 或在 load_existing_index() 中傳入檔案路徑")
            return
        
        if os.path.exists(self.persist_directory):
            try:
                print(f"載入現有索引：{self.persist_directory}")
                self.vectorstore = Chroma(
                    persist_directory=self.persist_directory,
                    embedding_function=self.embeddings
                )
                self._setup_qa_chain()
                print("✅ 現有索引載入成功")
            except Exception as e:
                print(f"❌ 載入現有索引失敗：{e}")
                self.vectorstore = None
        else:
            print(f"📝 未找到現有索引：{self.persist_directory}")
            self.vectorstore = None
    
    def _setup_qa_chain(self):
        """
        設定問答鏈 (使用 Gemini)
        """
        # 法律專用的提示模板
        template = """你是一位專業的法律學者，專精於台灣刑法。請根據以下相關的法律資料回答問題。

相關資料：
{context}

問題：{question}

請提供詳細且準確的法律分析，包括：
1. 相關法條
2. 構成要件分析
3. 學說和實務見解
4. 具體的法律適用

回答："""

        prompt = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        
        # 使用 Gemini Pro 模型
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=GoogleGenerativeAI(
                model="gemini-pro",  # 使用 Gemini Pro 模型
                temperature=0.1,
                max_output_tokens=2048  # 設定最大輸出長度
            ),
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": 5}  # Gemini 上下文較大，可以檢索更多片段
            ),
            chain_type_kwargs={"prompt": prompt},
            return_source_documents=True
        )
    
    def query(self, question: str) -> Dict:
        """
        查詢問題
        
        Args:
            question: 法律問題
            
        Returns:
            包含回答和來源文件的字典
        """
        if not self.qa_chain:
            raise ValueError("請先執行 index_documents() 或 load_existing_index()")
        
        print(f"處理問題：{question}")
        result = self.qa_chain({"query": question})
        
        return {
            "answer": result["result"],
            "source_documents": result["source_documents"]
        }
    
    def search_similar_cases(self, case_description: str, k: int = 3) -> List[Document]:
        """
        搜尋相似案例
        
        Args:
            case_description: 案例描述
            k: 返回的相似案例數量
            
        Returns:
            相似案例文件列表
        """
        if not self.vectorstore:
            raise ValueError("請先執行 index_documents() 或 load_existing_index()")
        
        return self.vectorstore.similarity_search(case_description, k=k)

# 使用範例
def main():
    """
    主要執行函式
    """
    try:
        # 初始化 RAG pipeline（不傳入 API 金鑰，讓它自動從環境變數載入）
        rag = LawRAGPipeline()
        
        # 指定要處理的文件
        data_file = "/Users/zoungming/Desktop/Codes/TsungMin_Pai_Tutor/Law_Bot/rag/data/specific_offences_ch1.txt"
        
        print(f"📁 處理文件：{data_file}")
        
        # 嘗試載入現有索引
        rag.load_existing_index(data_file)
        
        # 如果沒有現有索引，建立新的
        if not rag.vectorstore:
            print("建立新索引...")
            rag.index_documents(data_file)
        
        print("🎉 RAG 系統初始化完成！")
        
        # 簡單測試
        if rag.qa_chain:
            test_question = "什麼是竊盜罪？"
            print(f"\n🧪 測試問題：{test_question}")
            result = rag.query(test_question)
            print(f"✅ 測試成功，回答長度：{len(result['answer'])} 字元")
        
    except Exception as e:
        print(f"❌ 執行失敗：{e}")

if __name__ == "__main__":
    main()