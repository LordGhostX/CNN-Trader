import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from os.path import basename
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
    img_name = "data/images/chart-data-{}.jpg".format(index)
    plt.savefig(img_name)

    # convert to black and white then resize
    img = Image.open(img_name).convert('L')
    img = img.resize((160, 120), Image.ANTIALIAS)
    img.save(img_name)

    # print("Generated {}".format(img_name))
    # return np.array(img.getdata())
    return basename(img_name)

if __name__ == "__main__":
    # params
    bars_per_image = 20
    future_classification_level = 10

    # read csv data
    limit = 3000
    df = pd.read_csv("data/BTCUSD_1h.csv")[::-1][:limit + bars_per_image + future_classification_level][::-1]
    df.reset_index(inplace=True)

    # generate image data from csv
    index = 1
    img_csv = "id,target\n"

    print("Starting Generation...")
    for i in range(bars_per_image, len(df) - future_classification_level):
        img_name = generate_chart(df[i - bars_per_image: i], index)
        target = int(df.close[i] <= df.close[i + future_classification_level])
        img_csv += "{},{}\n".format(img_name, target)
        index += 1
    with open("data/labels.csv", "w") as f:
        f.write(img_csv)
