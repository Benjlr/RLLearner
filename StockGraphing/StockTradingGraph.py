import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mpl_finance import candlestick_ochl as candlestick


def date2num(date):
  converter = mdates.strpdate2num('%d/%m/%Y')
  return converter(date)


class StockTradingGraph:
    """Copyright TruffleCo Industries 2019
        Authoriser: Benjamin Roberts (CEO, CTO, MD)
        For All Those Truffling Needs"""

    def __init__(self, df, title=None):
        self.df = df
        self.net_worths = np.zeros(len(df['Date']))

        # Create a figure on screen and set the title
        fig = plt.figure()
        fig.suptitle(title)

        # Create top subplot for net worth axis
        self.net_worth_ax = plt.subplot2grid((6, 1), (0, 0), rowspan=2,     
            colspan=1)
        
        # Create bottom subplot for shared price/volume axis
        self.price_ax = plt.subplot2grid((6, 1), (2, 0), rowspan=8, 
            colspan=1, sharex=self.net_worth_ax)

        # Create a new axis for volume which shares its x-axis with price
        self.volume_ax = self.price_ax.twinx()

        # Add padding to make graph easier to view
        plt.subplots_adjust(left=0.11, bottom=0.24, right=0.90, 
            top=0.90, wspace=0.2, hspace=0)

        # Show the graph without blocking the rest of the program
        plt.show(block=False)
    

    def render(self, current_step, net_worth, trades, window_size=40):
        self.net_worths[current_step] = net_worth
        window_start = max(current_step - window_size, 0)
        step_range = range(window_start, current_step +1)

        dates = np.array([date2num(x)
            for x in self.df['Date'].values[step_range]])

        self._render_net_worth(current_step, net_worth, window_size, dates)
        self._render_price(current_step, net_worth, window_size, dates, step_range)
        #self._render_volume(current_step, net_worth, dates, step_range)
        self._render_trades(current_step, trades, step_range)

        # Format the date ticks to be more easily read
        self.price_ax.set_xticklabels(self.df['Date'].values[step_range],
            rotation=45, horizontalalignment='right')

        plt.setp(self.net_worth_ax.get_xticklabels(), visible=False)
        plt.pause(0.001)

    
    def _render_net_worth(self, current_step, net_worth, step_range, dates):
        # Clear the last rendered frame
        self.net_worth_ax.clear()

        # Plot net worths
        self.net_worth_ax.plot_date(dates, self.net_worths[step_range], '-', Label='Net Worth')
        self.net_worth_ax.legend()
        legend = self.net_worth_ax.legendA(Loc=2, ncol=2, prop={'size': 8})
        legend.get_frame().set_alpha(0.4)

        last_date =date2num(self.df['Date'].values[current_step])
        last_net_worth =self.net_worths[current_step]

         # Annotate the current net worth on the net worth graph
        self.net_worth_ax.annotate('{0:.2f}'.format(net_worth),     
        (last_date, last_net_worth),
        xytext=(last_date, last_net_worth),
        bbox=dict(boxstyle='round', fc='w', ec='k', lw=1),
        color="black",
        fontsize="small")

        # Add space above and below min/max net worth
        self.net_worth_ax.set_ylim(
        min(self.net_worths[np.nonzero(self.net_worths)]) / 1.25,    
        max(self.net_worths) * 1.25)


    def _render_price(self, current_step, net_worth, dates, step_range):
        self.price_ax.clear()

        # Format data for OHCL candlestick graph
        candlesticks = zip(dates,
        self.df['assetOpen'].values[step_range],  
        self.df['assetClose'].values[step_range],
        self.df['assetHigh'].values[step_range], 
        self.df['assetLow'].values[step_range])

        # Plot price using candlestick graph from mpl_finance
        candlestick(self.price_ax, candlesticks, width=1,
        colorup=UP_COLOR, colordown=DOWN_COLOR)
        last_date = date2num(self.df['Date'].values[current_step])
        last_close = self.df['assetClose'].values[current_step]
        last_high = self.df['assetHigh'].values[current_step]

        # Print the current price to the price axis
        self.price_ax.annotate('{0:.2f}'.format(last_close),
        (last_date, last_close),
        xytext=(last_date, last_high),
        bbox=dict(boxstyle='round', fc='w', ec='k', lw=1),
        color="black",
        fontsize="small")

        # Shift price axis up to give volume chart space
        ylim = self.price_ax.get_ylim()
        self.price_ax.set_ylim(ylim[0] - (ylim[1] - ylim[0]) 
            * VOLUME_CHART_HEIGHT, ylim[1])


    def _render_volume(self, current_step, net_worth, dates, step_range):
        self.volume_ax.clear()
        volume = np.array(self.df['Volume'].values[step_range])
  
        pos = self.df['Open'].values[step_range] - \
            self.df['Close'].values[step_range] < 0
        neg = self.df['Open'].values[step_range] - \
            self.df['Close'].values[step_range] > 0
        
        # Color volume bars based on price direction on that date
        self.volume_ax.bar(dates[pos], volume[pos], color=UP_COLOR,
            alpha=0.4, width=1, align='center')
        self.volume_ax.bar(dates[neg], volume[neg], color=DOWN_COLOR,
            alpha=0.4, width=1, align='center')
        
        # Cap volume axis height below price chart and hide ticks
        self.volume_ax.set_ylim(0, max(volume) / VOLUME_CHART_HEIGHT)
        self.volume_ax.yaxis.set_ticks([])


    def _render_trades(self, current_step, trades, step_range):
        for trade in trades:
            if trade['step'] in step_range:
                date = date2num(self.df['Date'].values[trade['step']])
                high = self.df['assetHigh'].values[trade['step']]
                low = self.df['assetLow'].values[trade['step']]
            
            if trade['type'] == 'long':
                high_low = low
                color = UP_TEXT_COLOR
            else:
                high_low = high
                color = DOWN_TEXT_COLOR
            
            total = '{0:.2f}'.format(trade['total'])
      
      # Print the current price to the price axis   
        self.price_ax.annotate(f'${total}', (date, high_low),
        xytext=(date, high_low),
        color=color,
        fontsize=8,
        arrowprops=(dict(color=color)))



            

