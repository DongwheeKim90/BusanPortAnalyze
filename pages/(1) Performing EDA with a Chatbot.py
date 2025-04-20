import streamlit as st  # Import the Streamlit library (Streamlit 라이브러리 임포트)
import pandas as pd  # Import the pandas library for data handling (데이터 처리를 위한 pandas 라이브러리 임포트)
from setting_llm import importMyBot

# Set Streamlit page layout to wide (Streamlit 페이지 레이아웃을 와이드로 설정)
st.set_page_config(layout="wide")

# Subheader for the page title (페이지 제목을 서브헤더로 표시)
st.subheader("ChatBot for EDA and Analytics 🤖")

# Radio button for selecting dataset (데이터 선택용 라디오 버튼 구성)
selectData = st.radio(
    "Select the data you want ChatBot to analyze with EDA.",  # 라디오 버튼 안내 문구
    [
        ":rainbow[Time series data on foreign vessel arrivals at ports across South Korea]",
        ":rainbow[Time series data on the number of vessel arrivals and cargo throughput at the three major ports in Busan]",
        ":rainbow[Location and address data of the three major ports in Busan]",
        ":rainbow[Monthly and yearly data on the number of ship supplies sales and sales amount]",
        ":rainbow[Meat company data related to shipping supplies]",
        ":rainbow[Food company data related to shipping supplies]",
        ":rainbow[Vacant data around Busan's three major ports]",
        ":rainbow[Time series data on vessel dwell time by shipping company at Busan New Port]",
    ]
)

# Case 1
if selectData == ":rainbow[Time series data on foreign vessel arrivals at ports across South Korea]":
    st.markdown(
        """
        <div style="background-color:#cce5ff; padding:10px; border-radius:5px;">
            <span style="color:#ff8c00; font-weight:bold;">
                📌 Currently selected data:
                Time series data on shipping companies/cargo volumes by port in South Korea
            </span>
        </div>
        """, unsafe_allow_html=True
    )

    dataArea, chatBotArea = st.columns(2)

    with dataArea:
        with st.container(height=450):
            readData = pd.read_csv("./useData/forLLM_data/raw_koreaAllHarbors.csv", encoding="utf-8-sig")
            st.dataframe(readData, use_container_width=True, hide_index=True)

    with chatBotArea:
        # Main container for the chatbot interface (채팅 UI를 담는 메인 컨테이너)
        with st.container(height=450):

            # Initialize message history in session state if not already present
            # (세션 상태에 메시지 기록이 없다면 초기화)
            if "messages" not in st.session_state:
                st.session_state.messages = []

            # If there are no previous messages, show a welcome image
            # (대화 내역이 없는 경우, 첫 화면에 환영 이미지를 표시)
            if len(st.session_state.messages) == 0:
                with st.container(height=350):
                    st.image("./useImage/gptReady.png")  # Welcome image (환영 이미지)

            else:
                # If there are messages, render them inside a container
                # (메시지가 있다면, 이전 대화 내역을 채팅 형식으로 렌더링)
                with st.container(height=350):
                    for message in st.session_state.messages:
                        if message.get("type") == "image":
                            # If the message is of type 'image', render it in chat bubble
                            # (메시지 타입이 이미지이면, 채팅 말풍선 안에 이미지 표시)
                            with st.chat_message(message["role"]):
                                st.image(
                                    message["content"],
                                    caption="Generated Visualization",  # Caption under the image (이미지 하단 캡션)
                                    use_container_width=True  # Fit image to container width (컨테이너 너비에 맞춤)
                                )
                        else:
                            # Otherwise, render text content in chat bubble
                            # (텍스트 메시지는 일반 채팅 말풍선으로 표시)
                            with st.chat_message(message["role"]):
                                st.markdown(message["content"])  # Render message text as markdown (마크다운 형태로 출력)

            # Chat input box at the bottom of the screen
            # (하단에 사용자 입력창 생성)
            userStart = st.chat_input("Ask questions you're curious about, but don't type illegal or violent words.")
            if userStart:
                # Append user's message to session state history
                # (사용자의 질문을 메시지 기록에 추가)
                st.session_state.messages.append({"role": "user", "content": userStart})

                # Run the custom chatbot logic and get the system's response
                # (사용자 입력을 바탕으로 봇 함수 실행 후 응답 수신)
                systemAnswer = importMyBot(readData, userStart)

                # If there's a valid response, add it to the chat
                # (유효한 응답이 있을 경우, 채팅 기록에 추가)
                if systemAnswer:
                    st.session_state.messages.append({"role": "ai", "content": systemAnswer})

                # Force UI to rerun so the new messages render immediately
                # (UI를 새로고침하여 새로운 메시지를 즉시 반영)
                st.rerun()

# Case 2
elif selectData == ":rainbow[Time series data on the number of vessel arrivals and cargo throughput at the three major ports in Busan]":
    st.markdown(
        """
        <div style="background-color:#cce5ff; padding:10px; border-radius:5px;">
            <span style="color:#ff8c00; font-weight:bold;">
                📌 Currently selected data:
                Time series data on shipping companies and cargo volumes entering the three major ports of Busan, South Korea
            </span>
        </div>
        """, unsafe_allow_html=True
    )

    dataArea, chatBotArea = st.columns(2)

    with dataArea:
        with st.container(height=450):
            readData = pd.read_csv("./useData/forLLM_data/busanAllPorts_GTCount.csv", encoding="utf-8-sig")
            st.dataframe(readData, use_container_width=True, hide_index=True)

    with chatBotArea:
        # Main container for the chatbot interface (채팅 UI를 담는 메인 컨테이너)
        with st.container(height=450):

            # Initialize message history in session state if not already present
            # (세션 상태에 메시지 기록이 없다면 초기화)
            if "messages" not in st.session_state:
                st.session_state.messages = []

            # If there are no previous messages, show a welcome image
            # (대화 내역이 없는 경우, 첫 화면에 환영 이미지를 표시)
            if len(st.session_state.messages) == 0:
                with st.container(height=350):
                    st.image("./useImage/gptReady.png")  # Welcome image (환영 이미지)

            else:
                # If there are messages, render them inside a container
                # (메시지가 있다면, 이전 대화 내역을 채팅 형식으로 렌더링)
                with st.container(height=350):
                    for message in st.session_state.messages:
                        if message.get("type") == "image":
                            # If the message is of type 'image', render it in chat bubble
                            # (메시지 타입이 이미지이면, 채팅 말풍선 안에 이미지 표시)
                            with st.chat_message(message["role"]):
                                st.image(
                                    message["content"],
                                    caption="Generated Visualization",  # Caption under the image (이미지 하단 캡션)
                                    use_container_width=True  # Fit image to container width (컨테이너 너비에 맞춤)
                                )
                        else:
                            # Otherwise, render text content in chat bubble
                            # (텍스트 메시지는 일반 채팅 말풍선으로 표시)
                            with st.chat_message(message["role"]):
                                st.markdown(message["content"])  # Render message text as markdown (마크다운 형태로 출력)

            # Chat input box at the bottom of the screen
            # (하단에 사용자 입력창 생성)
            userStart = st.chat_input("Ask questions you're curious about, but don't type illegal or violent words.")
            if userStart:
                # Append user's message to session state history
                # (사용자의 질문을 메시지 기록에 추가)
                st.session_state.messages.append({"role": "user", "content": userStart})

                # Run the custom chatbot logic and get the system's response
                # (사용자 입력을 바탕으로 봇 함수 실행 후 응답 수신)
                systemAnswer = importMyBot(readData, userStart)

                # If there's a valid response, add it to the chat
                # (유효한 응답이 있을 경우, 채팅 기록에 추가)
                if systemAnswer:
                    st.session_state.messages.append({"role": "ai", "content": systemAnswer})

                # Force UI to rerun so the new messages render immediately
                # (UI를 새로고침하여 새로운 메시지를 즉시 반영)
                st.rerun()

# Case 3
elif selectData == ":rainbow[Location and address data of the three major ports in Busan]":
    st.markdown(
        """
        <div style="background-color:#cce5ff; padding:10px; border-radius:5px;">
            <span style="color:#ff8c00; font-weight:bold;">
                📌 Currently selected data:
                Annual sales amount and number of sales data for pre-sale items
            </span>
        </div>
        """, unsafe_allow_html=True
    )

    dataArea, chatBotArea = st.columns(2)

    with dataArea:
        with st.container(height=450):
            readData = pd.read_csv("./useData/forLLM_data/busanThreeport_position.csv", encoding="utf-8-sig")
            st.dataframe(readData, use_container_width=True, hide_index=True)

    with chatBotArea:
        # Main container for the chatbot interface (채팅 UI를 담는 메인 컨테이너)
        with st.container(height=450):

            # Initialize message history in session state if not already present
            # (세션 상태에 메시지 기록이 없다면 초기화)
            if "messages" not in st.session_state:
                st.session_state.messages = []

            # If there are no previous messages, show a welcome image
            # (대화 내역이 없는 경우, 첫 화면에 환영 이미지를 표시)
            if len(st.session_state.messages) == 0:
                with st.container(height=350):
                    st.image("./useImage/gptReady.png")  # Welcome image (환영 이미지)

            else:
                # If there are messages, render them inside a container
                # (메시지가 있다면, 이전 대화 내역을 채팅 형식으로 렌더링)
                with st.container(height=350):
                    for message in st.session_state.messages:
                        if message.get("type") == "image":
                            # If the message is of type 'image', render it in chat bubble
                            # (메시지 타입이 이미지이면, 채팅 말풍선 안에 이미지 표시)
                            with st.chat_message(message["role"]):
                                st.image(
                                    message["content"],
                                    caption="Generated Visualization",  # Caption under the image (이미지 하단 캡션)
                                    use_container_width=True  # Fit image to container width (컨테이너 너비에 맞춤)
                                )
                        else:
                            # Otherwise, render text content in chat bubble
                            # (텍스트 메시지는 일반 채팅 말풍선으로 표시)
                            with st.chat_message(message["role"]):
                                st.markdown(message["content"])  # Render message text as markdown (마크다운 형태로 출력)

            # Chat input box at the bottom of the screen
            # (하단에 사용자 입력창 생성)
            userStart = st.chat_input("Ask questions you're curious about, but don't type illegal or violent words.")
            if userStart:
                # Append user's message to session state history
                # (사용자의 질문을 메시지 기록에 추가)
                st.session_state.messages.append({"role": "user", "content": userStart})

                # Run the custom chatbot logic and get the system's response
                # (사용자 입력을 바탕으로 봇 함수 실행 후 응답 수신)
                systemAnswer = importMyBot(readData, userStart)

                # If there's a valid response, add it to the chat
                # (유효한 응답이 있을 경우, 채팅 기록에 추가)
                if systemAnswer:
                    st.session_state.messages.append({"role": "ai", "content": systemAnswer})

                # Force UI to rerun so the new messages render immediately
                # (UI를 새로고침하여 새로운 메시지를 즉시 반영)
                st.rerun()

# Case 4
elif selectData == ":rainbow[Monthly and yearly data on the number of ship supplies sales and sales amount]":
    st.markdown(
        """
        <div style="background-color:#cce5ff; padding:10px; border-radius:5px;">
            <span style="color:#ff8c00; font-weight:bold;">
                📌 Currently selected data:
                Meat company data related to shipping supplies
            </span>
        </div>
        """, unsafe_allow_html=True
    )

    dataArea, chatBotArea = st.columns(2)

    with dataArea:
        with st.container(height=450):
            readData = pd.read_csv("./useData/forLLM_data/finish_prod_totalCountPrice_yearMonth.csv", encoding="utf-8-sig")
            st.dataframe(readData, use_container_width=True, hide_index=True)

    with chatBotArea:
        # Main container for the chatbot interface (채팅 UI를 담는 메인 컨테이너)
        with st.container(height=450):

            # Initialize message history in session state if not already present
            # (세션 상태에 메시지 기록이 없다면 초기화)
            if "messages" not in st.session_state:
                st.session_state.messages = []

            # If there are no previous messages, show a welcome image
            # (대화 내역이 없는 경우, 첫 화면에 환영 이미지를 표시)
            if len(st.session_state.messages) == 0:
                with st.container(height=350):
                    st.image("./useImage/gptReady.png")  # Welcome image (환영 이미지)

            else:
                # If there are messages, render them inside a container
                # (메시지가 있다면, 이전 대화 내역을 채팅 형식으로 렌더링)
                with st.container(height=350):
                    for message in st.session_state.messages:
                        if message.get("type") == "image":
                            # If the message is of type 'image', render it in chat bubble
                            # (메시지 타입이 이미지이면, 채팅 말풍선 안에 이미지 표시)
                            with st.chat_message(message["role"]):
                                st.image(
                                    message["content"],
                                    caption="Generated Visualization",  # Caption under the image (이미지 하단 캡션)
                                    use_container_width=True  # Fit image to container width (컨테이너 너비에 맞춤)
                                )
                        else:
                            # Otherwise, render text content in chat bubble
                            # (텍스트 메시지는 일반 채팅 말풍선으로 표시)
                            with st.chat_message(message["role"]):
                                st.markdown(message["content"])  # Render message text as markdown (마크다운 형태로 출력)

            # Chat input box at the bottom of the screen
            # (하단에 사용자 입력창 생성)
            userStart = st.chat_input("Ask questions you're curious about, but don't type illegal or violent words.")
            if userStart:
                # Append user's message to session state history
                # (사용자의 질문을 메시지 기록에 추가)
                st.session_state.messages.append({"role": "user", "content": userStart})

                # Run the custom chatbot logic and get the system's response
                # (사용자 입력을 바탕으로 봇 함수 실행 후 응답 수신)
                systemAnswer = importMyBot(readData, userStart)

                # If there's a valid response, add it to the chat
                # (유효한 응답이 있을 경우, 채팅 기록에 추가)
                if systemAnswer:
                    st.session_state.messages.append({"role": "ai", "content": systemAnswer})

                # Force UI to rerun so the new messages render immediately
                # (UI를 새로고침하여 새로운 메시지를 즉시 반영)
                st.rerun()

# Case 5
elif selectData == ":rainbow[Meat company data related to shipping supplies]":
    st.markdown(
        """
        <div style="background-color:#cce5ff; padding:10px; border-radius:5px;">
            <span style="color:#ff8c00; font-weight:bold;">
                📌 Currently selected data:
                Food company data related to shipping supplies
            </span>
        </div>
        """, unsafe_allow_html=True
    )

    dataArea, chatBotArea = st.columns(2)

    with dataArea:
        with st.container(height=450):
            readData = pd.read_csv("./useData/forLLM_data/meat_company_LaLo.csv", encoding="utf-8-sig")
            st.dataframe(readData, use_container_width=True, hide_index=True)

    with chatBotArea:
        # Main container for the chatbot interface (채팅 UI를 담는 메인 컨테이너)
        with st.container(height=450):

            # Initialize message history in session state if not already present
            # (세션 상태에 메시지 기록이 없다면 초기화)
            if "messages" not in st.session_state:
                st.session_state.messages = []

            # If there are no previous messages, show a welcome image
            # (대화 내역이 없는 경우, 첫 화면에 환영 이미지를 표시)
            if len(st.session_state.messages) == 0:
                with st.container(height=350):
                    st.image("./useImage/gptReady.png")  # Welcome image (환영 이미지)

            else:
                # If there are messages, render them inside a container
                # (메시지가 있다면, 이전 대화 내역을 채팅 형식으로 렌더링)
                with st.container(height=350):
                    for message in st.session_state.messages:
                        if message.get("type") == "image":
                            # If the message is of type 'image', render it in chat bubble
                            # (메시지 타입이 이미지이면, 채팅 말풍선 안에 이미지 표시)
                            with st.chat_message(message["role"]):
                                st.image(
                                    message["content"],
                                    caption="Generated Visualization",  # Caption under the image (이미지 하단 캡션)
                                    use_container_width=True  # Fit image to container width (컨테이너 너비에 맞춤)
                                )
                        else:
                            # Otherwise, render text content in chat bubble
                            # (텍스트 메시지는 일반 채팅 말풍선으로 표시)
                            with st.chat_message(message["role"]):
                                st.markdown(message["content"])  # Render message text as markdown (마크다운 형태로 출력)

            # Chat input box at the bottom of the screen
            # (하단에 사용자 입력창 생성)
            userStart = st.chat_input("Ask questions you're curious about, but don't type illegal or violent words.")
            if userStart:
                # Append user's message to session state history
                # (사용자의 질문을 메시지 기록에 추가)
                st.session_state.messages.append({"role": "user", "content": userStart})

                # Run the custom chatbot logic and get the system's response
                # (사용자 입력을 바탕으로 봇 함수 실행 후 응답 수신)
                systemAnswer = importMyBot(readData, userStart)

                # If there's a valid response, add it to the chat
                # (유효한 응답이 있을 경우, 채팅 기록에 추가)
                if systemAnswer:
                    st.session_state.messages.append({"role": "ai", "content": systemAnswer})

                # Force UI to rerun so the new messages render immediately
                # (UI를 새로고침하여 새로운 메시지를 즉시 반영)
                st.rerun()

# Case 6
elif selectData == ":rainbow[Food company data related to shipping supplies]":
    st.markdown(
        """
        <div style="background-color:#cce5ff; padding:10px; border-radius:5px;">
            <span style="color:#ff8c00; font-weight:bold;">
                📌 Currently selected data:
                Vacant data around Busan's three major ports
            </span>
        </div>
        """, unsafe_allow_html=True
    )

    dataArea, chatBotArea = st.columns(2)

    with dataArea:
        with st.container(height=450):
            readData = pd.read_csv("./useData/forLLM_data/food_company_LaLo.csv", encoding="utf-8-sig")
            st.dataframe(readData, use_container_width=True, hide_index=True)

    with chatBotArea:
        # Main container for the chatbot interface (채팅 UI를 담는 메인 컨테이너)
        with st.container(height=450):

            # Initialize message history in session state if not already present
            # (세션 상태에 메시지 기록이 없다면 초기화)
            if "messages" not in st.session_state:
                st.session_state.messages = []

            # If there are no previous messages, show a welcome image
            # (대화 내역이 없는 경우, 첫 화면에 환영 이미지를 표시)
            if len(st.session_state.messages) == 0:
                with st.container(height=350):
                    st.image("./useImage/gptReady.png")  # Welcome image (환영 이미지)

            else:
                # If there are messages, render them inside a container
                # (메시지가 있다면, 이전 대화 내역을 채팅 형식으로 렌더링)
                with st.container(height=350):
                    for message in st.session_state.messages:
                        if message.get("type") == "image":
                            # If the message is of type 'image', render it in chat bubble
                            # (메시지 타입이 이미지이면, 채팅 말풍선 안에 이미지 표시)
                            with st.chat_message(message["role"]):
                                st.image(
                                    message["content"],
                                    caption="Generated Visualization",  # Caption under the image (이미지 하단 캡션)
                                    use_container_width=True  # Fit image to container width (컨테이너 너비에 맞춤)
                                )
                        else:
                            # Otherwise, render text content in chat bubble
                            # (텍스트 메시지는 일반 채팅 말풍선으로 표시)
                            with st.chat_message(message["role"]):
                                st.markdown(message["content"])  # Render message text as markdown (마크다운 형태로 출력)

            # Chat input box at the bottom of the screen
            # (하단에 사용자 입력창 생성)
            userStart = st.chat_input("Ask questions you're curious about, but don't type illegal or violent words.")
            if userStart:
                # Append user's message to session state history
                # (사용자의 질문을 메시지 기록에 추가)
                st.session_state.messages.append({"role": "user", "content": userStart})

                # Run the custom chatbot logic and get the system's response
                # (사용자 입력을 바탕으로 봇 함수 실행 후 응답 수신)
                systemAnswer = importMyBot(readData, userStart)

                # If there's a valid response, add it to the chat
                # (유효한 응답이 있을 경우, 채팅 기록에 추가)
                if systemAnswer:
                    st.session_state.messages.append({"role": "ai", "content": systemAnswer})

                # Force UI to rerun so the new messages render immediately
                # (UI를 새로고침하여 새로운 메시지를 즉시 반영)
                st.rerun()

# Case 7
elif selectData == ":rainbow[Vacant data around Busan's three major ports]":
    st.markdown(
        """
        <div style="background-color:#cce5ff; padding:10px; border-radius:5px;">
            <span style="color:#ff8c00; font-weight:bold;">
                📌 Currently selected data:
                Vacant data around Busan's three major ports
            </span>
        </div>
        """, unsafe_allow_html=True
    )

    dataArea, chatBotArea = st.columns(2)

    with dataArea:
        with st.container(height=450):
            readData = pd.read_csv("./useData/forLLM_data/vacancy_locationLaLo.csv", encoding="utf-8-sig")
            st.dataframe(readData, use_container_width=True, hide_index=True)

    with chatBotArea:
        # Main container for the chatbot interface (채팅 UI를 담는 메인 컨테이너)
        with st.container(height=450):

            # Initialize message history in session state if not already present
            # (세션 상태에 메시지 기록이 없다면 초기화)
            if "messages" not in st.session_state:
                st.session_state.messages = []

            # If there are no previous messages, show a welcome image
            # (대화 내역이 없는 경우, 첫 화면에 환영 이미지를 표시)
            if len(st.session_state.messages) == 0:
                with st.container(height=350):
                    st.image("./useImage/gptReady.png")  # Welcome image (환영 이미지)

            else:
                # If there are messages, render them inside a container
                # (메시지가 있다면, 이전 대화 내역을 채팅 형식으로 렌더링)
                with st.container(height=350):
                    for message in st.session_state.messages:
                        if message.get("type") == "image":
                            # If the message is of type 'image', render it in chat bubble
                            # (메시지 타입이 이미지이면, 채팅 말풍선 안에 이미지 표시)
                            with st.chat_message(message["role"]):
                                st.image(
                                    message["content"],
                                    caption="Generated Visualization",  # Caption under the image (이미지 하단 캡션)
                                    use_container_width=True  # Fit image to container width (컨테이너 너비에 맞춤)
                                )
                        else:
                            # Otherwise, render text content in chat bubble
                            # (텍스트 메시지는 일반 채팅 말풍선으로 표시)
                            with st.chat_message(message["role"]):
                                st.markdown(message["content"])  # Render message text as markdown (마크다운 형태로 출력)

            # Chat input box at the bottom of the screen
            # (하단에 사용자 입력창 생성)
            userStart = st.chat_input("Ask questions you're curious about, but don't type illegal or violent words.")
            if userStart:
                # Append user's message to session state history
                # (사용자의 질문을 메시지 기록에 추가)
                st.session_state.messages.append({"role": "user", "content": userStart})

                # Run the custom chatbot logic and get the system's response
                # (사용자 입력을 바탕으로 봇 함수 실행 후 응답 수신)
                systemAnswer = importMyBot(readData, userStart)

                # If there's a valid response, add it to the chat
                # (유효한 응답이 있을 경우, 채팅 기록에 추가)
                if systemAnswer:
                    st.session_state.messages.append({"role": "ai", "content": systemAnswer})

                # Force UI to rerun so the new messages render immediately
                # (UI를 새로고침하여 새로운 메시지를 즉시 반영)
                st.rerun()
# Case 8
elif selectData == ":rainbow[Time series data on vessel dwell time by shipping company at Busan SinHang Port]":
    st.markdown(
        """
        <div style="background-color:#cce5ff; padding:10px; border-radius:5px;">
            <span style="color:#ff8c00; font-weight:bold;">
                📌 Currently selected data:
                Vacant data around Busan's three major ports
            </span>
        </div>
        """, unsafe_allow_html=True
    )

    dataArea, chatBotArea = st.columns(2)

    with dataArea:
        with st.container(height=450):
            readData = pd.read_csv("./useData/forLLM_data/SinhangSchedule_rawData.csv", encoding="utf-8-sig")
            st.dataframe(readData, use_container_width=True, hide_index=True)

    with chatBotArea:
        # Main container for the chatbot interface (채팅 UI를 담는 메인 컨테이너)
        with st.container(height=450):

            # Initialize message history in session state if not already present
            # (세션 상태에 메시지 기록이 없다면 초기화)
            if "messages" not in st.session_state:
                st.session_state.messages = []

            # If there are no previous messages, show a welcome image
            # (대화 내역이 없는 경우, 첫 화면에 환영 이미지를 표시)
            if len(st.session_state.messages) == 0:
                with st.container(height=350):
                    st.image("./useImage/gptReady.png")  # Welcome image (환영 이미지)

            else:
                # If there are messages, render them inside a container
                # (메시지가 있다면, 이전 대화 내역을 채팅 형식으로 렌더링)
                with st.container(height=350):
                    for message in st.session_state.messages:
                        if message.get("type") == "image":
                            # If the message is of type 'image', render it in chat bubble
                            # (메시지 타입이 이미지이면, 채팅 말풍선 안에 이미지 표시)
                            with st.chat_message(message["role"]):
                                st.image(
                                    message["content"],
                                    caption="Generated Visualization",  # Caption under the image (이미지 하단 캡션)
                                    use_container_width=True  # Fit image to container width (컨테이너 너비에 맞춤)
                                )
                        else:
                            # Otherwise, render text content in chat bubble
                            # (텍스트 메시지는 일반 채팅 말풍선으로 표시)
                            with st.chat_message(message["role"]):
                                st.markdown(message["content"])  # Render message text as markdown (마크다운 형태로 출력)

            # Chat input box at the bottom of the screen
            # (하단에 사용자 입력창 생성)
            userStart = st.chat_input("Ask questions you're curious about, but don't type illegal or violent words.")
            if userStart:
                # Append user's message to session state history
                # (사용자의 질문을 메시지 기록에 추가)
                st.session_state.messages.append({"role": "user", "content": userStart})

                # Run the custom chatbot logic and get the system's response
                # (사용자 입력을 바탕으로 봇 함수 실행 후 응답 수신)
                systemAnswer = importMyBot(readData, userStart)

                # If there's a valid response, add it to the chat
                # (유효한 응답이 있을 경우, 채팅 기록에 추가)
                if systemAnswer:
                    st.session_state.messages.append({"role": "ai", "content": systemAnswer})

                # Force UI to rerun so the new messages render immediately
                # (UI를 새로고침하여 새로운 메시지를 즉시 반영)
                st.rerun()
