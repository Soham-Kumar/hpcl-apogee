import pandas as pd
import math

def calculate_truck_combination(demand_df, truck_inventory_df):

    # Initialize dataframe to store truck used
    df = pd.DataFrame(columns=['station_name', 'trucks'])

    # Convert demand dataframe to dictionary for easier access
    demand_dict = demand_df.set_index('Station name').to_dict()
    
    # Sort truck inventory dataframe by 'No. of times used'
    truck_inventory_df.sort_values(by='No. of times used', inplace=True)
    
    # Initialize variables to store the trucks used and their corresponding demands
    trucks_used = []
    demands_met = {'MS': 0, 'HSD': 0}
    count = 0
    flag = False

    # Repeat until both MS and HSD demands for all stations are met
    while any(demand_dict['Demand of MS'][station] > 0 or demand_dict['Demand of MS'][station] > 0 for station in demand_dict['Demand of MS']):
        trucks_used = []
        demands_met = {'MS': 0, 'HSD': 0}

        # Iterate over demand for each station
        ms_demand_dict = demand_dict['Demand of MS']
        hsd_demand_dict = demand_dict['Demand of HSD']

        flag1 = False

        for (ms_station, ms_demand), (hsd_station, hsd_demand) in zip(ms_demand_dict.items(), hsd_demand_dict.items()):
            count += 1
            #print('===================================================================================================')
            #print(f"Station {count}")  # Debug #print
            #print('===================================================================================================')
            #print(f"MS demand at {ms_station}: {ms_demand}")  # Debug #print
            #print(f"HSD demand at {hsd_station}: {hsd_demand}")  # Debug #print
            #print(f"flag: {flag}")  # Debug #print
            if flag and ms_station == 'Station_1':
                return df
            if ms_station == 'Station_1':
                flag = True


            # Check if demand is non-zero
            if ms_demand > 0 or hsd_demand > 0:
                #print("Checking trucks...")  # Debug #print
                while ms_demand > 0 or hsd_demand > 0:
                    #print(f"MS demand remaining: {ms_demand}")  # Debug #print
                    #print(f"HSD demand remaining: {hsd_demand}") # Debug #print
                    truck_name = None
                    ms_in_truck = 0
                    hsd_in_truck = 0
                    
                    # Iterate over truck inventory to find suitable truck
                    for index, row in truck_inventory_df.iterrows():
                        #print(f"Checking truck {row['Truck name']}...")
                        if row['No. of times used'] == min(truck_inventory_df['No. of times used']):
                            truck_name = row['Truck name']
                            #print(f"Truck {truck_name} selected")  # Debug #print
                            truck_capacity = 24 if truck_name.startswith('A') else 12
                            compartments = 6 if truck_capacity == 24 else 3
                            total_volume = compartments * 4

                            # Fill the truck with initial demand
                            if total_volume <= ms_demand and total_volume <= hsd_demand:
                                ms_in_truck = total_volume/2
                                hsd_in_truck = total_volume/2
                                ms_demand -= ms_in_truck
                                hsd_demand -= hsd_in_truck
                                trucks_used.append(truck_name)
                                truck_inventory_df.loc[index, 'No. of times used'] += 1
                                demands_met['MS'] += ms_in_truck
                                demands_met['HSD'] += hsd_in_truck
                                #print(f"Truck {truck_name} loaded with MS: {ms_in_truck}, HSD: {hsd_in_truck}")  # Debug #print
                                #print(f"Demand remaining - MS: {ms_demand}, HSD: {hsd_demand}")  # Debug #print
                                # If demand is met, return df
                                if ms_demand == 0 and hsd_demand == 0:
                                    print("==========================================================================================================")
                                    print(f"Demand met for station {ms_station}")
                                    print("==========================================================================================================")
                                    df = df.append({'station_name': ms_station, 'trucks': trucks_used}, ignore_index=True)
                                    #print("=====================================================",df,"=====================================================")
                                    flag1 = True
                                    break
                            
                            # Fulfill hsd_demand if the ms_demand is quite higher
                            elif total_volume <= ms_demand and total_volume > hsd_demand:
                                # Determine how much MS and HSD can be loaded into the truck
                                hsd_in_truck = min(total_volume, hsd_demand)
                                ms_in_truck = total_volume - hsd_in_truck
                                ms_demand -= ms_in_truck
                                hsd_demand -= hsd_in_truck
                                trucks_used.append(truck_name)
                                truck_inventory_df.loc[index, 'No. of times used'] += 1
                                demands_met['MS'] += ms_in_truck
                                demands_met['HSD'] += hsd_in_truck
                                #print(f"Truck {truck_name} loaded with MS: {ms_in_truck}, HSD: {hsd_in_truck}")
                                #print(f"Demand remaining - MS: {ms_demand}, HSD: {hsd_demand}")
                                # If demand is met, return df
                                if ms_demand == 0 and hsd_demand == 0:
                                    print("==========================================================================================================")
                                    print(f"Demand met for station {ms_station}")
                                    print("==========================================================================================================")
                                    df = df.append({'station_name': ms_station, 'trucks': trucks_used}, ignore_index=True)
                                    #print("=====================================================",df,"=====================================================")
                                    flag1 = True
                                    break

                            # Fulfill ms_demand if the hsd_demand is quite higher                            
                            elif total_volume > ms_demand and total_volume <= hsd_demand:
                                # Determine how much MS and HSD can be loaded into the truck
                                ms_in_truck = min(total_volume, ms_demand)
                                hsd_in_truck = total_volume - ms_in_truck
                                ms_demand -= ms_in_truck
                                hsd_demand -= hsd_in_truck
                                trucks_used.append(truck_name)
                                truck_inventory_df.loc[index, 'No. of times used'] += 1
                                demands_met['MS'] += ms_in_truck
                                demands_met['HSD'] += hsd_in_truck
                                #print(f"Truck {truck_name} loaded with MS: {ms_in_truck}, HSD: {hsd_in_truck}")
                                #print(f"Demand remaining - MS: {ms_demand}, HSD: {hsd_demand}")
                                # If demand is met, return df
                                if ms_demand == 0 and hsd_demand == 0:
                                    print("==========================================================================================================")
                                    print(f"Demand met for station {ms_station}")
                                    print("==========================================================================================================")
                                    df = df.append({'station_name': ms_station, 'trucks': trucks_used}, ignore_index=True)
                                    #print("=====================================================",df,"=====================================================")
                                    flag1 = True
                                    break
                            
                            # Fulfill the remaining demands
                            elif total_volume >= ms_demand or total_volume >= hsd_demand and ms_demand+hsd_demand <= total_volume:
                                # Determine how much MS and HSD can be loaded into the truck
                                ms_in_truck = min(total_volume, ms_demand)
                                hsd_in_truck = min(total_volume, hsd_demand)
                                ms_demand -= ms_in_truck
                                hsd_demand -= hsd_in_truck
                                trucks_used.append(truck_name)
                                truck_inventory_df.loc[index, 'No. of times used'] += 1
                                demands_met['MS'] += ms_in_truck
                                demands_met['HSD'] += hsd_in_truck
                                #print(f"Truck {truck_name} loaded with MS: {ms_in_truck}, HSD: {hsd_in_truck}")  # Debug #print
                                #print(f"Demand remaining - MS: {ms_demand}, HSD: {hsd_demand}")  # Debug #print
                                # If demand is met, return df
                                if ms_demand == 0 and hsd_demand == 0:
                                    print("==========================================================================================================")
                                    print(f"Demand met for station {ms_station}")
                                    print("==========================================================================================================")
                                    print(trucks_used)
                                    print("==========================================================================================================")
                                    print('')
                                    print('')
                                    df = df.append({'station_name': ms_station, 'trucks': trucks_used}, ignore_index=True)
                                    #print("=====================================================",df,"=====================================================")
                                    flag1 = True
                                    break
                                
                            # Fulfill the remaining demands
                            elif total_volume >= ms_demand or total_volume >= hsd_demand and ms_demand+hsd_demand > total_volume:
                                if ms_demand > hsd_demand:
                                    ms_in_truck = total_volume
                                    hsd_in_truck = 0
                                elif hsd_demand > ms_demand:
                                    hsd_in_truck = total_volume
                                    ms_in_truck = 0
                                ms_demand -= ms_in_truck
                                hsd_demand -= hsd_in_truck
                                trucks_used.append(truck_name)
                                truck_inventory_df.loc[index, 'No. of times used'] += 1
                                demands_met['MS'] += ms_in_truck
                                demands_met['HSD'] += hsd_in_truck
                                #print(f"Truck {truck_name} loaded with MS: {ms_in_truck}, HSD: {hsd_in_truck}")
                                #print(f"Demand remaining - MS: {ms_demand}, HSD: {hsd_demand}")
                                # If demand is met, return df
                                if ms_demand == 0 and hsd_demand == 0:
                                    print("==========================================================================================================")
                                    print(f"Demand met for station {ms_station}")
                                    print("==========================================================================================================")
                                    df = df.append({'station_name': ms_station, 'trucks': trucks_used}, ignore_index=True)
                                    #print("=====================================================",df,"=====================================================")
                                    flag1 = True
                                    break
                            else:
                                print("Truck capacity insufficient")  # Debug #print
                    if flag1: 
                        break
                    if truck_name is None:
                        break  # No suitable truck found, exit loop
            
        # Update demand dictionaries after processing each station
        demand_dict['Demand of MS'][ms_station] = ms_demand
        demand_dict['Demand of HSD'][hsd_station] = hsd_demand
            
    # Update dataframe with trucks for one station
    df = df.append({'station_name': ms_station, 'trucks': trucks_used}, ignore_index=True)
    #print("=====================================================",df,"=====================================================")
    
    return df


def main():

    demand_df = pd.read_csv('demand.csv')
    truck_inventory_df = pd.read_csv('truck_inventory.csv')
    
    # Calculate truck combination
    df = calculate_truck_combination(demand_df, truck_inventory_df)

    # Save updated truck inventory
    truck_inventory_df.to_csv('truck_inventory_updated.csv', index=False)

    # Save truck used dataframe
    df.to_csv('truck_used.csv', index=False)
    #print("Truck combination calculated successfully")


if __name__ == "__main__":
    main()
