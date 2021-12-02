'''
    File name: analysis.py
    Author: Vitor Hespanhol Côrtes
    Date created: 12/1/2020
    Date last modified: 12/1/2020
    Python Version: 3.6
'''

import pickle
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from  .toolkit.tools import errorMessage

## Class Analysis
# - realiza análise dos resultados
class Analysis:
    def __init__(self, respath):
        self.respath = respath
        
    def load_results(self):
        #try:
        with open(self.respath, 'rb') as inp:
            self.res = pickle.load(inp)
        
        self.pars = [par.pName for par in self.res.std.parameters]
        self.cases = [case.cName for case in self.res.std.cases]
        ofs = [of.ofName for of in self.res.std.objFuncs]
        delta = [of.delta for of in self.res.std.objFuncs]
        OFs = []
        for i,row in enumerate(ofs):
            for cs in self.cases:
                OFs.append(row+'_'+cs)
            if delta[i]==True:
                OFs.append(row+'_Delta')
        self.ofs = OFs
        self.results = self.res.results

    # Mostra crossplot correlacionando parâmetros com FO    
    def xPlot(self,par1,par2,of1,of2):
        fig = px.scatter( self.results, x=par1, y=par2, color=of1,size = of2, marginal_y="violin",
            marginal_x="violin", trendline="ols",  template="seaborn")
        fig.show()
    
    # Mostra histogramama com percentis
    def hist( self, of1, nbins = 10):
        x00 = self.results[of1].values
        
        #Figure
        fig = make_subplots(
            rows=3, cols=1,
            specs=[[{"type": "histogram", "rowspan": 2}],
                [None],
                [{"type": "box"}]])
        #Histogram
        fig.add_trace(go.Histogram(x=x00,histnorm='probability',nbinsx = nbins),row=1, col=1)
        
        #Boxplot
        fig.add_trace(go.Box(x=x00,boxpoints='all',jitter=0.3,pointpos=0,
                                name = 'models',
                                marker=dict(
                                color='black',size = 2),
                                line_color='blue'

                            ),row=3, col=1)
        # Percentis
        perc = np.zeros(3)
        perc[0]= np.percentile(x00,10)
        perc[1]= np.percentile(x00,50)
        perc[2]= np.percentile(x00,90)
        
        fig.add_vline(
                x=perc[0], line_width=2, line_dash="dot", 
                line_color="black",
                annotation_text=('%.1f MM (P10)' % (perc[0]/1e6)), 
                annotation_position="top left",
                row=1, col=1)

        fig.add_vline(
                x=perc[1], line_width=2, line_dash="dot", 
                line_color="black",
                annotation_text=('%.1f MM (P50)' % (perc[1]/1e6)), 
                annotation_position="top",
                row=1, col=1)

        fig.add_vline(
                x=perc[2], line_width=2, line_dash="dot", 
                line_color="black",
                annotation_text=('%.1f MM (P90)' % (perc[2]/1e6)), 
                annotation_position="top right",
                row=1, col=1)

        # Config
        fig.update_layout(barmode='overlay',
                        title=('Uncertainty Analysis - Objective Function: %s' % of1),
                        yaxis_title='Probability',
                        showlegend=False,
                        plot_bgcolor='white')
        xrang = [np.min(x00)*.98,np.max(x00)*1.02]
        
        fig.update_xaxes(range=xrang)
        fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
        fig.update_yaxes(showline=True, linewidth=2, linecolor='black')
        
        # Reduce opacity
        fig.update_traces(opacity=0.75)
        fig.show()
        return 