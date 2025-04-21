1. Project Overview
The Busan Port Marketing Data Analysis Project was planned based on a meeting with officials from the Busan Port Authority in 2020. The main goal was to establish a data-driven strategy for attracting foreign shipping companies to Busan Port. From the perspective of the Busan Port Authority, this project proposes practical online services—such as an online ship supplies store and a customized sightseeing guide based on vessel dwell time—and conducts relevant data analysis to support these ideas.

2. Main Objectives
2.1. Building an Online Ship Supplies Platform
Analyzed annual sales volume and revenue data to identify key product categories

Selected meat and food as the primary product categories based on consistent upward sales trends

Performed word cloud analysis using text data from SNS and blogs posted by foreign users

Visualized company and warehouse vacancy data to support distribution planning near Busan's ports

2.2. Providing Time-Based Tourism Information
Designed custom tourism course recommendations based on vessel dwell time

Grouped dwell times into short (24–42 hrs), medium (43–44 hrs), and long (45+ hrs) durations

Aimed to increase satisfaction and engagement of foreign shipping companies and crew members

3. Key Data Analysis
Time-series analysis showed that both GT (Gross Tonnage) and CT (Cargo Throughput) are steadily increasing, while the number of ship arrivals is declining

Correlation analysis results:

GT vs. CT: r = 0.5942, p = 0.0416

CT vs. Dwell Time: r = 0.5105, p = 0.0

Estimated 244,395 to 290,790 foreign crew members arrive at Busan Port annually, based on average crew size and number of foreign vessel arrivals

4. Additional Feature: EDA Chatbot
Implemented a chatbot to provide an overview of collected data before processing, including data types, structure, and basic visualizations

Built using OpenAI and LangChain

General conversation is handled using LCEL (LangChain Expression Language)

Data-related questions are answered using the create_pandas_dataframe_agent

Set a low temperature to minimize hallucinations in responses
