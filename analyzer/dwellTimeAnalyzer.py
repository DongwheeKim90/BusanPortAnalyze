import pandas as pd
import plotly.express as px
import os
import pickle

class dwellTimeAnalyzer:
    def __init__(self, df, y, x, by: bool=False, marker_color=None):
        self.df = df
        self.x_col = x
        self.y_col = y
        self.marker_color = marker_color
        self.by = by
        if by==False:
            self.boxplot_file = f'graph/{y}_Boxplot.pkl'
        else:
            self.boxplot_file = f'graph/{y}_Boxplot_by_{x}'

    def draw_boxplot(self,title: str):
        if os.path.exists(self.boxplot_file):
            with open(self.boxplot_file, 'rb') as f:
                return pickle.load(f)
        
        if self.by==False:
            fig = px.box(
                self.df,
                y = self.y_col
            )
        else:
            fig = px.box(
                self.df,
                x = self.x_col,
                y = self.y_col
            )

        fig.update_layout(
            title = dict(
                text = title,
                x = 0.5,
                xanchor = 'center',
                font = dict(color='white')
            ),
            plot_bgcolor="black",
            paper_bgcolor="black",
            font=dict(color="white"),
            xaxis=dict(
                title=dict(text=self.x_col, font=dict(color="white")),
                tickfont=dict(color="white")
            ),
            yaxis=dict(
                title=dict(text=self.y_col, font=dict(color="white")),
                tickfont=dict(color="white"),
                gridcolor="gray"
            )
        )

        fig.update_traces(
            marker_color=self.marker_color,
            boxmean=True
            )
        
        with open(self.boxplot_file, 'wb') as f:
            pickle.dump(fig, f)

        return fig