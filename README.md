1. Project Summary
This project is a data-driven marketing strategy analysis for revitalizing Busan Port, conducted from the perspective of the Busan Port Authority. It aims to propose and validate actionable services for foreign shipping companies using real-world port data and correlation analysis.

2. Purpose
2.1. Identify practical services to boost port utilization
(e.g., online ship supplies store, tourism service based on dwell time)
2.2. Support strategic planning with exploratory data analysis and visualization
2.3. Enable data-informed decisions by port authorities and stakeholders

3. Main Features
3.1. Time-Series Analysis
Analyze annual trends in Gross Tonnage (GT) and Cargo Throughput (CT)

Identify correlation between CT, GT, and vessel dwell time

3.2. Service Recommendation Logic
Recommend tourism courses based on dwell time quartiles (short, medium, long stay)

Estimate number of foreign crew members to support demand forecasting

3.3. Online Ship Supply Market Insights
Analyze historical product sales and trends

Conduct word cloud analysis using blog/SNS data

Visualize local vendor and warehouse vacancy data around Busan ports

3.4. EDA Support Chatbot
Built with OpenAI + LangChain

Handles general conversation via LCEL

Uses create_pandas_dataframe_agent for answering data-specific queries

Provides basic metadata overview and visualizations of uploaded datasets

4. Key Libraries & Tools
4.1. pandas, numpy – Data processing
4.2. matplotlib, plotly – Visualization
4.3. OpenAI, LangChain – EDA chatbot
4.4. Streamlit – Web-based dashboard
4.5. NLTK, wordcloud – Text analysis
4.6. Selenium, BeautifulSoup – (Optional, for external data scraping)
