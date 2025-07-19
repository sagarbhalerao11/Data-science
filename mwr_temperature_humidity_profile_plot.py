import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict


#mpl.rcParams['toolbar'] = 'None' # or False


# Function to read MWR file and create structured dictionary
def read_mwr_file(filepath):
    #data_dict = defaultdict(lambda: {'height': [], 'temperature': [], 'humidity': []})
    data_dict = {
        'height': [],        # Only for the first timestamp
        'temperature': [],   # All temperatures
        'humidity': []       # All humidities
    }
    current_temp_list = []
    current_humidity_list = []
    #temperture_list = []
    time_list =[]
    height_list =[]
    first_timestamp = None  # To track the first timestamp
    previous_timestamp = None

    with open(filepath, 'r') as file:
        for line in file:
            #parts = line.strip().split()
            parts = line.split(',')
            #if len(parts) == 5 and "-" in parts[0]:  # Simple validation
            if "-" in parts[0]:  # Simple validation
                timestamp = parts[0] #+ " " + parts[1]
                height = float(parts[1])
                temperature = float(parts[2])
                humidity = float(parts[3])

                # Set first timestamp
                if first_timestamp is None:
                    first_timestamp = timestamp


                # Collect heights only for the first timestamp
                if timestamp == first_timestamp:
                    height_list.append(height)


                if not timestamp in time_list:
                    time_list.append(timestamp)

                # New timestamp: push previous group into lists
                if timestamp != previous_timestamp and previous_timestamp is not None:
                    data_dict['temperature'].append(current_temp_list)
                    current_temp_list = []
                    data_dict['humidity'].append(current_humidity_list)
                    current_humidity_list = []

                # Append current values
                current_temp_list.append(temperature)

                current_humidity_list.append(humidity)

                previous_timestamp = timestamp

    # Append the last group (for final timestamp)
    if current_temp_list:
        data_dict['temperature'].append(current_temp_list)
        data_dict['humidity'].append(current_humidity_list)

    return data_dict,time_list,height_list

def plot_temperature_and_humidity(times, heights, temperature_data, humidity_data, title, cmap, cbar_label,filename):
    plot_temperature(times, heights, temperature_data, filename)
    plot_humidity(times, heights, humidity_data, filename)


def plot_temperature(times, heights, temperature_data, filename):
    temperature_data = np.array(temperature_data).T  # Shape: [height x time]
    
    fig, ax = plt.subplots(figsize=(14, 3))

    filename = os.path.basename(filename)
    contour = ax.contourf(
        np.arange(len(times)), heights, temperature_data, levels=50, cmap='jet'
    )
    ax.set_ylabel("Height (m)")
    ax.set_xlabel("Time")
    ax.set_yticks([2000, 4000, 6000, 8000, 10000])
    #ax.set_title(f"Temperature Profile {filename}")
    #plt.colorbar(contour, ax=ax, label="Temperature (°C)")
    cbar = plt.colorbar(contour, ax=ax)
    cbar.ax.set_title("Temperature (°C)", fontsize=10, pad=10)  # Top label

    time_labels = times[::20]
    x_positions = np.arange(0, len(times), 20)
    ax.set_xticks(x_positions)
    ax.set_xticklabels(time_labels, rotation=45, ha='right', fontsize=8)


    plt.tight_layout()
    plt.show()

def plot_humidity(times, heights, humidity_data, filename):
    humidity_data = np.array(humidity_data).T
    humidity_data[humidity_data < 0] = np.nan

    fig, ax = plt.subplots(figsize=(14, 3))

    filename = os.path.basename(filename)
    contour = ax.contourf(
        np.arange(len(times)), heights, humidity_data, levels=50, cmap='jet'
    )
    ax.set_ylabel("Height (m)")
    ax.set_xlabel("Time")
    ax.set_yticks([2000, 4000, 6000, 8000, 10000])
    #ax.set_title(f"Humidity Profile {filename}")
    #plt.colorbar(contour, ax=ax, label="Humidity (%)")

    # Add colorbar and move label to top
    cbar = plt.colorbar(contour, ax=ax)
    cbar.ax.set_title("Humidity (%)", fontsize=10, pad=10)  # Top label

    time_labels = times[::20]
    x_positions = np.arange(0, len(times), 20)
    ax.set_xticks(x_positions)
    ax.set_xticklabels(time_labels, rotation=45, ha='right', fontsize=8)

    plt.tight_layout()
    plt.show()




def plot_temperature_and_humidity____(times, heights, temperature_data, humidity_data, title, cmap, cbar_label,filename):
    temperature_data = np.array(temperature_data).T  # Shape: [height x time]
    humidity_data = np.array(humidity_data).T        # Shape: [height x time]
    humidity_data[humidity_data < 0] = np.nan  # Set negative values to NaN


    fig, axs = plt.subplots(nrows=2, figsize=(14, 10), sharex=True)

    filename = os.path.basename(filename)  # Extracts '1MayDataL3.csv'
    # --- Temperature Plot ---
    temp_contour = axs[0].contourf(
        np.arange(len(times)), heights, temperature_data, levels=50, cmap='jet'
    )
    axs[0].set_ylabel("Height (m)")
    axs[0].set_title(f"Temperature Profile {filename}")

    
    #plt.clabel(temp_contour, inline=1, fontsize=10, colors="k")
    plt.colorbar(temp_contour, ax=axs[0], label="Temperature (°C)")

    # For cleaner x-tick display
    time_labels = times[::20]
    x_positions = np.arange(0, len(times), 20)

    # Temperature plot
    axs[0].set_xticks(x_positions)
    axs[0].set_xticklabels(time_labels, rotation=45, ha='right', fontsize=8)

    # Humidity plot
    axs[1].set_xticks(x_positions)
    axs[1].set_xticklabels(time_labels, rotation=45, ha='right', fontsize=8)

    # --- Humidity Plot ---
    hum_contour = axs[1].contourf(
        np.arange(len(times)), heights, humidity_data, levels=50, cmap='jet'
    )
    axs[1].set_xlabel("Time")
    axs[1].set_ylabel("Height (m)")
    axs[1].set_title(f"Humidity Profile {filename}")
    axs[1].set_xticks(range(len(times)))
    #axs[1].set_xticklabels(times, rotation=45, fontsize=8)
    plt.colorbar(hum_contour, ax=axs[1], label="Humidity (%)")

    plt.tight_layout()
    plt.show()


# Main execution
if __name__ == "__main__":
    #filepath = '/home/sagar/Desktop/radiometer_jULY/1MayDataL3.csv'  # <-- Change path if needed
    #filepath = '/home/sagar/Desktop/radiometer_jULY/10JulyDataL3.csv'  # <-- Change path if needed
    #filepath = '/home/sagar/Desktop/radiometer_jULY/14JuneDataL3.csv'  # <-- Change path if needed
    filepath = '/home/sagar/Desktop/radiometer_jULY/14MayDataL3.csv'  # <-- Change path if needed
    mwr_data,time_list,height_list = read_mwr_file(filepath)
    
    if not mwr_data:
        print("No valid data found.")
    else:
        #times, heights, temp_data, humid_data = prepare_2d_data(mwr_data)
        plot_temperature_and_humidity(time_list, height_list, mwr_data['temperature'],mwr_data['humidity'], title="Temperature Profile", cmap="jet", cbar_label="Temperature (°C)",filename=filepath)
