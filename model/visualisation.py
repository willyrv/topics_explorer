#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import plotly.graph_objects as go

class Views(object):
    def __init__(self,topic_model):
        
        self.model = topic_model
        
        self.scaled_topics = go.Figure(data=[go.Scatter(
            x=self.model.topic_2d_coordinates()[:,0], 
            y=self.model.topic_2d_coordinates()[:,1],
            text=["Topic" + str(i) for i in range(self.model.number_topics)],
            mode='markers',
            marker=dict (
                size=self.model.topics_frequency(),
                sizemode='area',
                sizeref=2.*max(self.model.topics_frequency())/(50.**2),
                color=np.linspace(0, self.model.number_topics,self.model.number_topics),
                showscale=True
                )
            )]) 
        
    def frequency_topic_evolution(self,topic_id):
        fig = go.Figure(data=[go.Bar(x=self.model.corpus.years,
                                     y=self.model.topic_frequency_per_dates(topic_id))])
        return fig