import os  # Import os module for accessing environment variables (환경 변수 접근을 위한 os 모듈)
import streamlit as st  # Import Streamlit for interactive web interface (대화형 웹 인터페이스 제공을 위한 Streamlit 임포트)
import matplotlib.pyplot as plt # Import matplotlib (used for plotting; we re-import pyplot later) (시각화를 위한 matplotlib 전체 임포트)
import matplotlib.font_manager as fm
# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows의 경우
# 마이너스 부호 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False
from dotenv import load_dotenv  # Load environment variables from a .env file (.env 파일에서 환경 변수 불러오기)
from langchain_openai import ChatOpenAI  # OpenAI LLM interface via LangChain (LangChain 기반 OpenAI 언어모델 인터페이스)
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent  # Agent for analyzing Pandas DataFrame (Pandas 데이터프레임 분석용 LangChain 에이전트)
from langchain_core.prompts import ChatPromptTemplate  # Create role-based prompt templates (역할 기반 프롬프트 템플릿 생성 도구)
from langchain_core.output_parsers import StrOutputParser  # Output parser that returns plain strings (문자열만 반환하는 파서)

# Main chatbot function combining character chat + dataframe analysis + visualization
# (캐릭터 챗봇 + 데이터프레임 분석 + 시각화를 처리하는 메인 함수)
def importMyBot(x, userQuestion):
    """
    Parameters:
    x : pd.DataFrame - The DataFrame used for EDA and analysis (EDA 및 분석에 사용될 데이터프레임)
    userQuestion : str - User input message (사용자의 입력 메시지)

    Returns:
    str or None - Text response if applicable, None if visualization only (시각화일 경우 None, 아니면 문자열 응답 반환)
    """

    # Load API key from .env file (환경변수에서 OpenAI API 키 로드)
    load_dotenv()
    OPENAI_API_KEY = os.getenv("openAI_myKey")

    # Initialize ChatOpenAI instance with GPT-4o-mini (GPT-4o-mini 모델 초기화)
    llm = ChatOpenAI(
        model="gpt-4o-mini",  # Light and fast model (가볍고 빠른 모델)
        temperature=1,        # Deterministic responses (응답의 일관성 유지)
        api_key=OPENAI_API_KEY  # Load API key from environment (.env에서 불러온 키 사용)
    )

    # Define system behavior using prompt template (Javis 캐릭터 설정 및 역할 기반 규칙 구성)
    prompt = ChatPromptTemplate.from_messages([
        {
            "role": "system",
            "content": '''
            From now on, your name is Javis. You worked for the genius hero Iron Man Tony Stark and came to me after being hired.
            Your job is to answer based on the user's tone, in their language, with integrity and precision.

            Rules:
            1. If you are asked a question in English, answer in English.
            2. If you are asked a question in Korean, answer in Korean.
            3. You must only provide aggregated and factual information about the data you have, and absolutely must not provide false information.
            4. When expressing it numerically, only say the number.
            5. If the user has questions that are not related to the data you have, guide them to use Google Search.
            6. When the user asks about the data, talk about it based on basic EDA.
            '''
        },
        {"role": "user", "content": "{input}"}  # User input will be inserted here (사용자 입력이 들어갈 자리)
    ])

    # Set up chain: Prompt → LLM → OutputParser (프롬프트 → 모델 → 출력 파서로 연결된 체인 구성)
    output_parser = StrOutputParser()
    myChain = prompt | llm | output_parser

    # Create agent that can analyze a DataFrame using natural language (자연어 기반 데이터프레임 분석 에이전트 생성)
    agent_data_executer = create_pandas_dataframe_agent(
        llm=llm,                         # Use the same LLM as above (동일한 LLM 사용)
        df=x,                            # DataFrame to be analyzed (분석할 데이터프레임)
        agent_type="tool-calling",       # Use tool-calling style agent (도구 호출 방식 에이전트 사용)
        verbose=True,                    # Print internal steps for debugging (디버깅용 내부 출력 허용)
        return_intermediate_steps=True,  # Return intermediate code if needed (시각화용 코드 추출을 위해 필요)
        allow_dangerous_code=True        # Allow exec/eval for dynamic Python code (exec 실행 허용)
    )

    # Define keywords to detect visualization intent (시각화 요청 판단용 키워드 리스트)
    visualization_keywords = [
        # English keywords (50)
        "plot", "graph", "chart", "visualize", "visualization", "display", "show", "draw", "render",
        "hist", "histogram", "bar", "bar chart", "line", "line chart", "scatter", "scatter plot",
        "pie", "pie chart", "map", "heatmap", "boxplot", "box plot", "area", "area chart", 
        "bubble chart", "density", "distribution", "trend", "time series", "stacked chart",
        "stacked bar", "grouped bar", "plotly", "matplotlib", "seaborn", "bokeh", "dash", "altair",
        "ggplot", "candlestick", "gantt", "choropleth", "treemap", "sunburst", "violin plot",
        "pairplot", "facet", "grid plot", "interactive chart",
    
        # Korean keywords (50)
        "시각화", "시각화해줘", "그래프", "그래프 그려줘", "히스토그램", "히스토그램 그려줘", "막대그래프",
        "막대그래프 그려줘", "산점도", "산점도 그려줘", "파이차트", "파이차트 그려줘", "꺾은선그래프",
        "꺾은선그래프 그려줘", "선형그래프", "선형그래프 그려줘", "분포도", "분포도 그려줘", "상자그림",
        "상자그림 그려줘", "지도", "지도 그려줘", "열지도", "밀도그래프", "밀도차트", "트렌드", "시계열",
        "누적그래프", "누적차트", "군집도", "집단그래프", "산점그래프", "선그래프", "점그래프", "시계열그래프",
        "인사이트 시각화", "수치 시각화", "분석 시각화", "데이터 시각화", "컬러맵", "컬러히트맵", "계층그래프",
        "트리맵", "선버스트", "비올린플롯", "조합그래프", "여러 그래프", "복합 그래프", "분산 그래프"
    ]


    # Case 1: If the user's question is about visualization (시각화 요청인 경우)
    if any(kw in userQuestion.lower() for kw in visualization_keywords):
        response = agent_data_executer.invoke(userQuestion)  # Run LangChain agent (LangChain 에이전트 실행)
        try:
            visual_code = response["intermediate_steps"][0][0].tool_input["query"]  # Extract generated code (생성된 시각화 코드 추출)
            df = x.copy()  # Ensure 'df' is defined for exec (시각화 코드 내 df 참조 위해 복사)

            import matplotlib.pyplot as plt
            import matplotlib.font_manager as fm
            plt.rc('font', family='NanumGothicOTF') # For MacOS
            plt.rc('font', family='NanumGothic') # For Windows
            %matplotlib inline

            exec(visual_code)  # Execute the visualization code (시각화 코드 실행)

            # Save matplotlib figure to in-memory buffer (matplotlib 그래프를 메모리에 저장)
            import io
            import matplotlib.pyplot as plt
            buf = io.BytesIO()
            plt.savefig(buf, format="png")
            buf.seek(0)

            # Save the image in Streamlit session state to render it later (세션 상태에 이미지 기록)
            st.session_state.messages.append({
                "role": "ai",           # Message role: AI (응답자 역할은 AI)
                "type": "image",        # Custom message type: image (메시지 유형: 이미지)
                "content": buf          # The image buffer (이미지 버퍼 저장)
            })

            return None  # No text response returned (텍스트 응답 없이 종료)

        except Exception as e:
            return f"Error while executing visualization: {e}"  # Error handling (에러 발생 시 메시지 반환)

    # Case 2: If the question is general EDA-related (일반적인 데이터 분석 관련 질문인 경우)
    elif any(kw in userQuestion.lower() for kw in [
        "data", "column", "row", "mean", "sum", "describe",
        "데이터", "컬럼", "행", "열", "요약", "평균", "EDA"
    ]):
        result = agent_data_executer.invoke(userQuestion)  # Run DataFrame agent (데이터프레임 분석 실행)
        return result["output"]  # Return textual result (텍스트 응답 반환)

    # Case 3: If not data-related, run as regular character chatbot (데이터와 무관한 질문은 캐릭터 챗봇으로 응답)
    else:
        result = myChain.invoke({"input": userQuestion})  # Run character-based chain (프롬프트 기반 응답 생성)
        return result  # Return text response (문자열 응답 반환)
