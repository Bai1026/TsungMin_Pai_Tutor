import logging
import os
import logging
import dspy
from dotenv import find_dotenv, load_dotenv
from rich import print
from data.questions import question_1 as example

load_dotenv(find_dotenv())
logger = logging.getLogger(__name__)

def configure_dspy():
    LLM_OPENAI_4O_MINI = "openai/gpt-4o"
    LLM_GEMINI_FLASH_2 = "gemini/gemini-2.5-flash"
    LLM_VERTEX_AI_2 = "vertex_ai/gemini-2.0-flash"
    VERTEX_CREDENTIALS_PATH = './src/utils/credentials.json'
    # DSPY_MODEL = LLM_VERTEX_AI_2
    DSPY_CACHE = True

    """配置 DSPy 模型，包含錯誤處理"""
    try:
        # 嘗試使用 Vertex AI
        if os.path.exists(VERTEX_CREDENTIALS_PATH):
            logger.info("嘗試使用 Vertex AI 憑證檔案...")
            dspy.configure(lm=dspy.LM(
                model=LLM_VERTEX_AI_2, 
                temperature=0.3, 
                cache=DSPY_CACHE,
                vertex_credentials=VERTEX_CREDENTIALS_PATH
            ))
            logger.info("Vertex AI 配置成功")
        else:
            # 備用方案：使用環境變數設定的 Vertex AI
            logger.info("嘗試使用環境變數的 Vertex AI 配置...")
            dspy.configure(lm=dspy.LM(
                model=LLM_VERTEX_AI_2, 
                temperature=0.3, 
                cache=DSPY_CACHE
            ))
            logger.info("環境變數 Vertex AI 配置成功")
            
    except Exception as vertex_error:
        logger.warning(f"Vertex AI 配置失敗: {vertex_error}")
        
        try:
            # 備用方案：使用 Gemini Flash
            logger.info("嘗試使用 Gemini Flash 作為備用...")
            dspy.configure(lm=dspy.LM(
                model=LLM_GEMINI_FLASH_2, 
                temperature=0.3, 
                cache=DSPY_CACHE
            ))
            logger.info("Gemini Flash 配置成功")
            global DSPY_MODEL
            DSPY_MODEL = LLM_GEMINI_FLASH_2
            
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
                DSPY_MODEL = LLM_OPENAI_4O_MINI
                
            except Exception as openai_error:
                logger.error(f"所有模型配置都失敗: {openai_error}")
                raise Exception("無法配置任何 DSPy 模型")

configure_dspy()            

import dspy

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
        5.  **模擬評分**：根據核心爭點的掌握度，給出一個模擬的評分。
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

    <example_explanation>
        從上述的示範內容(example)中，我們可以拆解出每一個分析單元的核心要素。
        - **行為**：甲輸入私下偷記的密碼登入A的手機查看
        - **法律評價**：可能成立刑法第358條侵入電腦罪
        - **示範內容詳解（評分重點）**：
            -   客觀構成要件：手機是電腦、未經同意輸入密碼。
            -   主觀構成要件：具備故意。
            -   違法性與罪責：無正當理由（無故）、無阻卻事由。
    </example_explanation>

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


def correct_question(student_answer, example):
    """
    選擇適當的主題，後續會用來選擇 RAG 的 database。
    """
    corrector_agent = dspy.ChainOfThought(Corrector)
    output = corrector_agent(student_answer=student_answer, example=example)
    result = output.correction_suggestion
    reasoning = output.reasoning if hasattr(output, 'reasoning') else "無法提供推理過程"

    return result, reasoning


student_answer = input("請輸入學生的法律考試回答：\n")
example = example  # 從 data/questions.py 匯入的示範內容
correction, reasoning = correct_question(student_answer, example)
print("\n=== 批改建議 ===")
print(correction)
print("\n=== 推理過程 ===")
print(reasoning)

