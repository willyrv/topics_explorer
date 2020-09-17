#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import plotly.graph_objects as go

colors = ['#FF0000','#FFFF00','#FF00FF','#00FFFF','#800000','#008000','#808000','#800080','#008080','#C0C0C0','#808080','#9999FF','#993366','#FF8080','#0066CC','#CCCCFF','#000080','#00CCFF','#CCFFCC','#FFFF99','#FF99CC','#FFCC00','#FF9900','#FF6600','#666699','#969696','#003366','#333333','#339966','#003300','#333300','#993300','#333399','#0000FF','#99CCFF','#CC99FF','#FFCC99','#3366FF','#33CCCC','#99CC00','#00FF00']

class Views(object):

    '''view object permits to create all the available graphs in the application. Each graph is a figure object build with the librairy plotly.'''

    def __init__(self,topic_model):
        
        self.model = topic_model #: A TopicModel object
        self.colors = colors[:self.model.number_topics] #: vector with all the colors' references for each topic
        
    def scaled_topics(self):

        '''Create a graph with a colored buble for each topic using 2-dimensional coordinates based on distance between topics. Each buble's size is proportional to the importance of the topic in the corpus. On hover, you can see the top words of the selected topic'''

        scaled = go.Figure(data=[go.Scatter(
            x=self.model.topic_coordinates[:,0], 
            y=self.model.topic_coordinates[:,1],
            hovertemplate= "Topic %{text}: <br> %{customdata} </br><extra></extra>",
            customdata=[self.model.display_top_words_1topic(topic,10) for topic in range(self.model.number_topics)],
            mode='markers+text',
            marker=dict (
                size=self.model.topics_proportion,
                sizemode='area',
                sizeref=2.*max(self.model.topics_proportion)/(120.**2),
                color=colors,
                showscale=False),
            text=[str(i) for i in range(self.model.number_topics)]
            )],
            layout=go.Layout(
                autosize=True,
                height = 700,
                xaxis=dict(visible=True),
                yaxis=dict(visible=True)
            )
        )
        return scaled
        
        
    def frequency_topic_evolution(self,topic_id):

        '''Create a histogram where each bar represents the proportion of the topic for a precise year.''' 

        if self.model.corpus.dates==False:
            raise Exception('dates are missing')
        fig = go.Figure(
            data=[go.Bar(
                x=self.model.corpus.years,
                y=self.model.topic_frequency_per_dates(topic_id),
                hovertemplate= "Year %{x} : <br> %{y} </br><extra></extra>")],
            layout= dict(
                yaxis=dict(ticksuffix='%'),
                plot_bgcolor = 'white')
                
            )
        return fig

    def frequency_word_topics(self,word_id):

        '''Create a histogram with the proportion of each topic for a selected word''' 

        fig = go.Figure(
            data=[go.Bar(
                x=[i for i in range(self.model.number_topics)],
                y=self.model.frequency_word_for_topics(word_id),
                hovertemplate= "Topic %{x} : %{customdata} <br> %{y} </br><extra></extra>",
                marker_color = colors[:self.model.number_topics],
                customdata=[self.model.display_top_words_1topic(topic,10) for topic in range(self.model.number_topics)])],
            layout= dict(
                yaxis=dict(ticksuffix='%'),
                plot_bgcolor = 'white',
                xaxis=dict(title='Topics'))                
            )
        return fig

    def frequency_doc_topics(self,doc_id):

        '''Create a histogram with the proportion of each topic for a selected document''' 

        fig = go.Figure(
            data=[go.Bar(
                x=[i for i in range(self.model.number_topics)],
                y=self.model.frequency_doc_for_topics(doc_id),
                hovertemplate= "Topic %{x} : %{customdata} <br> %{y} </br><extra></extra>",
                marker_color = colors[:self.model.number_topics],
                customdata=[self.model.display_top_words_1topic(topic,10) for topic in range(self.model.number_topics)])],
            layout= dict(
                yaxis=dict(ticksuffix='%'),
                plot_bgcolor = 'white',
                xaxis=dict(title='Topics'))                
            )
        return fig

    
    def racing_bar_graph(self):

        '''Create an animated histogram which can be controlled by a play and a pause button and which represents the frequency evolution of each topic over years'''

        if self.model.corpus.dates==False:
            raise Exception('dates are missing')
        # make figure
        fig_dict = {
            "data": [],
            "layout": {},
            "frames": []
        }
        # fill in most of layout
        fig_dict['layout']['xaxis']= {"range":[0,100],
                                    "autorange":False,
                                    "title":'percentage in the corpus',
                                    'tickfont':dict(size=14)}
        fig_dict["layout"]["yaxis"] = {"range":[-0.5,self.model.number_topics+0.5],
                                    "autorange":False,
                                    "tickprefix":'Topic ',
                                    'tickfont':dict(size=14)}
        fig_dict["layout"]["hovermode"] = "closest"
        fig_dict["layout"]["yaxis_type"] = 'category'
        fig_dict['layout']['autosize'] = True
        fig_dict['layout']['height'] = 700
        fig_dict["layout"]["title"] = {
            'text':"topics' frequencies ",
            'font':dict(size=28),
            'x':0.5,
            'xanchor':'center'
        }
        fig_dict["layout"]['plot_bgcolor']='white'
        fig_dict["layout"]["updatemenus"] = [
            {"buttons": [
                {"label": "Play",
                "method": "animate",             
                "args": [None, {"frame": {"duration": 500, "redraw": False},
                                "fromcurrent": True, "transition": {"duration": 300,
                                                                    "easing": "linear"}}]},
                {"label": "Pause",
                "method": "animate",
                "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                "mode": "immediate","transition": {"duration": 0}}]}
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"}]
        
        sliders_dict = {
            "active": 0,
            "yanchor": "top",
            "xanchor": "left",
            "currentvalue": {
                "font": {"size": 20},
                "prefix": "Year:",
                "visible": True,
                "xanchor": "right"},
            "transition": {"duration": 300, "easing": "cubic-in-out"},
            "pad": {"b": 10, "t": 50},
            "len": 0.9,
            "x": 0.1,
            "y": 0,
            "steps": []
        }
        
        #make data
        year= self.model.corpus.years[0]
        fig_dict['data'] = [{
            'type':'bar',
            'x': self.model.topics_frequency_per_dates[:,0],
            'y': np.linspace(0, self.model.number_topics-1,self.model.number_topics),
            'orientation' : 'h',
            'text' : self.model.topics_frequency_per_dates[:,0],
            'texttemplate' : '%{text:.3s}',
            'textfont' : {'size':18},
            'textposition' : 'inside',
            'insidetextanchor' : 'middle',
            'width' : 0.9,
            'marker' : {'color':colors},
            'hovertemplate' : "%{y}: <br> %{customdata} </br><extra></extra>",
            'customdata' : [self.model.display_top_words_1topic(topic,10) for topic in range(self.model.number_topics)]   
        }]
        
        #make frames
        for year in range(len(self.model.corpus.years)):
            frame = {"data": [], "name": str(year)}
            frame["data"] = [{
                'type':'bar',
                'x': self.model.topics_frequency_per_dates[:,year],
                'y': np.linspace(0, self.model.number_topics-1,self.model.number_topics),
                'orientation' : 'h',
                'text' : self.model.topics_frequency_per_dates[:,year],
                'texttemplate' : '%{text:.3s}',
                'textfont' : {'size':18},
                'textposition' : 'inside',
                'insidetextanchor' : 'middle',
                'width' : 0.9,
                'marker' : {'color':colors}        
            }]
            fig_dict["frames"].append(frame)
            slider_step = {"args": [[year],
                                    {"frame": {"duration": 300, "redraw": False},
                                    "mode": "immediate",
                                    "transition": {"duration": 300}}],
                        "label": str(self.model.corpus.years[year]),
                        "method": "animate"}
            sliders_dict["steps"].append(slider_step)
            
        fig_dict["layout"]["sliders"] = [sliders_dict]
        return go.Figure(fig_dict)

        

    def streamgraph(self):

        '''Create a graph where the evolution of the proportion of the topics is represented by the place taking by the topic.''' 

        if self.model.corpus.dates==False:
            raise Exception('dates are missing')
        freq_matrix = self.model.topics_cumulative_frequencies
        x=self.model.corpus.years
        streamgraph = go.Figure()
        streamgraph.add_trace(go.Scatter(
            x=x,
            y=freq_matrix[0,:],
            name="Topic 0",
            mode='lines',
            line=dict(width=0.5, color=colors[0]),
            stackgroup ='one',
            groupnorm='percent'
        ))
        for id in range(1,self.model.number_topics):
            streamgraph.add_trace(go.Scatter(
                x=x,
                y=freq_matrix[id,:],
                name="Topic " + str(id),
                mode='lines',
                line=dict(width=0.5, color=colors[id]),
                stackgroup ='one'
            ))
        streamgraph.update_layout(
            showlegend=True,
            legend=dict(
                orientation='h',
                yanchor='bottom',
                xanchor='right',
                y=1.02,
                x=1
            ),
            autosize=True,
            height = 700,
            legend_itemclick = False,
            hovermode='x unified',   
            clickmode='none',   
            xaxis_type='category',
            yaxis=dict(
                type='linear',
                range=[0,100],
                ticksuffix='%'))

        return streamgraph

    def table(self):

        '''Table with 3 columns containing the number of the topics, their top words and their proportion in the corpus'''

        table = go.Figure(data=[go.Table(
            columnorder= [1,2,3,4],
            columnwidth=[50,500,100,100],
            header= dict(
                values=['TOPICS','TOP WORDS','PROPORTION IN THE CORPUS'],
                height=30,
                fill=dict(color='black'),
                align='center',
                font=dict(size=14,color='white')),
            hoverinfo = 'all',
            cells= dict(values=[
                [id for id in range(self.model.number_topics)],
                [self.model.display_top_words_1topic(topic,10) for topic in range(self.model.number_topics)],
                np.around(self.model.topics_proportion,2)
            ],
            fill=dict(color=[['lightgrey','white']*int(self.model.number_topics+1/2)]),
            font=dict(color='black'),
            height=30,
            line_color='darkslategray'
            )
        )],
        layout=go.Layout(
                plot_bgcolor='white',
                #autosize=True,
                clickmode = 'event'
            )
        )
        return table
            
