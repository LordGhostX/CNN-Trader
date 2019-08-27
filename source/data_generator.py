import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from mpl_finance import candlestick_ohlc


def generate_chart(chart_df, index):
    # reset df index to avoid errors from derived dataframe
    chart_df.reset_index(inplace=True)

    # chart plotting subplot
    ax1 = plt.subplot2grid((1,1),(0,0))

    # candlestick ohlc data genration
    ohlc = []
    for i in range(len(chart_df)):
        ohlc.append([i, chart_df.open[i], chart_df.high[i], chart_df.low[i], chart_df.close[i]])

    # plot the candlestick data
    candlestick_ohlc(ax1, ohlc, colorup="grey", colordown="black")

    # hide axis value so we don't give our model unnecessary noise
    ax1.axes.get_xaxis().set_visible(False)
    ax1.axes.get_yaxis().set_visible(False)

    # save image
    img_name = "data/images/chart-data-{}.png".format(index)
    plt.savefig(img_name)

    # convert to black and white then resize
    img = Image.open(img_name).convert('LA')
    img.resize((160, 120), Image.ANTIALIAS)
    img.save(img_name)

if __name__ == "__main__":
    # params
    bars_per_image = 20
    future_classification_level = 10

    # read csv data
    df = pd.read_csv("data/BTCUSD_1h.csv")[:100]

    # generate image data from csv
    index = 1
    for i in range(bars_per_image, len(df) - future_classification_level):
        generate_chart(df[i - bars_per_image: i], index)
        index += 1
