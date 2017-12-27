import numpy as np
import excel_reader
from matplotlib import pyplot as plt

DATA_FROM = 0
DATA_TO = 10000
#FEATURE_SCALE = np.array([[1000, 1000, 1000, 1000, 1000]])
FEATURE_SCALE = 1000


def std_moving_average(log_price, i, period):
    return np.mean(log_price[i - period:i - 1, :])


def feature_transform(log_price, i):
    ma_60_out = std_moving_average(log_price, i + 60, 60) - log_price[i]
    ma_60_1 = std_moving_average(log_price, i - 60, 60)
    ma_60_2 = std_moving_average(log_price, i, 60)
    ma_120_1 = std_moving_average(log_price, i - 120, 120)
    ma_120_2 = std_moving_average(log_price, i, 120)
    ma_240_1 = std_moving_average(log_price, i - 240, 240)
    ma_240_2 = std_moving_average(log_price, i, 240)
    ma_480_1 = std_moving_average(log_price, i - 480, 480)
    ma_480_2 = std_moving_average(log_price, i, 480)
    ma_960_1 = std_moving_average(log_price, i - 960, 960)
    ma_960_2 = std_moving_average(log_price, i, 960)
    d_60 = ma_60_2 - ma_60_1
    d_120 = ma_120_2 - ma_120_1
    d_240 = ma_240_2 - ma_240_1
    d_480 = ma_480_2 - ma_480_1
    d_960 = ma_960_2 - ma_960_1
    features = np.vstack((d_60,
                          d_120,
                          d_240,
                          d_480,
                          d_960
                          ))
    return features * FEATURE_SCALE, ma_60_out * FEATURE_SCALE


def generate_features(log_price, from_id, to_id):
    features = np.hstack((
        feature_transform(log_price, from_id)[0],
        feature_transform(log_price, from_id + 1)[0]
    ))
    out = np.hstack((
        feature_transform(log_price, from_id)[1],
        feature_transform(log_price, from_id + 1)[1]
    ))
    for i in range(from_id + 2, to_id):
        features = np.hstack((features, feature_transform(log_price, i)[0]))
        out = np.hstack((out, feature_transform(log_price, i)[1]))
    return features.T, out.T


def generate():
    p = excel_reader.get_data(DATA_FROM, DATA_TO, 'D:\python\projdata\data\\1m.xlsx')
    log_price = np.log(p)
    plt.plot(p)
    plt.show()
    plt.plot(log_price)
    plt.show()
    features, out = generate_features(log_price, DATA_FROM + 1921, DATA_TO - 60)
    features_mean = np.mean(features, axis=0)
    print('means:', features_mean)
    print(features)
    print(out)
    plt.plot(features)
    plt.show()
    plt.plot(out)
    plt.show()

generate()


