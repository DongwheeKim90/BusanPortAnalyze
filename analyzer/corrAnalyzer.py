import os
import pickle
import plotly.graph_objects as go
from scipy.stats import pearsonr

# 상관분석 및 plotly시각화 객체 생성 및 저장 클래스 생성
class CorrelationAnalyzer:
    def __init__(self, df, x_col, y_col, time_col=None,
                 x_color: str = 'red', y_color: str = 'blue', scatter_color: str = 'green'):
        self.df = df    # 사용할 데이터프레임
        self.x_col = x_col  # 산점도의 x축 및 첫 번째 시계열 그래프 데이터 컬럼
        self.y_col = y_col  # 산점도의 y축 및 두 번째 시계열 그래프 데이터 컬럼
        self.time_col = time_col    # 시계열 라인 그래프를 위한 시간축
        self.x_color: str = x_color # 첫 번째 시계열 그래프 라인 색상
        self.y_color: str = y_color # 첫 번째 시계열 그래프 라인 색상
        self.scatter_color: str = scatter_color # 상관분석용 산점도 색상

        # 파일 이름 설정
        # plotly객체에서 상호작용까지 온전히 저장하기 위해 pickle파일로 저장
        self.scatter_file = f'graph/{self.x_col}_{self.y_col}_Scatter.pkl'
        self.line_file = f'graph/{self.x_col}_{self.y_col}_Line.pkl'

        # 상관계수, p-value 계산 및 클래스 매개변수에 저장
        self.corr, self.p = pearsonr(self.df[self.x_col], self.df[self.y_col])

    # 상관분석 및 plotly 산점도 객체 생성 및 저장
    def analyze_and_plot(self):
        # 피클 파일이 존재하면 불러오기
        if os.path.exists(self.scatter_file):
            with open(self.scatter_file, 'rb') as f:
                return pickle.load(f), self.corr, self.p

        # 피클 파일이 없다면 산점도 새로 생성하기
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=self.df[self.x_col],
            y=self.df[self.y_col],
            mode='markers',
            marker=dict(size=10, color=self.scatter_color, opacity=.9),
            name='Data Points'
        ))

        # 산점도 제목, 축 라벨, 그래프 사이즈 설정
        fig.update_layout(
            title=(f'Correlation between {self.x_col} and {self.y_col} in Busan Port<br>'
                   f'corr: {self.corr:.4f}, p-value: {self.p:.4f}'),
            xaxis_title=f'{self.x_col} (scaled)',
            yaxis_title=f'{self.y_col} (scaled)',
            template='plotly_white',
            showlegend=False,
            width=700,
            height=700
        )

        # 피클로 저장
        with open(self.scatter_file, 'wb') as f:
            pickle.dump(fig, f)

        # plotly 객체, 상관계수, p-value return
        return fig, self.corr, self.p

    # plotly 시계열 라인 그래프 생성 및 저장
    # 그래프 제목 타입 지정
    def plot_time_series(self, title: str): 
        if not self.time_col:
            raise ValueError("time_col must be set to use time series plot.")

        # 피클 파일이 존재하면 불러오기
        if os.path.exists(self.line_file):
            with open(self.line_file, 'rb') as f:
                return pickle.load(f)

        # 피클 파일이 없다면 시계열 라인 그래프 새로 생성하기
        fig = go.Figure()
        # 첫 번째 라인 생성
        fig.add_trace(go.Scatter(
            x=self.df[self.time_col],
            y=self.df[self.x_col],
            mode='lines+markers',
            name=self.x_col,
            line=dict(color=self.x_color),
            marker=dict(size=8)
        ))

        # 두 번째 라인 생성
        fig.add_trace(go.Scatter(
            x=self.df[self.time_col],
            y=self.df[self.y_col],
            mode='lines+markers',
            name=self.y_col,
            line=dict(color=self.y_color),
            marker=dict(size=8)
        ))

        # 라인 그래프 제목, 축 라벨, 범례설정
        fig.update_layout(
            title=title,
            xaxis_title=self.time_col,
            yaxis_title='Scaled Values',
            legend_title='Metrics',
            template='plotly_white'
        )

        # 피클로 저장
        with open(self.line_file, 'wb') as f:
            pickle.dump(fig, f)

        # plotly 객체 return
        return fig