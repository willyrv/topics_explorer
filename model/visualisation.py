#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import plotly.graph_objects as go

colors = ['#FF0000','#FFFF00','#FF00FF','#00FFFF','#800000','#008000','#808000','#800080','#008080','#C0C0C0','#808080','#9999FF','#993366','#FFFFCC','#CCFFFF','#660066','#FF8080','#0066CC','#CCCCFF','#000080','#00CCFF','#CCFFCC','#FFFF99','#FF99CC','#FFCC00','#FF9900','#FF6600','#666699','#969696','#003366','#333333','#339966','#003300','#333300','#993300','#333399','#0000FF','#99CCFF','#CC99FF','#FFCC99','#3366FF','#33CCCC','#99CC00','#00FF00']

class Views(object):
    def __init__(self,topic_model):
        
        self.model = topic_model
        self.colors = colors[:self.model.number_topics]
        
    def scaled_topics(self):
        fig = go.Figure(data=[go.Scatter(
            x=self.model.topic_2d_coordinates()[:,0], 
            y=self.model.topic_2d_coordinates()[:,1],
            hovertemplate= "Topic %{text}: <br> %{customdata} </br><extra></extra>",
            customdata=[self.model.display_top_words_1topic(topic,10) for topic in range(self.model.number_topics)],
            mode='markers+text',
            marker=dict (
                size=self.model.topics_frequency(),
                sizemode='area',
                sizeref=2.*max(self.model.topics_frequency())/(90.**2),
                color=colors,
                showscale=False),
            text=[str(i) for i in range(self.model.number_topics)]
            )],
            layout=go.Layout(clickmode='event+select'))
        fig.update_layout(
            plot_bgcolor='white',
            autosize=False,
            width=1000,
            height=600
        )
        return fig
        
        
    def frequency_topic_evolution(self,topic_id):
        fig = go.Figure(data=[go.Bar(x=self.model.corpus.years,
                                     y=self.model.topic_frequency_per_dates(topic_id))])
        return fig

    def racing_bar_graph(self):
        fig = go.Figure(
            data=[
                go.Bar(
                    x=self.model.topics_frequency_per_dates(self.model.corpus.years)[:,0],
                    y=np.linspace(0, self.model.number_topics-1,self.model.number_topics),
                    orientation='h',
                    text=self.model.topics_frequency_per_dates(self.model.corpus.years)[:,0],
                    texttemplate='%{text:.3s}',
                    textfont={'size':18},
                    textposition='inside',
                    insidetextanchor='middle',
                    width=0.9,
                    marker={'color':colors})
            ],
            layout=go.Layout(
                xaxis=dict(range=[0,100],autorange=False,title='percentage in the corpus',tickfont=dict(size=14)),
                yaxis=dict(range=[-0.5,self.model.number_topics+0.5],
                autorange=False,
                tickfont=dict(size=14),
                tickprefix='Topic '),
                yaxis_type = 'category',

                title=dict(text="topics' frequencies : "+ str(self.model.corpus.years[0]),font=dict(size=28),x=0.5,xanchor='center'),
                plot_bgcolor='white',
                updatemenus=[dict(
                    type='buttons',
                    buttons=[dict(
                        label='Play',
                        method='animate',
                        args=[None,
                        {"date":{'duration':5000,'redraw':True},
                        'transition':{'duration':250,'easing':'linear'}}]
                    )]
                )]
            ),
            frames=[
                go.Frame(
                    data=[
                        go.Bar(x=self.model.topics_frequency_per_dates(self.model.corpus.years)[:,value],
                        y=np.linspace(0, self.model.number_topics-1,self.model.number_topics),
                        orientation='h',
                        text=self.model.topics_frequency_per_dates(self.model.corpus.years)[:,value],
                        marker={'color':colors})
                    ],
                    layout=go.Layout(
                        xaxis=dict(range=[0,100],autorange=False,title='percentage in the corpus',tickfont=dict(size=14)),
                        yaxis=dict(range=[-0.5,self.model.number_topics+0.5],autorange=False,tickfont=dict(size=14)),
                        title=dict(text="topics' frequencies : "+ str(self.model.corpus.years[value]),font=dict(size=28),x=0.5,xanchor='center'))
                )
                for value in range(len(self.model.corpus.years))
            ]
        )
        fig.update_layout(
            autosize=False,
            width=800,
            height=600
        )
        return fig
