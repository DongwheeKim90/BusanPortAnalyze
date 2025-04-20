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
expander.image("ht
