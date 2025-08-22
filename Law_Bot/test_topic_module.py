import dspy
from dotenv import find_dotenv, load_dotenv
from rich import print

import logging
logger = logging.getLogger(__name__)

load_dotenv(find_dotenv())

def configure_dspy():
    LLM_OPENAI_4O_MINI = "openai/gpt-4o-mini"
    LLM_GEMINI_FLASH_2 = "gemini/gemini-2.0-flash"
    DSPY_CACHE = True
    
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


topic_metadata = {
    '侵害生命法益之犯罪': '包含殺人罪章（普通殺人罪、殺直系血親尊親屬罪、義憤殺人罪、生母殺嬰罪、加工自殺罪）、遺棄罪章（單純遺棄罪、違背義務之遺棄罪）、墮胎罪章（自行或聽從墮胎罪、加工墮胎罪、圖利加工墮胎罪、未受囑託或未得承諾之墮胎罪、公然介紹墮胎罪）',
    # '侵害健康法益之犯罪': '包含傷害罪章（普通傷害罪及加重結果犯、重傷罪、義憤傷害罪、傷害直系血親尊親屬罪、加暴行於直系血親尊親屬、加工自傷罪、聚眾鬥毆罪、過失傷害罪、妨害幼童自然發育罪）',
    # '侵害自由法益犯罪': '包含妨害自由罪章（剝奪他人行動自由罪、加重剝奪他人行動自由罪、剝奪直系血親尊親屬行動自由罪、強制罪、恐嚇危害安全罪、侵入住居罪、違法搜索罪）和妨害性自主罪章（強制性交罪、加重強制性交罪、強制猥褻罪、趁機性交猥褻罪、結合犯、與幼童性交猥褻罪、利用權勢性交猥褻罪、詐術性交罪）',
    # '侵害名譽及信用犯罪': '包含公然侮辱罪、誹謗罪、善意發表言論不罰、妨害信用罪等相關犯罪類型',
    # '侵害秘密犯罪': '包含妨害書信秘密罪、窺視竊聽竊錄罪、便利窺視竊聽竊錄及散布竊錄內容罪等侵害隱私秘密之犯罪',
    '侵害個別財產法益之犯罪': '包含竊盜罪章（普通竊盜罪與竊佔罪、加重竊盜罪）、搶奪強盜及海盜罪章（普通搶奪罪、普通強盜罪、準強盜罪、強盜結合罪）、恐嚇及擄人勒贖罪章（恐嚇取財得利罪、擄人勒贖罪）、侵占罪章（普通侵占罪、公務公益侵占罪、業務侵占罪、侵占脫離物罪）',
}

import dspy

"""
ChooseTopic 是一個用於選擇最相關台灣刑法分則主題的模組。
"""
class ChooseTopic(dspy.Signature):
    """
    <role>
        你是一個專精台灣刑法分則的法律助手，能夠根據使用者的法律問題或案例，準確判斷所涉及的犯罪類型並選擇最相關的刑法分則主題。你具備深厚的刑法知識，熟悉各種犯罪的構成要件和分類體系。
    </role>

    <task>
        根據使用者的刑法問題或案例描述，從台灣刑法分則的六大犯罪類型中選擇最相關的主題。請仔細分析問題所涉及的法益侵害類型和具體犯罪行為。
    </task>

    <output_format>
        請選擇一個最相關的刑法分則主題，直接輸出主題名稱。例如：'侵害生命法益之犯罪'
        
        選擇標準：
        1. 優先考慮問題中明確提及的犯罪行為
        2. 分析所侵害的法益類型（生命、健康、自由、名譽信用、秘密、財產）
        3. 考慮犯罪的主要特徵和構成要件
        
        特殊情況處理：
        - 如果使用者問題是一般法律諮詢但不涉及具體刑法分則內容，請輸出 'rag' 以啟用一般法律知識庫搜尋
        - 如果使用者只是想要聊天而非法律問題，請輸出 'others'
        - 如果涉及多個犯罪類型，請選擇最主要或最嚴重的犯罪類型
    </output_format>
    
    <examples>
        範例1：
        使用者問題：「某人故意殺害他人，應該如何論處？」
        分析：涉及故意殺人行為，侵害他人生命法益
        答案：侵害生命法益之犯罪
        
        範例2：
        使用者問題：「甲男強制乙女發生性關係，觸犯什麼罪？」
        分析：涉及強制性交行為，侵害性自主權（自由法益）
        答案：侵害自由法益犯罪
        
        範例3：
        使用者問題：「竊取他人財物會有什麼法律後果？」
        分析：涉及竊盜行為，侵害他人財產法益
        答案：侵害個別財產法益之犯罪
    </examples>
    """
    # --- Input ---
    user_query = dspy.InputField(desc="使用者的刑法問題或案例描述")
    rag_topic_metadata = dspy.InputField(desc="台灣刑法分則犯罪類型分類")

    # --- Output ---
    chosen_topic = dspy.OutputField(desc="選擇的刑法分則犯罪類型")


def get_topic_demos():
    """
    提供台灣刑法分則犯罪分類的示範範例
    """
    rag_topic_metadata = {
        '侵害生命法益之犯罪': '包含殺人罪章、遺棄罪章、墮胎罪章等',
        '侵害健康法益之犯罪': '包含傷害罪章等',
        '侵害自由法益犯罪': '包含妨害自由罪章、妨害性自主罪章等',
        '侵害名譽及信用犯罪': '包含公然侮辱罪、誹謗罪等',
        '侵害秘密犯罪': '包含妨害書信秘密罪、竊聽竊錄罪等',
        '侵害個別財產法益之犯罪': '包含竊盜罪章、搶奪強盜罪章、侵占罪章等'
    }
    
    demos = [
        {
            'user_query': '某人故意殺害他人',
            'rag_topic_metadata': rag_topic_metadata,
            'chosen_topic': '侵害生命法益之犯罪'
        },
        {
            'user_query': '甲男強制乙女發生性關係',
            'rag_topic_metadata': rag_topic_metadata,
            'chosen_topic': '侵害自由法益犯罪'
        },
        {
            'user_query': '竊取他人財物',
            'rag_topic_metadata': rag_topic_metadata,
            'chosen_topic': '侵害個別財產法益之犯罪'
        },
        {
            'user_query': '在網路上公然辱罵他人',
            'rag_topic_metadata': rag_topic_metadata,
            'chosen_topic': '侵害名譽及信用犯罪'
        },
        {
            'user_query': '用拳頭毆打他人造成受傷',
            'rag_topic_metadata': rag_topic_metadata,
            'chosen_topic': '侵害健康法益之犯罪'
        }
    ]
    return demos

def choose_topic(user_query):
    """
    選擇適當的台灣刑法分則犯罪類型，後續會用來選擇對應的 RAG database。
    
    Args:
        user_query (str): 使用者的刑法問題或案例描述
        
    Returns:
        str: 選擇的犯罪類型主題名稱
    """
    choose_topic_agent = dspy.ChainOfThought(ChooseTopic, demos=get_topic_demos())
    output = choose_topic_agent(user_query=user_query, rag_topic_metadata=topic_metadata)
    result = output.chosen_topic
    reasoning = output.reasoning if hasattr(output, 'reasoning') else "無法提供推理過程"
    
    return result, reasoning


if __name__ == "__main__":
    # 測試選擇主題功能
    # test_query = "某人故意殺害他人，應該如何論處？"
    # test_query = "某人故意殺害三個月的胚胎，應該如何論處？"
    test_queries = [
        "某人故意殺害他人，應該如何論處？",
        "某人故意殺害三個月的胚胎，應該如何論處？",
        "某人甩別人一巴掌，造成對方臉部受傷，應該如何論處？",
        "甲男偷摸乙女的屁股",
        "把辦公室的衛生紙拿回家使用",
    ]

    result = {}
    # print the result in json format
    for test_query in test_queries:
        chosen_topic = choose_topic(test_query)
        result[test_query] = chosen_topic
    
    print(result)
        
