import plotly
import plotly.graph_objects as go
import plotly.offline as offline
import plotly.express as px
import pandas as pd
import numpy as np
from fetch import Fetch
class PlotPlotly(Fetch):
    def __init__(self,  security_name, expiry):
        super().__init__( security_name, expiry)
        self.expiry=expiry
        self.plot_Open_Interest()
        self.plot_Open_Interest_Change()
    def plot_Open_Interest(self):
        # tickvals = [0, 5e3, 1e4, 5e4, 1e5, 5e5, 1e6, 5e6, 1e7]
        # ticktext = ['0', '5K', '10K', '50K', '100K', '500K', '1M', '5M', '10M']

        total_put_oi = sum(x for x in self.put_oi if x is not None)
        total_call_oi = sum(x for x in self.call_oi if x is not None)
        round_total_put_oi = f"{round(total_put_oi/1000000, 2)} (in M)" if total_put_oi > 100000 else round(total_put_oi)
        round_total_call_oi = f"{round(total_call_oi/1000000, 2)} (in M)" if total_call_oi > 100000 else round(total_call_oi)
        pcr = round(total_put_oi/total_call_oi, 3) if total_call_oi != 0 else 0
        hist1 = go.Bar(x=self.near_atm_strikes, y=self.call_oi, marker_color='red', name = "Call OI")
        hist2 = go.Bar(x=self.near_atm_strikes, y=self.put_oi, marker_color='green', name = "Put OI")
        volume_trace1 = go.Scatter(x=self.near_atm_strikes, y=self.call_volume, mode='lines', name='Volume Call OI', yaxis='y2')
        volume_trace2 = go.Scatter(x=self.near_atm_strikes, y=self.put_volume, mode='lines', name='Volume Put OI', yaxis='y2')

        # layout = go.Layout(paper_bgcolor='white')
        # fig = go.Figure(data=[hist1, hist2, volume_trace2, volume_trace1,], layout=layout)
        

        fig = go.Figure(data=[hist1, hist2, volume_trace2, volume_trace1,],)
        fig.update_layout(yaxis=dict(tickformat='.3s'))
        fig.update_layout(yaxis2=dict(overlaying='y', side='right', tickformat='.3s'),xaxis_tickangle=-45)
        fig.update_layout(xaxis=dict(tickmode='array', tickvals=self.near_atm_strikes, ticktext=self.near_atm_strikes, tickformat=',d'))
        fig.update_layout(
            dragmode='drawopenpath',
            newshape_line_color='cyan',
            modebar_add=["v1hovermode", "hoverclosest", "hovercompare", "togglehover",
                         'drawline','drawopenpath','eraseshape','togglespikelines'],
            modebar_remove=['zoom', 'pan', ],
            modebar_orientation='v',
            transition_duration=0,
            # margin_b=40,
            # margin_l=10,
            # margin_r=30,
            # margin_t=80,
            # margin_pad=10,
            # autosize=True,
            # width=900,
            height=600
        )

        # fig.update_layout(yaxis2=dict(overlaying='y', side='right', tickformat='.3s'), xaxis=dict(rangeslider=dict(visible=False)))
        fig.update_layout(title=dict(text='Open Interest', font=dict(size=24, color='#000000')),
        xaxis_title=dict(text=f'{self.security_name}', font=dict(size=20, color='#000000')),
        yaxis_title=dict(text='Open Interest', font=dict(size=20, color='#000000')),
        yaxis2_title=dict(text='Volume', font=dict(size=20, color='#000000')))
        # plot_html = offline.plot(fig, include_plotlyjs=True, output_type='div')
        fig.add_annotation(
        x=0,
        y=1,
        showarrow=False,
        text=f"Spot Price: {self.spot_price}<br>PCR: {pcr}<br>Total Put OI: {round_total_put_oi}<br>Total Call OI: {round_total_call_oi}<br>Data Fetched at:{self.fetched_time}<br>Data Shown for Expiry:{self.expiry_date}",
        xref="paper",
        yref="paper",
        align='left')

        config = dict({'scrollZoom': True})
        
        # return plot_html
        return fig
    def plot_Open_Interest_Change(self):
        total_put_oi_change=sum(x for x in  self.put_change_oi if x is not None)
        total_call_oi_change=sum(x for x in self.call_change_oi if x is not None)
        round_total_put_oi_change = total_put_oi_change
        if -100000 > total_put_oi_change or total_put_oi_change > 100000:
            round_total_put_oi_change = f"{round(round_total_put_oi_change/1000000,2)} (in M)"
        round_total_call_oi_change = total_call_oi_change
        if -100000 > total_call_oi_change or total_call_oi_change > 100000:
            round_total_call_oi_change = f"{round(round_total_call_oi_change/1000000,2)} (in M)"
  
        call_premium=[int(i*self.lot_size) for i in self.call_price]
        put_premium=[int(i*self.lot_size) for i in self.put_price]
    
        hist3 = go.Bar(x=self.near_atm_strikes, y=self.call_change_oi, marker_color='red', name = "Call OI Change")
        hist4 = go.Bar(x=self.near_atm_strikes, y=self.put_change_oi, marker_color='green', name = "Put OI Change")

        price_trace1 = go.Scatter(x=self.near_atm_strikes, y=self.call_price, mode='lines', name='Call Price', yaxis='y2', visible='legendonly')
        price_trace2 = go.Scatter(x=self.near_atm_strikes, y=self.put_price, mode='lines', name='Put Price', yaxis='y2', visible='legendonly')
        call_premium_trace=go.Scatter(x=self.near_atm_strikes, y=call_premium, mode='lines', name='Call Premium', yaxis='y2', visible='legendonly')
        put_premium_trace=go.Scatter(x=self.near_atm_strikes, y=put_premium, mode='lines', name='Put Premium', yaxis='y2', visible='legendonly')
        
        fig2 = go.Figure(data=[hist3, hist4, price_trace1, price_trace2, call_premium_trace, put_premium_trace])


        # fig2 = go.Figure(data=[hist3, hist4,])
        fig2.update_layout(yaxis=dict(tickformat='.3s'))
        fig2.update_layout(yaxis2=dict(overlaying='y', side='right', tickformat='.3s'),xaxis_tickangle=-45)
        fig2.update_layout(yaxis2={'type':'log'}),
        fig2.update_layout(xaxis=dict(tickmode='array', tickvals=self.near_atm_strikes, ticktext=self.near_atm_strikes, tickformat=',d'))

        fig2.update_layout(
            dragmode='drawopenpath',
            newshape_line_color='cyan',
            modebar_add=["v1hovermode", "hoverclosest", "hovercompare", "togglehover",
                         'drawline','drawopenpath','eraseshape','togglespikelines'],
            modebar_remove=['zoom', 'pan', ],
            modebar_orientation='v',
            transition_duration=0,
            # margin_b=40,
            # margin_l=10,
            # margin_r=30,
            # margin_t=80,
            # margin_pad=10,
            # autosize=True,
            # width=900,
            height=600
        )

        # fig2.update_layout(yaxis2=dict(overlaying='y', side='right', tickformat='.3s'), xaxis=dict(rangeslider=dict(visible=False)))
        fig2.update_layout(title=dict(text='Open Interest Change', font=dict(size=24, color='#000000')),
        xaxis_title=dict(text=f'{self.security_name}', font=dict(size=20, color='#000000')),
        yaxis_title=dict(text='Open Interest Change', font=dict(size=20, color='#000000')),
        yaxis2_title=dict(text='Price', font=dict(size=20, color='#000000')))

        
        plot2_html = offline.plot(fig2, include_plotlyjs=True, output_type='div')
        fig2.add_annotation(
        x=0,
        y=1,
        showarrow=False,
        text=f"Put OI Change: {round_total_put_oi_change}<br>Call OI Change: {round_total_call_oi_change}",
        xref="paper",
        yref="paper",
        align='left')
        return fig2
        # offline.plot(fig2, filename='plot2.html', auto_open=False)
        # return plot2_html