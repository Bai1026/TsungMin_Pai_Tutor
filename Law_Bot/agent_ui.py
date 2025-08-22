import streamlit as st
import os
from typing import Dict
import pandas as pd
from agent import LawBotAgent

# 設定頁面配置
st.set_page_config(
    page_title="⚖️ 法律機器人代理",
    page_icon="🤖",
    layout="wide"
)

# 初始化 session state
if 'agent' not in st.session_state:
    st.session_state.agent = None
if 'last_result' not in st.session_state:
    st.session_state.last_result = None

def load_agent():
    """載入法律機器人代理"""
    
    # 嘗試多種方式獲取 API 金鑰
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
        """)
        return None
    
    if st.session_state.agent is None:
        with st.spinner('正在初始化法律機器人代理...'):
            try:
                st.session_state.agent = LawBotAgent(OPENAI_API_KEY)
                st.success("✅ 法律機器人代理初始化成功！")
                return st.session_state.agent
            except Exception as e:
                st.error(f"❌ 初始化失敗：{e}")
                return None
    
    return st.session_state.agent

def display_classification_result(result: Dict):
    """顯示分類主題結果"""
    st.subheader("🎯 主題分類結果")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("選擇的主題", result['chosen_topic'])
    
    with col2:
        if result['data_file']:
            db_name = os.path.basename(result['data_file'])
            st.metric("使用資料庫", db_name)
    
    # 主題說明
    if result['chosen_topic'] in st.session_state.agent.topic_to_file_mapping:
        # 從 topic_metadata 取得說明
        from test_topic_module import topic_metadata
        if result['chosen_topic'] in topic_metadata:
            with st.expander("📖 主題詳細說明"):
                st.write(topic_metadata[result['chosen_topic']])
    # 主題選擇原因
    if 'chosen_topic_reasoning' in result:
        st.subheader("📝 主題選擇推理")
        st.write(result['chosen_topic_reasoning'])

def display_reference_data(result: Dict):
    """顯示參考資料"""
    st.subheader("📚 參考資料")
    
    if not result['retrieved_docs']:
        st.warning("沒有找到相關參考資料")
        return
    
    # 參考資料統計
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("檢索片段數", len(result['retrieved_docs']))
    
    with col2:
        total_chars = sum(len(doc.page_content) for doc in result['retrieved_docs'])
        st.metric("總字符數", f"{total_chars:,}")
    
    with col3:
        unique_sources = len(set(doc.metadata.get('title', '未知') for doc in result['retrieved_docs']))
        st.metric("來源文件數", unique_sources)
    
    with col4:
        avg_length = total_chars // len(result['retrieved_docs'])
        st.metric("平均片段長度", f"{avg_length:,}")
    
    # 參考資料列表
    st.subheader("📄 參考資料詳細內容")
    
    # 顯示方式選擇
    display_mode = st.radio(
        "選擇顯示方式：",
        ["卡片模式", "表格模式", "完整內容"],
        horizontal=True
    )
    
    if display_mode == "卡片模式":
        for i, doc in enumerate(result['retrieved_docs'], 1):
            with st.container():
                st.markdown(f"### 📄 參考資料 {i}")
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.info(f"""
                    **標題：** {doc.metadata.get('title', '未知')}  
                    **章節：** {doc.metadata.get('section', '未知')}  
                    **題目編號：** {doc.metadata.get('question_number', '未知')}  
                    **類型：** {doc.metadata.get('type', '未知')}  
                    **內容長度：** {len(doc.page_content)} 字元
                    """)
                
                with col2:
                    # 內容預覽
                    preview = doc.page_content[:200] + ("..." if len(doc.page_content) > 200 else "")
                    st.text_area(
                        f"內容預覽 {i}",
                        value=preview,
                        height=100,
                        key=f"preview_{i}",
                        disabled=True
                    )
                
                # 展開查看完整內容
                with st.expander(f"🔍 查看參考資料 {i} 完整內容"):
                    st.text_area(
                        f"完整內容 {i}",
                        value=doc.page_content,
                        height=300,
                        key=f"full_content_{i}",
                        disabled=True
                    )
                
                st.divider()
    
    elif display_mode == "表格模式":
        # 建立表格資料
        table_data = []
        for i, doc in enumerate(result['retrieved_docs'], 1):
            content_preview = doc.page_content[:100].replace('\n', ' ') + ("..." if len(doc.page_content) > 100 else "")
            table_data.append({
                "序號": i,
                "標題": doc.metadata.get('title', '未知'),
                "章節": doc.metadata.get('section', '未知'),
                "題目編號": doc.metadata.get('question_number', '未知'),
                "類型": doc.metadata.get('type', '未知'),
                "內容長度": f"{len(doc.page_content)} 字元",
                "內容預覽": content_preview
            })
        
        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True, height=400)
        
        # 下載按鈕
        csv = df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 下載參考資料 (CSV)",
            data=csv,
            file_name=f"reference_data_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    else:  # 完整內容模式
        tabs = st.tabs([f"參考資料 {i}" for i in range(1, len(result['retrieved_docs']) + 1)])
        
        for i, (tab, doc) in enumerate(zip(tabs, result['retrieved_docs'])):
            with tab:
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.subheader("📋 文件資訊")
                    st.write(f"**標題：** {doc.metadata.get('title', '未知')}")
                    st.write(f"**章節：** {doc.metadata.get('section', '未知')}")
                    st.write(f"**題目編號：** {doc.metadata.get('question_number', '未知')}")
                    st.write(f"**類型：** {doc.metadata.get('type', '未知')}")
                    st.write(f"**內容長度：** {len(doc.page_content)} 字元")
                    
                    # Metadata 詳細資訊
                    with st.expander("🔍 完整 Metadata"):
                        st.json(doc.metadata)
                
                with col2:
                    st.subheader("📝 完整內容")
                    st.text_area(
                        f"參考資料 {i+1} 完整內容",
                        value=doc.page_content,
                        height=400,
                        key=f"tab_content_{i}",
                        disabled=True
                    )

def display_ai_response(result: Dict):
    """顯示 AI 回答"""
    st.subheader("🤖 AI 回答")
    
    if result['answer']:
        # AI 回答內容
        st.markdown("### 💡 回答內容")
        st.write(result['answer'])
        
        # 來源文件
        if result['source_documents']:
            st.markdown("### 📖 回答依據的來源文件")
            for i, doc in enumerate(result['source_documents'], 1):
                title = doc.metadata.get('title', '未知')
                section = doc.metadata.get('section', '未知')
                st.write(f"{i}. **{title}** - {section}")
        
        # 回答分析
        with st.expander("📊 回答分析"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("回答字數", len(result['answer']))
            
            with col2:
                st.metric("使用來源數", len(result['source_documents']) if result['source_documents'] else 0)
            
            with col3:
                # 簡單的回答品質評估
                word_count = len(result['answer'])
                if word_count > 200:
                    quality = "🟢 詳細"
                elif word_count > 100:
                    quality = "🟡 適中"
                else:
                    quality = "🔴 簡短"
                st.metric("回答詳細度", quality)
    else:
        st.warning("未能產生 AI 回答")

def display_process_flow(result: Dict):
    """顯示處理流程"""
    st.subheader("🔄 處理流程")
    
    # 流程圖
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.success("✅ 1. 問題輸入")
        st.write("✓ 接收使用者問題")
    
    with col2:
        st.success("✅ 2. 主題分類")
        st.write(f"✓ 選擇：{result['chosen_topic']}")
    
    with col3:
        st.success("✅ 3. 資料庫選擇")
        if result['data_file']:
            db_name = os.path.basename(result['data_file'])
            st.write(f"✓ 使用：{db_name}")
    
    with col4:
        st.success("✅ 4. 文件檢索")
        st.write(f"✓ 找到：{len(result['retrieved_docs'])} 個片段")
    
    with col5:
        if result['answer']:
            st.success("✅ 5. 產生回答")
            st.write("✓ AI 回答完成")
        else:
            st.error("❌ 5. 產生回答")
            st.write("✗ 回答失敗")

def main():
    # 標題和說明
    st.title("⚖️ 法律機器人代理")
    st.markdown("輸入法律問題，系統會自動分類主題、檢索相關資料並產生專業回答")
    
    # 載入代理
    agent = load_agent()
    if not agent:
        st.stop()
    
    # 側邊欄設定
    st.sidebar.title("🔧 系統設定")
    
    # 系統狀態
    st.sidebar.success("✅ 系統已就緒")
    
    # 進階設定
    st.sidebar.subheader("⚙️ 進階設定")
    verbose_mode = st.sidebar.checkbox("詳細處理過程", value=False)
    show_process_flow = st.sidebar.checkbox("顯示處理流程", value=True)
    
    # 範例問題
    st.sidebar.subheader("💡 範例問題")
    example_questions = [
        "某人故意殺害他人，應該如何論處？",
        "甲竊取他人財物後被發現，為了脫免逮捕而使用暴力",
        "什麼是準強盜罪？構成要件有哪些？",
        "竊盜罪的構成要件有哪些？",
        "甲男強制乙女發生性關係，觸犯什麼罪？"
    ]
    
    selected_example = st.sidebar.selectbox(
        "選擇範例問題：",
        ["請選擇..."] + example_questions
    )
    
    # 主要介面
    st.subheader("❓ 輸入您的法律問題")
    
    # 問題輸入區域
    col1, col2 = st.columns([4, 1])
    
    with col1:
        if selected_example and selected_example != "請選擇...":
            user_query = st.text_area(
                "請輸入問題：",
                value=selected_example,
                height=100,
                placeholder="例如：甲竊取他人財物後被發現，為了脫免逮捕而使用暴力，這樣的行為如何定罪？"
            )
        else:
            user_query = st.text_area(
                "請輸入問題：",
                height=100,
                placeholder="例如：甲竊取他人財物後被發現，為了脫免逮捕而使用暴力，這樣的行為如何定罪？"
            )
    
    with col2:
        st.write("")  # 空白用於對齊
        st.write("")  # 空白用於對齊
        query_button = st.button("🔍 查詢", type="primary", use_container_width=True)
        clear_button = st.button("🗑️ 清除", use_container_width=True)
    
    # 清除功能
    if clear_button:
        st.session_state.last_result = None
        st.rerun()
    
    # 處理查詢
    if query_button and user_query.strip():
        with st.spinner('🔄 正在處理您的問題...'):
            result = agent.process_query(user_query.strip(), verbose=verbose_mode)
            st.session_state.last_result = result
    
    # 顯示結果
    if st.session_state.last_result:
        result = st.session_state.last_result
        
        # 檢查是否有錯誤
        if result['error']:
            st.error(f"❌ 處理過程中發生錯誤：{result['error']}")
            return
        
        # 顯示處理流程（可選）
        if show_process_flow:
            display_process_flow(result)
            st.divider()
        
        # 建立三個主要區塊的標籤頁
        tab1, tab2, tab3 = st.tabs(["🎯 主題分類", "📚 參考資料", "🤖 AI 回答"])
        
        with tab1:
            display_classification_result(result)
        
        with tab2:
            display_reference_data(result)
        
        with tab3:
            display_ai_response(result)
        
        # 匯出功能
        st.divider()
        st.subheader("📤 匯出結果")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # 匯出完整結果為 JSON
            import json
            export_data = {
                "query": result['user_query'],
                "topic": result['chosen_topic'],
                "database": os.path.basename(result['data_file']) if result['data_file'] else None,
                "retrieved_docs_count": len(result['retrieved_docs']),
                "answer": result['answer'],
                "timestamp": pd.Timestamp.now().isoformat()
            }
            
            json_data = json.dumps(export_data, ensure_ascii=False, indent=2)
            st.download_button(
                label="📄 匯出查詢結果 (JSON)",
                data=json_data,
                file_name=f"law_query_result_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        with col2:
            # 匯出回答為文字檔
            if result['answer']:
                answer_text = f"""法律問題：{result['user_query']}

分類主題：{result['chosen_topic']}

AI 回答：
{result['answer']}

查詢時間：{pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                st.download_button(
                    label="📝 匯出回答 (TXT)",
                    data=answer_text,
                    file_name=f"law_answer_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
        
        with col3:
            # 匯出參考資料
            if result['retrieved_docs']:
                ref_data = []
                for i, doc in enumerate(result['retrieved_docs'], 1):
                    ref_data.append({
                        "序號": i,
                        "標題": doc.metadata.get('title', '未知'),
                        "章節": doc.metadata.get('section', '未知'),
                        "題目編號": doc.metadata.get('question_number', '未知'),
                        "類型": doc.metadata.get('type', '未知'),
                        "內容": doc.page_content
                    })
                
                df = pd.DataFrame(ref_data)
                csv = df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="📊 匯出參考資料 (CSV)",
                    data=csv,
                    file_name=f"law_references_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )

if __name__ == "__main__":
    main()
