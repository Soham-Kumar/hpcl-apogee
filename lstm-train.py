import torch
import torch.nn as nn
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error


data = pd.read_csv("synthetic_demand_data.csv")

# Leave the last 200 instances
data = data[:-200]

rows_with_nan = data[data.isna().any(axis=1)]
print("Rows with one or more NaN values:")
print(rows_with_nan)

features = data[["Temperature", "Humidity", "Elevation", "Petrol tax", "Nifty 50 turnover"]]
target = data[["Petrol Sold", "Diesel Sold"]]

scaler = MinMaxScaler()
features_scaled = scaler.fit_transform(features)
target_scaled = scaler.fit_transform(target)

features_tensor = torch.Tensor(features_scaled)
target_tensor = torch.Tensor(target_scaled)

features_tensor = features_tensor.unsqueeze(0) 
target_tensor = target_tensor.unsqueeze(0)

class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size) 

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out)  
        return out

input_size = features.shape[1]
hidden_size = 64
num_layers = 2
output_size = target.shape[1]

model = LSTMModel(input_size, hidden_size, num_layers, output_size)

criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters())

num_epochs = 50
for epoch in range(num_epochs):
    outputs = model(features_tensor)
    loss = criterion(outputs, target_tensor)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

torch.save(model.state_dict(), 'lstm_model.pth')

# plt.plot(target_tensor.squeeze(0).detach().numpy(), label='Actual')
# plt.plot(outputs.squeeze(0).detach().numpy(), label='Predicted')
# plt.legend()
# plt.show()



model.eval()  # Set model to evaluation mode
with torch.no_grad():
  predictions = model(features_tensor)

# Inverse transform to get predictions in original scale
predictions_unscaled = scaler.inverse_transform(predictions.squeeze(0).detach().numpy())
target_unscaled = scaler.inverse_transform(target_tensor.squeeze(0).detach().numpy())

# Calculate MAE and RMSE for both Petrol and Diesel
mae_petrol = mean_absolute_error(target_unscaled[:, 0], predictions_unscaled[:, 0])
rmse_petrol = mean_squared_error(target_unscaled[:, 0], predictions_unscaled[:, 0], squared=False)

mae_diesel = mean_absolute_error(target_unscaled[:, 1], predictions_unscaled[:, 1])
rmse_diesel = mean_squared_error(target_unscaled[:, 1], predictions_unscaled[:, 1], squared=False)

print(f"Petrol MAE: {mae_petrol:.2f}")
print(f"Petrol RMSE: {rmse_petrol:.2f}")
print(f"Diesel MAE: {mae_diesel:.2f}")
print(f"Diesel RMSE: {rmse_diesel:.2f}")