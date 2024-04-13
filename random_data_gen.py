import pandas as pd
import random

# Generate truck names
truck_names = []
for i in range(1, 501):
    if random.random() < 0.5:
        truck_names.append(f"A_{i}")
    else:
        truck_names.append(f"B_{i}")

# Generate random usage counts
usage_counts = [random.randint(0, 10) for _ in range(500)]

# Create DataFrame
truck_inventory_df = pd.DataFrame({
    'Truck name': truck_names,
    'No. of times used': usage_counts
})

# Save to csv
truck_inventory_df.to_csv('truck_inventory.csv', index=False)


# Generate random station names
stations = [f"Station_{i}" for i in range(1, 101)]

# Generate random demand for HSD and MS for each station
demand_hsd = [random.randint(500, 2000) for _ in range(100)]
demand_ms = [random.randint(500, 2000) for _ in range(100)]

# Create DataFrame
demand_df = pd.DataFrame({
    'Station name': stations,
    'Demand of HSD': demand_hsd,
    'Demand of MS': demand_ms
})

# Save to Excel
demand_df.to_csv('demand.csv', index=False)
