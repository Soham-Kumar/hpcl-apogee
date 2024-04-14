# hpcl-apogee
1. synthetic_demand_data.csv is the synthetic data created for demand of diesel and petrol based on 8 factors.
2. truck_inventory.py: It takes as input the data of how many times a truck has been used and which all trucks of what capacity are available. It gives as output truck_used.csv, which tells which trucks are used to carry the predicted amount of MS and HSD form source ot stations. In this, random data is used, as the major evaluative component remains the core logic of the code. We have taken that there are 2 types of trucks - of 24KL and 12KL capacity, with maximum 6 segments, tht of 3 or 4KL each.
3. lstm_train.py: Trains a basic LSTM model, as it was most common among the baseline research papers. The hyperparameters are chosen from various papers and by personal experimentation. The weights are saved as lstm_weights.pth. The training log is shared in error.txt.

Reason for low accuracy:
The reason for low accuracy is almost surely lack of coherency in synthetic data. The data doesn't represent a coherent solution curve in the space, hence finding a mininima is difficult. As the data is generated randomly, it contains more noise than patterns. As warranted by numerous papers on demand forecastng using LSTMs and its variants, the accuracy will go up upon usage of real world data which makes sense.
