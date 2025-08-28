import streamlit as st
import logging
import os
import dspy
from dotenv import find_dotenv, load_dotenv
from data.questions import question_1 as example

# 載入環境變數
load_dotenv(find_dotenv())
logger = logging.getLogger(__name__)

def configure_dspy():
    LLM_OPENAI_4O_MINI = "openai/gpt-4o-mini"
    LLM_GEMINI_FLASH_2 = "gemini/gemini-2.5-pro"
    LLM_VERTEX_AI_2 = "vertex_ai/gemini-2.0-flash"
    VERTEX_CREDENTIALS_PATH = './src/utils/credentials.json'
    DSPY_CACHE = True

    """配置 DSPy 模型，包含錯誤處理"""

    try:
        # 備用方案：使用 Gemini Flash
        logger.info("嘗試使用 Gemini Flash 作為備用...")
        dspy.configure(lm=dspy.LM(
            model=LLM_GEMINI_FLASH_2, 
            temperature=0.3, 
            cache=DSPY_CACHE,
            max_tokens=12000
        ))
        logger.info("Gemini Flash 配置成功")
        
    except Exception as gemini_error:
        logger.warning(f"Gemini Flash 配置失敗: {gemini_error}")
        
        try:
            # 最後備用方案：使用 OpenAI
            logger.info("嘗試使用 OpenAI 作為最後備用...")
            dspy.configure(lm=dspy.LM(
                model=LLM_OPENAI_4O_MINI, 
                temperature=0.3, 
                cache=DSPY_CACHE
            ))
            logger.info("OpenAI 配置成功")
            
        except Exception as openai_error:
            logger.error(f"所有模型配置都失敗: {openai_error}")
            raise Exception("無法配置任何 DSPy 模型")

class Corrector(dspy.Signature):
    """
    <role>
        你是一個專精台灣法律考試的教授。你的任務是批改學生針對一個法律案例的回答。
    </role>

    <task>
        根據示範內容(example)去批改使用者回答(student_answer)。
        你的批改步驟如下：
        1.  **識別行為**：逐一分析學生回答中提到的每一個犯罪行為。
        2.  **比對爭點**：將學生的論述與示範內容中的核心法律爭點和論證進行比對。
        3.  **分析差異**：找出學生回答中遺漏的、錯誤的或不夠深入的論點。
        4.  **提供建議**：基於差異分析，提供具體的修改建議和正確的法律觀念。
        5.  **確認題目批改**：確認所有題目都有批改完成，若無，請在是否繼續欄位輸出 "yes"。
    </task>

    <example_format>
        這是一個示範內容(example)的格式範例，它會條列出一個案件中可能涉及的所有行為與對應的法律分析。
        ---
        1.  **甲輸入私下偷記的密碼登入A的手機查看，可能成立刑法第358條侵入電腦罪**
            -   客觀上甲未經持有人A同意，輸入其手號密碼而登入查看對話內容，該手機自屬A之電腦，客觀構成要件該當。
            -   主觀上甲對於上開情狀既知且欲，且無正當理由，又無其他阻卻違法及罪責事由，成立本罪。
        2.  **甲閱讀A與客戶之對話紀錄，可能成立刑法第315條妨害書信秘密罪**
            -   客觀上...自非本罪客體，故甲不成立本罪。
            -   且學說上亦有認為...依此見解，甲觀看對話紀錄內容行為自不能夠成立本罪。
        ---
    </example_format>

    <output_format>
        請嚴格遵循以下格式，針對學生回答中的每一個案件分析，逐點生成批改建議。

        ---
        **[編號]：[行為描述]，成立[法律條文與罪名]**
        
        **你的作答：**
        「[此處直接引用學生在該點的完整作答文字]」
        
        **擬答與評分重點對比：**
        [此處條列出示範內容中的核心法律爭點。然後，明確指出學生的回答遺漏或錯誤對應了哪些重點。]
        
        **調整建議：**
        [基於前述的對比分析，提供具體、可行的修改建議，應包含正確的法律概念和論證結構。]
        
        **給分與扣分：**
        [將評分重點轉化為具體的給分項目，並標示出學生在該項目的得分情況。]
        - [評分重點一] (X分)： 得分Y分。[簡要說明得分或扣分原因]
        - [評分重點二] (X分)： 得分Y分。[簡要說明得分或扣分原因]
        ---
    </output_format>
    """
    # --- Input ---
    student_answer = dspy.InputField(desc="一個法律系學生的申論題回答。")
    example = dspy.InputField(desc="一份詳細的法律問題擬答或詳解，作為批改的標準答案。")

    # --- Output ---
    correction_suggestion = dspy.OutputField(desc="一份結構化、詳細的批改建議，包含與擬答的對比、修改建議和模擬評分。")
    completness_check = dspy.OutputField(desc="是否所有題目都已批改完成，若無，請輸出 'yes'。", default="no")

def correct_question(student_answer, example):
    """
    選擇適當的主題，後續會用來選擇 RAG 的 database。
    """
    corrector_agent = dspy.ChainOfThought(Corrector)
    continue_check = "yes"
    result = ""
    reasoning = ""

    while continue_check.strip().lower() == "yes":
        output = corrector_agent(student_answer=student_answer, example=example)
        result += output.correction_suggestion
        continue_check = output.completness_check if hasattr(output, 'completness_check') else "no"
        reasoning += output.reasoning if hasattr(output, 'reasoning') else "無法提供推理過程"

    return result, reasoning

def main():
    # 頁面配置
    st.set_page_config(
        page_title="法律考試批改助手",
        page_icon="⚖️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # 初始化 DSPy
    if 'dspy_configured' not in st.session_state:
        with st.spinner('正在設定AI模型...'):
            try:
                configure_dspy()
                st.session_state.dspy_configured = True
                st.success("AI模型設定成功！")
            except Exception as e:
                st.error(f"AI模型設定失敗: {str(e)}")
                st.stop()

    # 標題和說明
    st.title("⚖️ 法律考試批改助手")
    st.markdown("""
    這個工具可以幫助您批改法律考試答案，提供詳細的評分建議和改進意見。
    """)

    # 側邊欄
    with st.sidebar:
        st.header("🔧 工具說明")
        st.markdown("""
        ### 使用步驟：
        1. 在右側文字區域輸入學生的答案
        2. 點擊「開始批改」按鈕
        3. 等待AI分析並生成批改結果
        
        ### 批改內容包含：
        - 與標準答案的對比分析
        - 具體的調整建議
        - 詳細的評分說明
        """)
        
        st.header("📋 範例題目")
        with st.expander("查看題目內容"):
            st.markdown(example)

    # 主要內容區域
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 學生答案輸入")
        student_answer = st.text_area(
            "請在此輸入學生的法律考試答案：",
            height=400,
            placeholder="請輸入完整的法律分析答案..."
        )
        
        # 批改按鈕
        col1_1, col1_2, col1_3 = st.columns([1, 2, 1])
        with col1_2:
            submit_button = st.button(
                "🚀 開始批改",
                type="primary",
                use_container_width=True
            )

    with col2:
        st.header("📊 批改結果")
        
        if submit_button:
            if not student_answer.strip():
                st.warning("請先輸入學生答案！")
            else:
                with st.spinner('正在分析答案，請稍候...'):
                    try:
                        correction, reasoning = correct_question(student_answer, example)
                        
                        # 顯示批改結果
                        st.subheader("📋 批改建議")
                        st.markdown(correction)
                        
                        # 顯示推理過程（可選展開）
                        with st.expander("🔍 查看AI推理過程"):
                            st.markdown(reasoning)
                        
                        # 儲存到session state以便重新整理後還能看到
                        st.session_state.last_correction = correction
                        st.session_state.last_reasoning = reasoning
                        
                    except Exception as e:
                        st.error(f"批改過程中發生錯誤: {str(e)}")
        
        # 如果有之前的批改結果，顯示它們
        elif 'last_correction' in st.session_state:
            st.subheader("📋 批改建議")
            st.markdown(st.session_state.last_correction)
            
            with st.expander("🔍 查看AI推理過程"):
                st.markdown(st.session_state.last_reasoning)
        else:
            st.info("請在左側輸入學生答案，然後點擊「開始批改」按鈕。")

    # 頁腳
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: gray;'>"
        "法律考試批改助手 | 由 AI 技術驅動"
        "</p>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()