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
                Time series data on foreign vessel arrivals at ports across South Korea
            </span>
        </div>
        """, unsafe_allow_html=True
    )

    dataArea, chatBotArea = st.columns(2)

    with dataArea:
        with st.container(height=450):
            readData = pd.read_csv("./useData/forLLM_data/koreaAllHarbors.csv", encoding="utf-8-sig")
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
                Time series data on the number of vessel arrivals and cargo throughput at the three major ports in Busan
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
                Location and address data of the three major ports in Busan
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
                Monthly and yearly data on the number of ship supplies sales and sales amount
            </span>
        </div>
        """, unsafe_allow_html=True
    )

    dataArea, chatBotArea = st.columns(2)

    with dataArea:
        with st.container(height=450):
            readData = pd.read_csv("./useData/forLLM_data/prod_totalCountPrice_yearMonth.csv", encoding="utf-8-sig")
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
                Meat company data related to shipping supplies
            </span>
        </div>
        """, unsafe_allow_html=True
    )

    dataArea, chatBotArea = st.columns(2)

    with dataArea:
        with st.container(height=450):
            readData = pd.read_csv("./useData/forLLM_data/company(Meat)_LaLo.csv", encoding="utf-8-sig")
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
                Food company data related to shipping supplies
            </span>
        </div>
        """, unsafe_allow_html=True
    )

    dataArea, chatBotArea = st.columns(2)

    with dataArea:
        with st.container(height=450):
            readData = pd.read_csv("./useData/forLLM_data/company(Food)_LaLo.csv", encoding="utf-8-sig")
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
            readData = pd.read_csv("./useData/forLLM_data/vacancy_location_LaLo.csv", encoding="utf-8-sig")
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
# elif selectData == ":rainbow[Time series data on vessel dwell time by shipping company at Busan SinHang Port]":
else:
    st.markdown(
        """
        <div style="background-color:#cce5ff; padding:10px; border-radius:5px;">
            <span style="color:#ff8c00; font-weight:bold;">
                📌 Currently selected data:
                Time series data on vessel dwell time by shipping company at Busan SinHang Port
            </span>
        </div>
        """, unsafe_allow_html=True
    )

    dataArea, chatBotArea = st.columns(2)

    with dataArea:
        with st.container(height=450):
            readData = pd.read_csv("./useData/forLLM_data/SinhangSchedule.csv", encoding="utf-8-sig")
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
                
expander = st.expander("Basic LLM Integration Code (using OpenAI API)")
expander.code('''
import os  # Import os module for accessing environment variables (환경 변수 접근을 위한 os 모듈)
import streamlit as st  # Import Streamlit for interactive web interface (대화형 웹 인터페이스 제공을 위한 Streamlit 임포트)
import matplotlib.pyplot as plt  # Import matplotlib (used for plotting) (시각화를 위한 matplotlib 임포트)
import matplotlib.font_manager as fm  # Font manager for matplotlib (matplotlib 폰트 매니저 임포트)
from dotenv import load_dotenv  # Load environment variables from a .env file (.env 파일에서 환경 변수 불러오기)
from langchain_openai import ChatOpenAI  # OpenAI LLM interface via LangChain (LangChain 기반 OpenAI 언어모델 인터페이스)
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent  # LangChain agent for DataFrame (Pandas 데이터프레임 분석용 LangChain 에이전트)
from langchain_core.prompts import ChatPromptTemplate  # Role-based prompt template generator (역할 기반 프롬프트 템플릿 생성)
from langchain_core.output_parsers import StrOutputParser  # Simple string output parser (단순 문자열 반환 파서)

# Set font for Korean display in matplotlib (matplotlib 한글 폰트 설정)
plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows 기준 말굿 고딕 적용
plt.rcParams['axes.unicode_minus'] = False  # Prevent broken minus sign (마이너스 부호 깨짐 방지)

# Main chatbot function that processes user questions, runs LLM + EDA + Visualization
# (LLM + 데이터프레임 분석 + 시각화를 통합한 메인 챗봇 함수)
def importMyBot(x, userQuestion):
    """
    Parameters:
    x : pd.DataFrame - DataFrame to analyze (분석할 데이터프레임)
    userQuestion : str - User question or command (사용자 질문 또는 명령)

    Returns:
    str or None - Textual response or None if image is returned (텍스트 응답 또는 이미지 반환시 None)
    """

    # Load API key from .env (환경 변수에서 OpenAI API 키 로드)
    load_dotenv()
    OPENAI_API_KEY = os.getenv("openAI_myKey")

    # Initialize LLM with gpt-4o-mini for cost-effective inference (gpt-4o-mini 모델 초기화)
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=1,
        api_key=OPENAI_API_KEY
    )

    # Create chatbot personality and behavior prompt (챗봇 캐릭터 설정 및 응답 규칙 정의)
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
        {"role": "user", "content": "{input}"}
    ])

    # Combine prompt → LLM → output parser into a chain (프롬프트 → 모델 → 파서 체인 구성)
    output_parser = StrOutputParser()
    myChain = prompt | llm | output_parser

    # Create a LangChain agent that can interact with the DataFrame using natural language
    # (자연어를 이용해 데이터프레임과 상호작용하는 LangChain 에이전트 구성)
    agent_data_executer = create_pandas_dataframe_agent(
        llm=llm,
        df=x,
        agent_type="tool-calling",
        verbose=True,
        return_intermediate_steps=True,
        allow_dangerous_code=True
    )

    # List of keywords to detect if the user is asking for visualization (시각화 요청 키워드 정의)
    visualization_keywords = [
        # English (영어)
        "plot", "graph", "chart", "visualize", "display", "show", "draw", "render",
        "hist", "bar", "line", "scatter", "pie", "map", "heatmap", "box", "area",
        "bubble", "density", "distribution", "trend", "time series", "stacked", "plotly",
        "matplotlib", "seaborn", "bokeh", "dash", "altair", "gantt", "treemap", "sunburst",

        # Korean (한글)
        "시각화", "그래프", "히스토그램", "막대그래프", "산점도", "파이차트", "선형그래프", "분포도", "상자그림",
        "지도", "열지도", "밀도차트", "트렌드", "시계열", "누적그래프", "군집도", "트리맵", "선버스트", "비올린플롯"
    ]

    # Case 1: Visualization requested (시각화 요청 시)
    if any(kw in userQuestion.lower() for kw in visualization_keywords):
        response = agent_data_executer.invoke(userQuestion)  # 에이전트 실행
        try:
            visual_code = response["intermediate_steps"][0][0].tool_input["query"]  # 생성된 코드 추출
            df = x.copy()  # 코드 내에서 사용될 df 정의

            exec(visual_code)  # 시각화 코드 실행

            # 시각화 결과를 이미지로 저장
            import io
            buf = io.BytesIO()
            plt.savefig(buf, format="png")
            buf.seek(0)

            # 이미지 버퍼를 세션에 저장하여 Streamlit에서 렌더링
            st.session_state.messages.append({
                "role": "ai",
                "type": "image",
                "content": buf
            })

            return None  # 시각화는 텍스트 응답 없이 종료

        except Exception as e:
            return f"Error while executing visualization: {e}"  # 에러 핸들링

    # Case 2: Data-related summary/EDA questions (EDA 질문일 경우)
    elif any(kw in userQuestion.lower() for kw in [
        "data", "column", "row", "mean", "sum", "describe", "데이터", "컬럼", "행", "열", "요약", "평균", "EDA"
    ]):
        result = agent_data_executer.invoke(userQuestion)  # 에이전트 실행
        return result["output"]  # 결과 텍스트 반환

    # Case 3: General character conversation (일반 캐릭터 응답)
    else:
        result = myChain.invoke({"input": userQuestion})  # 일반 챗봇 응답
        return result  # 텍스트 반환

import streamlit as st  # Import the Streamlit library (Streamlit 라이브러리 임포트)
import pandas as pd  # Import the pandas library for data handling (데이터 처리를 위한 pandas 라이브러리 임포트)
from setting_llm import importMyBot  # Import custom chatbot logic (사용자 정의 챗봇 로직 임포트)

# Set Streamlit page layout to wide format (Streamlit 페이지 레이아웃을 와이드 포맷으로 설정)
st.set_page_config(layout="wide")

# Display a subheader as the chatbot title (챗봇 제목을 서브헤더로 표시)
st.subheader("ChatBot for EDA and Analytics")

# Define dataset selection radio buttons (분석할 데이터셋을 선택하기 위한 라디오 버튼 정의)
selectData = st.radio(
    "Select the data you want ChatBot to analyze with EDA.",  # Instruction for dataset selection (데이터셋 선택을 위한 안내 문구)
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

# Dictionary mapping each selection to its corresponding CSV file (선택한 옵션에 따른 CSV 파일 매핑 딕셔너리)
data_sources = {
    ":rainbow[Time series data on foreign vessel arrivals at ports across South Korea]": "./useData/forLLM_data/koreaAllHarbors.csv",
    ":rainbow[Time series data on the number of vessel arrivals and cargo throughput at the three major ports in Busan]": "./useData/forLLM_data/busanAllPorts_GTCount.csv",
    ":rainbow[Location and address data of the three major ports in Busan]": "./useData/forLLM_data/busanThreeport_position.csv",
    ":rainbow[Monthly and yearly data on the number of ship supplies sales and sales amount]": "./useData/forLLM_data/prod_totalCountPrice_yearMonth.csv",
    ":rainbow[Meat company data related to shipping supplies]": "./useData/forLLM_data/company(Meat)_LaLo.csv",
    ":rainbow[Food company data related to shipping supplies]": "./useData/forLLM_data/company(Food)_LaLo.csv",
    ":rainbow[Vacant data around Busan's three major ports]": "./useData/forLLM_data/vacancy_location_LaLo.csv",
    ":rainbow[Time series data on vessel dwell time by shipping company at Busan New Port]": "./useData/forLLM_data/SinhangSchedule.csv",
}

# Display header indicating current selection (현재 선택된 데이터셋을 강조하는 헤더 표시)
st.markdown(
    f"""
    <div style='background-color:#cce5ff; padding:10px; border-radius:5px;'>
        <span style='color:#ff8c00; font-weight:bold;'>
            📌 Currently selected data: <br> {selectData.split(']')[1]}
        </span>
    </div>
    """, unsafe_allow_html=True
)

# Layout with two columns for data and chatbot (데이터와 챗봇 UI를 위한 2열 레이아웃 구성)
dataArea, chatBotArea = st.columns(2)

# Load and show selected data in the left column (선택한 데이터를 좌측 영역에 표시)
with dataArea:
    with st.container(height=450):  # Set a fixed height container (고정 높이 컨테이너 설정)
        readData = pd.read_csv(data_sources[selectData], encoding="utf-8-sig")
        st.dataframe(readData, use_container_width=True, hide_index=True)  # Show data table (데이터 테이블 표시)

# Chat interface area in the right column (우측에 챗봇 인터페이스 영역 구성)
with chatBotArea:
    with st.container(height=450):

        # Initialize message session state if not already created (세션 상태에 메시지 기록이 없다면 초기화)
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # If no previous chat, show welcome image (대화 이력이 없으면 환영 이미지 표시)
        if len(st.session_state.messages) == 0:
            with st.container(height=350):
                st.image("./useImage/gptReady.png")  # Welcome image (환영 이미지)
        else:
            with st.container(height=350):
                # Display past chat messages (이전 채팅 메시지 표시)
                for message in st.session_state.messages:
                    with st.chat_message(message["role"]):
                        if message.get("type") == "image":
                            st.image(
                                message["content"],
                                caption="Generated Visualization",  # Image caption (이미지 캡션)
                                use_container_width=True
                            )
                        else:
                            st.markdown(message["content"])  # Display text as markdown (마크다운 텍스트 표시)

        # Input field for user message (사용자 메시지 입력 필드)
        userStart = st.chat_input("Ask questions you're curious about, but don't type illegal or violent words.")

        if userStart:
            st.session_state.messages.append({"role": "user", "content": userStart})  # Save user message (사용자 메시지 저장)

            systemAnswer = importMyBot(readData, userStart)  # Get chatbot reply (챗봇 응답 받기)

            if systemAnswer:
                st.session_state.messages.append({"role": "ai", "content": systemAnswer})  # Save chatbot reply (챗봇 메시지 저장)

            st.rerun()  # Rerun UI to update messages (UI 재실행하여 메시지 갱신)

''')
