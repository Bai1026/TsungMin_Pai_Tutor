import streamlit as st
import os
from index_rag import LawRAGPipeline
import pandas as pd

# 設定頁面配置
st.set_page_config(
    page_title="法律 RAG 檢索系統",
    page_icon="⚖️",
    layout="wide"
)

# 初始化 session state
if 'rag_pipeline' not in st.session_state:
    st.session_state.rag_pipeline = None
if 'vectorstore_loaded' not in st.session_state:
    st.session_state.vectorstore_loaded = False

def load_rag_pipeline():
    """載入 RAG pipeline"""
    
    # 嘗試多種方式獲取 API 金鑰
    # OPENAI_API_KEY = None
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    if not OPENAI_API_KEY:
        try:
            from dotenv import load_dotenv
            load_dotenv()
            OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        except ImportError:
            pass

    if not OPENAI_API_KEY:
        st.error("❌ 無法取得 OPENAI_API_KEY")
        st.info("""
        請設定 OPENAI_API_KEY，可以使用以下方式之一：
        1. 設定環境變數：`export OPENAI_API_KEY="your-api-key"`
        2. 建立 .env 文件，內容：`OPENAI_API_KEY=your-api-key`
        3. 或者直接在程式碼中設定（不建議用於生產環境）
        """)
        return
    
    if st.session_state.rag_pipeline is None:
        with st.spinner('正在初始化 RAG 系統...'):
            st.session_state.rag_pipeline = LawRAGPipeline(OPENAI_API_KEY)
            
            # 嘗試載入現有索引
            try:
                st.session_state.rag_pipeline.load_existing_index()
                if st.session_state.rag_pipeline.vectorstore:
                    st.session_state.vectorstore_loaded = True
                    st.success("✅ 成功載入現有索引！")
                else:
                    st.warning("⚠️ 未找到現有索引，請先建立索引")
            except Exception as e:
                st.error(f"❌ 載入索引失敗：{e}")

def display_retrieved_data(retrieved_docs, scores=None):
    """顯示檢索到的資料"""
    st.subheader("🔍 檢索到的相關資料")
    
    if not retrieved_docs:
        st.warning("沒有找到相關資料")
        return
    
    # 檢索統計資訊
    st.subheader("📈 檢索統計總覽")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("檢索片段數", len(retrieved_docs))
    
    with col2:
        total_chars = sum(len(doc.page_content) for doc in retrieved_docs)
        st.metric("總字符數", f"{total_chars:,}")
    
    with col3:
        if scores:
            avg_score = sum(scores) / len(scores)
            st.metric("平均相似度", f"{avg_score:.4f}")
    
    with col4:
        unique_sources = len(set(doc.metadata.get('title', '未知') for doc in retrieved_docs))
        st.metric("來源文件數", unique_sources)
    
    # 詳細總覽表格 (像 test_data_retrieval.py)
    st.subheader("📊 檢索結果詳細總覽")
    overview_data = []
    for i, doc in enumerate(retrieved_docs):
        score = scores[i] if scores else "N/A"
        # 內容預覽 (前100字符)
        content_preview = doc.page_content[:100].replace('\n', ' ') + ("..." if len(doc.page_content) > 100 else "")
        
        overview_data.append({
            "排名": i + 1,
            "相似度分數": f"{score:.4f}" if scores else "N/A",
            "標題": doc.metadata.get('title', '未知'),
            "章節": doc.metadata.get('section', '未知'),
            "題目編號": doc.metadata.get('question_number', '未知'),
            "類型": doc.metadata.get('type', '未知'),
            "內容長度": f"{len(doc.page_content)} 字元",
            "內容預覽": content_preview
        })
    
    df = pd.DataFrame(overview_data)
    st.dataframe(df, use_container_width=True, height=300)
    
    # 檢索品質分析
    if scores:
        st.subheader("📊 相似度分數分析")
        col1, col2 = st.columns(2)
        
        with col1:
            # 分數分布圖
            score_df = pd.DataFrame({
                "片段": [f"片段 {i+1}" for i in range(len(scores))],
                "相似度分數": scores
            })
            st.bar_chart(score_df.set_index("片段"))
        
        with col2:
            # 分數統計
            st.metric("最高相似度", f"{max(scores):.4f}")
            st.metric("最低相似度", f"{min(scores):.4f}")
            st.metric("分數範圍", f"{max(scores) - min(scores):.4f}")
            
            # 分數品質評估
            if max(scores) > 0.8:
                quality = "🟢 優秀"
            elif max(scores) > 0.6:
                quality = "🟡 良好"
            else:
                quality = "🔴 需改善"
            st.metric("檢索品質", quality)
    
    # 顯示完整內容的選項
    st.subheader("📄 詳細內容檢視")
    
    # 選擇顯示方式
    display_mode = st.radio(
        "選擇顯示方式：",
        ["標籤頁模式", "連續顯示模式", "表格模式"],
        horizontal=True
    )
    
    if display_mode == "標籤頁模式":
        # 原本的標籤頁顯示，但加上更多資訊
        tab_labels = []
        for i in range(len(retrieved_docs)):
            score_text = f"(分數: {scores[i]:.3f})" if scores else ""
            title_short = retrieved_docs[i].metadata.get('title', '未知')[:20]
            tab_labels.append(f"片段 {i+1} {score_text}")
        
        tabs = st.tabs(tab_labels)
        
        for i, (tab, doc) in enumerate(zip(tabs, retrieved_docs)):
            with tab:
                display_single_document(doc, scores[i] if scores else None, i+1)
    
    elif display_mode == "連續顯示模式":
        # 連續顯示所有文件 (模擬 test_data_retrieval.py 的輸出格式)
        st.markdown("### 🔍 詳細檢索結果 (連續顯示)")
        
        for i, doc in enumerate(retrieved_docs):
            st.markdown("---")
            
            # 模擬 test_data_retrieval.py 的格式
            st.markdown(f"#### 片段 {i+1}:")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**標題：** {doc.metadata.get('title', '未知')}")
                st.write(f"**章節：** {doc.metadata.get('section', '未知')}")
                st.write(f"**題目編號：** {doc.metadata.get('question_number', '未知')}")
                st.write(f"**類型：** {doc.metadata.get('type', '未知')}")
            
            with col2:
                st.write(f"**內容長度：** {len(doc.page_content)} 字元")
                if scores:
                    st.write(f"**相似度分數：** {scores[i]:.4f}")
            
            # 內容預覽 (像 test_data_retrieval.py)
            st.write("**內容預覽：**")
            st.text("─" * 40)
            preview = doc.page_content[:300]
            st.text(preview)
            if len(doc.page_content) > 300:
                st.text("...")
            st.text("─" * 40)
            
            # 展開查看完整內容
            with st.expander(f"� 查看片段 {i+1} 完整內容"):
                display_single_document(doc, scores[i] if scores else None, i+1)
    
    elif display_mode == "表格模式":
        # 表格模式顯示完整內容
        display_table_mode(retrieved_docs, scores)

def display_single_document(doc, score, rank):
    """顯示單個文件的詳細資訊"""
    
    # 詳細資訊標題
    st.markdown(f"### 📄 片段 {rank} 詳細資訊")
    
    # 基本資訊區塊
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("排名", f"#{rank}")
        if score is not None:
            st.metric("相似度分數", f"{score:.4f}")
    
    with col2:
        st.metric("內容長度", f"{len(doc.page_content)} 字元")
        st.metric("字數估計", f"~{len(doc.page_content.replace(' ', ''))}")
    
    with col3:
        st.info(f"""
        **標題：** {doc.metadata.get('title', '未知')}  
        **章節：** {doc.metadata.get('section', '未知')}
        """)
    
    with col4:
        st.info(f"""
        **題目編號：** {doc.metadata.get('question_number', '未知')}  
        **類型：** {doc.metadata.get('type', '未知')}
        """)
    
    # 完整 Metadata 展開
    with st.expander(f"🔍 完整 Metadata (片段 {rank})"):
        st.json(doc.metadata)
        
        # 額外的 metadata 分析
        st.subheader("Metadata 分析")
        metadata_df = pd.DataFrame([
            {"屬性": key, "值": str(value)} 
            for key, value in doc.metadata.items()
        ])
        st.dataframe(metadata_df, use_container_width=True)
    
    # 內容預覽 (像 test_data_retrieval.py 一樣)
    st.subheader("📖 內容預覽 (前 300 字元)")
    preview = doc.page_content[:300]
    st.text_area(
        f"片段 {rank} 內容預覽",
        value=preview + ("..." if len(doc.page_content) > 300 else ""),
        height=150,
        key=f"preview_{rank}",
        disabled=True
    )
    
    # 完整內容
    st.subheader("📝 完整內容")
    
    # 內容顯示選項
    col1, col2 = st.columns(2)
    with col1:
        height_option = st.selectbox(
            f"顯示高度：",
            [200, 300, 400, 500, 600],
            index=2,
            key=f"height_{rank}"
        )
    
    with col2:
        show_line_numbers = st.checkbox(f"顯示行號 (片段 {rank})", key=f"line_numbers_{rank}")
    
    # 完整內容顯示
    if show_line_numbers:
        # 加上行號的顯示
        lines = doc.page_content.split('\n')
        content_with_lines = '\n'.join([f"{i+1:3d}: {line}" for i, line in enumerate(lines)])
        st.text_area(
            f"片段 {rank} 完整內容 (含行號)",
            value=content_with_lines,
            height=height_option,
            key=f"content_full_lines_{rank}",
            disabled=True
        )
    else:
        st.text_area(
            f"片段 {rank} 完整內容",
            value=doc.page_content,
            height=height_option,
            key=f"content_full_{rank}",
            disabled=True
        )
    
    # 內容分析
    with st.expander(f"📊 內容分析 (片段 {rank})"):
        col1, col2 = st.columns(2)
        
        with col1:
            # 字符統計
            st.subheader("字符統計")
            char_stats = {
                "總字符數": len(doc.page_content),
                "總行數": len(doc.page_content.split('\n')),
                "中文字符數": len([c for c in doc.page_content if '\u4e00' <= c <= '\u9fff']),
                "英文字符數": len([c for c in doc.page_content if c.isalpha() and ord(c) < 256]),
                "數字字符數": len([c for c in doc.page_content if c.isdigit()]),
                "標點符號數": len([c for c in doc.page_content if not c.isalnum() and not c.isspace()])
            }
            
            for key, value in char_stats.items():
                st.metric(key, value)
        
        with col2:
            # 關鍵詞分析
            st.subheader("可能的關鍵詞")
            # 簡單的關鍵詞提取
            import re
            words = re.findall(r'[\u4e00-\u9fff]+', doc.page_content)  # 提取中文詞
            word_freq = pd.Series(words).value_counts().head(10)
            if len(word_freq) > 0:
                st.bar_chart(word_freq)
            else:
                st.write("未找到明顯的關鍵詞")
    
    # 可複製的文本 (多種格式)
    with st.expander(f"📋 可複製文本 (片段 {rank})"):
        copy_format = st.radio(
            "選擇複製格式：",
            ["純文本", "Markdown", "JSON格式"],
            key=f"copy_format_{rank}",
            horizontal=True
        )
        
        if copy_format == "純文本":
            st.code(doc.page_content, language="text")
        elif copy_format == "Markdown":
            markdown_content = f"""# 片段 {rank}

## Metadata
- **標題**: {doc.metadata.get('title', '未知')}
- **章節**: {doc.metadata.get('section', '未知')}
- **題目編號**: {doc.metadata.get('question_number', '未知')}
- **類型**: {doc.metadata.get('type', '未知')}
- **相似度分數**: {score:.4f if score else 'N/A'}

## 內容
{doc.page_content}
"""
            st.code(markdown_content, language="markdown")
        else:  # JSON格式
            json_content = {
                "rank": rank,
                "similarity_score": score,
                "metadata": doc.metadata,
                "content": doc.page_content,
                "content_length": len(doc.page_content)
            }
            import json
            st.code(json.dumps(json_content, ensure_ascii=False, indent=2), language="json")

def display_table_mode(retrieved_docs, scores):
    """表格模式顯示所有檢索資料"""
    st.markdown("**📋 所有檢索內容 (表格格式)**")
    
    table_data = []
    for i, doc in enumerate(retrieved_docs):
        score = scores[i] if scores else "N/A"
        table_data.append({
            "排名": i + 1,
            "相似度分數": f"{score:.4f}" if scores else "N/A",
            "標題": doc.metadata.get('title', '未知'),
            "章節": doc.metadata.get('section', '未知'),
            "題目編號": doc.metadata.get('question_number', '未知'),
            "類型": doc.metadata.get('type', '未知'),
            "內容長度": f"{len(doc.page_content)} 字元",
            "完整內容": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
            "完整內容(未截斷)": doc.page_content
        })
    
    df = pd.DataFrame(table_data)
    
    # 顯示選項
    show_full_content = st.checkbox("顯示完整內容 (而非截斷版本)")
    
    if show_full_content:
        # 顯示包含完整內容的表格
        display_df = df.drop(columns=["完整內容"])
        display_df = display_df.rename(columns={"完整內容(未截斷)": "完整內容"})
    else:
        # 顯示截斷版本
        display_df = df.drop(columns=["完整內容(未截斷)"])
    
    st.dataframe(
        display_df, 
        use_container_width=True,
        height=400
    )
    
    # 下載按鈕
    csv = df.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="📥 下載檢索結果 (CSV)",
        data=csv,
        file_name=f"retrieval_results_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

def display_vectorstore_stats():
    """顯示向量資料庫統計資訊"""
    if st.session_state.vectorstore_loaded and st.session_state.rag_pipeline:
        try:
            collection = st.session_state.rag_pipeline.vectorstore._collection
            results = collection.get(include=['documents', 'metadatas'])
            total_docs = len(results['documents'])
            
            st.sidebar.metric("📊 資料庫統計", f"{total_docs} 個文件片段")
            
            # 分析文件類型
            types = [meta.get('type', '未知') for meta in results['metadatas']]
            type_counts = pd.Series(types).value_counts()
            
            st.sidebar.subheader("📈 文件類型分布")
            st.sidebar.bar_chart(type_counts)
            
        except Exception as e:
            st.sidebar.error(f"無法取得統計資訊：{e}")

def main():
    # 標題
    st.title("⚖️ 法律 RAG 檢索系統")
    st.markdown("輸入法律問題，查看系統檢索到的相關資料片段")
    
    # 載入 RAG pipeline
    load_rag_pipeline()
    
    # 側邊欄
    st.sidebar.title("🔧 系統設定")
    
    # 顯示系統狀態
    if st.session_state.vectorstore_loaded:
        st.sidebar.success("✅ 系統已就緒")
        display_vectorstore_stats()
    else:
        st.sidebar.error("❌ 系統未就緒")
        
        # 建立索引按鈕
        if st.sidebar.button("🔄 建立新索引"):
            data_file = "/Users/zoungming/Desktop/Codes/TsungMin_Pai_Tutor/Law_Bot/rag/data/qa.txt"
            if os.path.exists(data_file):
                with st.spinner('正在建立索引...'):
                    try:
                        st.session_state.rag_pipeline.index_documents(data_file)
                        st.session_state.vectorstore_loaded = True
                        st.rerun()
                    except Exception as e:
                        st.error(f"建立索引失敗：{e}")
            else:
                st.error(f"找不到資料文件：{data_file}")
    
    # 檢索設定
    st.sidebar.subheader("🎛️ 檢索設定")
    k_value = st.sidebar.slider("檢索片段數量", 1, 10, 5)
    show_scores = st.sidebar.checkbox("顯示相似度分數", True)
    
    # 主要介面
    if st.session_state.vectorstore_loaded:
        # 問題輸入
        st.subheader("❓ 輸入您的法律問題")
        question = st.text_input(
            "請輸入問題：",
            placeholder="例如：甲竊取他人財物後被發現，為了脫免逮捕而使用暴力，這樣的行為如何定罪？"
        )
        
        # 範例問題按鈕
        st.subheader("💡 範例問題")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("竊盜罪構成要件"):
                question = "竊盜罪的構成要件有哪些？"
                st.rerun()
                
        with col2:
            if st.button("準強盜罪"):
                question = "什麼是準強盜罪？構成要件有哪些？"
                st.rerun()
                
        with col3:
            if st.button("竊盜與強盜區別"):
                question = "竊盜罪和強盜罪的區別是什麼？"
                st.rerun()
        
        # 執行檢索
        if question:
            with st.spinner('正在檢索相關資料...'):
                try:
                    if show_scores:
                        results = st.session_state.rag_pipeline.vectorstore.similarity_search_with_score(
                            question, k=k_value
                        )
                        retrieved_docs = [doc for doc, score in results]
                        scores = [score for doc, score in results]
                    else:
                        retrieved_docs = st.session_state.rag_pipeline.vectorstore.similarity_search(
                            question, k=k_value
                        )
                        scores = None
                    
                    # 顯示檢索結果
                    display_retrieved_data(retrieved_docs, scores)
                    
                    # QA Validation 工具
                    st.subheader("🔍 QA Validation 工具")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        # 匯出檢索資料為 JSON
                        export_data = []
                        for i, doc in enumerate(retrieved_docs):
                            export_data.append({
                                "rank": i + 1,
                                "similarity_score": scores[i] if scores else None,
                                "question": question,
                                "metadata": doc.metadata,
                                "content": doc.page_content,
                                "content_length": len(doc.page_content)
                            })
                        
                        import json
                        json_data = json.dumps(export_data, ensure_ascii=False, indent=2)
                        st.download_button(
                            label="📄 匯出檢索資料 (JSON)",
                            data=json_data,
                            file_name=f"qa_validation_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json"
                        )
                    
                    with col2:
                        # 檢索品質分析
                        if scores:
                            avg_score = sum(scores) / len(scores)
                            max_score = max(scores)
                            min_score = min(scores)
                            
                            st.metric("平均相似度", f"{avg_score:.4f}")
                            st.metric("最高相似度", f"{max_score:.4f}")
                            st.metric("最低相似度", f"{min_score:.4f}")
                    
                    # 檢索資料統計分析
                    with st.expander("📊 檢索資料統計分析"):
                        # 內容長度分布
                        lengths = [len(doc.page_content) for doc in retrieved_docs]
                        st.subheader("內容長度分布")
                        st.bar_chart(pd.DataFrame({"片段": range(1, len(lengths)+1), "長度": lengths}).set_index("片段"))
                        
                        # 文件類型分析
                        types = [doc.metadata.get('type', '未知') for doc in retrieved_docs]
                        type_counts = pd.Series(types).value_counts()
                        if len(type_counts) > 1:
                            st.subheader("檢索文件類型分布")
                            st.bar_chart(type_counts)
                        
                        # 來源分析
                        sources = [doc.metadata.get('title', '未知') for doc in retrieved_docs]
                        source_counts = pd.Series(sources).value_counts()
                        if len(source_counts) > 1:
                            st.subheader("來源文件分布")
                            st.bar_chart(source_counts)
                    
                    # 顯示完整問答（可選）
                    if st.checkbox("🤖 顯示 AI 回答"):
                        with st.spinner('正在產生回答...'):
                            try:
                                result = st.session_state.rag_pipeline.query(question)
                                st.subheader("🎯 AI 回答")
                                st.write(result['answer'])
                                
                                with st.expander("📚 參考資料來源"):
                                    for i, doc in enumerate(result['source_documents']):
                                        st.write(f"{i+1}. {doc.metadata.get('title', '未知')} - {doc.metadata.get('section', '未知')}")
                                        
                            except Exception as e:
                                st.error(f"產生回答時發生錯誤：{e}")
                    
                except Exception as e:
                    st.error(f"檢索過程中發生錯誤：{e}")
    else:
        st.warning("⚠️ 請先載入或建立索引才能使用檢索功能")

if __name__ == "__main__":
    main()