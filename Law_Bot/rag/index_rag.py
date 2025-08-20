import os
from typing import List, Dict
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain.schema import Document
from langchain_openai import OpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

class LawRAGPipeline:
    def __init__(self, openai_api_key: str, persist_directory: str = "./chroma_db"):
        """
        初始化法律 RAG Pipeline
        
        Args:
            openai_api_key: OpenAI API 金鑰
            persist_directory: 向量資料庫儲存目錄
        """
        os.environ["OPENAI_API_KEY"] = openai_api_key
        
        self.embeddings = OpenAIEmbeddings()
        self.persist_directory = persist_directory
        self.vectorstore = None
        self.qa_chain = None
        
        # 法律專用的文本分割器設定
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
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
    
    def index_documents(self, file_path: str):
        """
        索引文件到向量資料庫
        
        Args:
            file_path: 文件路徑
        """
        print("載入文件...")
        
        # 檢查文件是否存在
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        # 嘗試不同的編碼
        encodings = ['utf-8', 'big5', 'gb2312', 'cp950']
        raw_documents = None
        
        for encoding in encodings:
            try:
                loader = TextLoader(file_path, encoding=encoding)
                raw_documents = loader.load()
                print(f"成功使用 {encoding} 編碼載入文件")
                break
            except UnicodeDecodeError:
                print(f"使用 {encoding} 編碼失敗，嘗試下一個...")
                continue
        
        if not raw_documents:
            raise ValueError("無法使用任何編碼載入文件")
        
        print("解析法律文件...")
        law_documents = []
        for doc in raw_documents:
            print(f"原始文件長度: {len(doc.page_content)}")
            parsed_docs = self.parse_law_document(doc.page_content)
            law_documents.extend(parsed_docs)
        
        print(f"解析出 {len(law_documents)} 個文件片段")
        
        if not law_documents:
            raise ValueError("沒有解析出任何文件片段，請檢查文件格式")
        
        print("分割文本...")
        documents = self.text_splitter.split_documents(law_documents)
        print(f"分割後共 {len(documents)} 個片段")
        
        if not documents:
            raise ValueError("文本分割後沒有產生任何片段")
        
        print("建立向量索引...")
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        self.vectorstore.persist()
        print("索引建立完成！")
        
        self._setup_qa_chain()
    
    def load_existing_index(self):
        """
        載入現有的向量索引
        """
        if os.path.exists(self.persist_directory):
            print("載入現有索引...")
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
            self._setup_qa_chain()
            print("索引載入完成！")
        else:
            print("未找到現有索引，請先執行 index_documents()")
    
    def _setup_qa_chain(self):
        """
        設定問答鏈
        """
        # 法律專用的提示模板
        template = """你是一位專業的法律學者，專精於刑法。請根據以下相關的法律資料回答問題。

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
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=OpenAI(temperature=0.1),
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": 5}  # 檢索前5個最相關的片段
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
    # 設定你的 OpenAI API 金鑰
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    if not OPENAI_API_KEY:
        try:
            from dotenv import load_dotenv
            load_dotenv()
            OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        except ImportError:
            pass
    
    if not OPENAI_API_KEY:
        print("錯誤：請設定 OPENAI_API_KEY 環境變數")
        print("可以使用以下方式之一：")
        print("1. 設定環境變數：export OPENAI_API_KEY='your-api-key'")
        print("2. 建立 .env 文件，內容：OPENAI_API_KEY=your-api-key")
        return
    
    # 初始化 RAG pipeline
    rag = LawRAGPipeline(OPENAI_API_KEY)
    
    # 索引文件
    data_file = "/Users/zoungming/Desktop/Codes/TsungMin_Pai_Tutor/Law_Bot/rag/data/qa.txt"
    
    try:
        # 如果是第一次執行，建立索引
        rag.index_documents(data_file)
        
        # # 查詢範例
        # questions = [
        #     # "甲竊取他人財物後被發現，為了脫免逮捕而使用暴力，這樣的行為如何定罪？",
        #     # "什麼是準強盗罪？構成要件有哪些？",
        #     # "竊盜罪和強盗罪的區別是什麼？"
        #     "會不會成立重傷？"
        # ]
        
        # for question in questions:
        #     print(f"\n{'='*50}")
        #     result = rag.query(question)
        #     print(f"問題：{question}")
        #     print(f"回答：{result['answer']}")
        #     print(f"\n參考資料來源：")
        #     for i, doc in enumerate(result['source_documents']):
        #         print(f"{i+1}. {doc.metadata.get('title', '未知來源')} - {doc.metadata.get('section', '未知章節')}")
                
    except Exception as e:
        print(f"發生錯誤：{e}")
        print("\n建議檢查：")
        print("1. 文件路徑是否正確")
        print("2. 文件編碼是否正確")
        print("3. 文件內容是否有可解析的結構")

if __name__ == "__main__":
    main()