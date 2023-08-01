import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
from main import get_status, get_device_list, send_command
from send_to_thingsbord import send_Thingsboard, send_Thingsboard_price
from mqtt_publisher import download_litgrid_data, download_litgrid_current

class DeviceGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        style = ttk.Style()
        style.configure('Custom.TFrame', background='blue', relief='raised')
        self.devices = [{'name': device['name'], 'id': device['id']} for device in get_device_list()]
        self.selected_device = None
        self.device_graphs = {}  # Stores the graph objects for each device
        self.data = {}  # Stores the device data
        
        self.title("Device Control")
        self.geometry("1920x1080")

        self.device_frame = ttk.Frame(self,style='Custom.TFrame')
        self.device_frame.pack(pady=20)

        self.device_label = ttk.Label(self.device_frame, text="Select Device:", font=("Helvetica", 14))
        self.device_label.pack(side=tk.LEFT)

        self.device_combobox = ttk.Combobox(self.device_frame, values=[device['name'] for device in self.devices], font=("Helvetica", 12))
        self.device_combobox.pack(side=tk.LEFT)

        self.value_label = ttk.Label(self, text="Selected Device Value:", font=("Helvetica", 14))
        self.value_label.pack(pady=10)

        self.value_display = ttk.Label(self, text="", font=("Helvetica", 12))
        self.value_display.pack()

        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(pady=20)

        self.on_button = ttk.Button(self.button_frame, text="Turn On", command=self.turn_on_device, width=12)
        self.on_button.grid(row=0, column=0, padx=10, sticky=tk.W)

        self.off_button = ttk.Button(self.button_frame, text="Turn Off", command=self.turn_off_device, width=12)
        self.off_button.grid(row=0, column=1, padx=10, sticky=tk.W)

        self.update_button = ttk.Button(self.button_frame, text="Update Graph", command=self.update_graph, width=12)
        self.update_button.grid(row=0, column=2, padx=10, sticky=tk.W)

        self.price_update_button = ttk.Button(self.button_frame, text="Price Update", command=self.price_update, width=12)
        self.price_update_button.grid(row=0, column=3, padx=10, sticky=tk.W)

        self.start_date_label = ttk.Label(self.button_frame, text="Start Date:", font=("Helvetica", 12))
        self.start_date_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        self.start_year_entry = ttk.Entry(self.button_frame, font=("Helvetica", 12), width=6)
        self.start_year_entry.grid(row=1, column=1, padx=2, pady=10, sticky=tk.W)

        self.start_month_entry = ttk.Entry(self.button_frame, font=("Helvetica", 12), width=4)
        self.start_month_entry.grid(row=1, column=2, padx=2, pady=10, sticky=tk.W)

        self.start_day_entry = ttk.Entry(self.button_frame, font=("Helvetica", 12), width=4)
        self.start_day_entry.grid(row=1, column=3, padx=2, pady=10, sticky=tk.W)

        self.end_date_label = ttk.Label(self.button_frame, text="End Date:", font=("Helvetica", 12))
        self.end_date_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

        self.end_year_entry = ttk.Entry(self.button_frame, font=("Helvetica", 12), width=6)
        self.end_year_entry.grid(row=2, column=1, padx=2, pady=10, sticky=tk.W)

        self.end_month_entry = ttk.Entry(self.button_frame, font=("Helvetica", 12), width=4)
        self.end_month_entry.grid(row=2, column=2, padx=2, pady=10, sticky=tk.W)

        self.end_day_entry = ttk.Entry(self.button_frame, font=("Helvetica", 12), width=4)
        self.end_day_entry.grid(row=2, column=3, padx=2, pady=10, sticky=tk.W)

        self.graph_frame = ttk.Frame(self)
        self.graph_frame.pack(pady=20)

        self.graph_canvas = None

        self.device_combobox.bind("<<ComboboxSelected>>", self.select_device)

        self.start_data_collection()

    def price_update(self):
        print("Sending price update message")

        # Get the entered start date components
        start_year = self.start_year_entry.get()
        start_month = self.start_month_entry.get()
        start_day = self.start_day_entry.get()

        # Get the entered end date components
        end_year = self.end_year_entry.get()
        end_month = self.end_month_entry.get()
        end_day = self.end_day_entry.get()

        # Perform action to send the price update message using the entered start date and end date components
        download_litgrid_data(start_year, start_month, start_day, end_year, end_month, end_day)
        
        # Optionally, update any display elements or perform additional actions after sending the message


    # Rest of the code remains the same
    def start_data_collection(self):
        self.after(60000, self.collect_device_data)
        

    def collect_device_data(self):
        for device in self.devices:
            device_id = device['id']
            device_name = device['name']
            value = get_status(device_id)
            price = download_litgrid_current()
            send_Thingsboard(value,device_id)
            send_Thingsboard_price(price,value,device_id)
            timestamp = time.strftime("%H:%M")
            if device_id not in self.data:
                self.data[device_id] = {'name': device_name, 'values': [(timestamp, value)]}
            else:
                self.data[device_id]['values'].append((timestamp, value))
        
        self.update_graph()
        self.start_data_collection()

    def select_device(self, event):
        device_name = self.device_combobox.get()
        self.selected_device = device_name
        device_id = self.devices[self.device_combobox.current()]['id']
        self.update_value_display(device_id)

        # Create or update the graph for the selected device
        self.update_device_graph(device_id)

    def turn_on_device(self):
        if self.selected_device:
            device_id = self.devices[self.device_combobox.current()]['id']
            print(f"Turning on device {device_id}")
            send_command(device_id,1)
            # Perform action to turn on the selected device
            # Add your code here

            # Update the value display if necessary
            self.update_value_display(device_id)

    def turn_off_device(self):
        if self.selected_device:
            device_id = self.devices[self.device_combobox.current()]['id']
            print(f"Turning off device {device_id}")
            # Perform action to turn off the selected device
            # Add your code here
# Update the value display if necessary
            send_command(device_id,0)
            # Update the value display if necessary
            self.update_value_display(device_id)

    def update_graph(self):
        if self.selected_device:
            device_id = self.devices[self.device_combobox.current()]['id']
            print(f"Updating graph for device {device_id}")
            self.update_value_display(device_id)

            # Update the graph for the selected device
            self.update_device_graph(device_id)

    def update_value_display(self, device_id):
        value = get_status(device_id)
        price = download_litgrid_current() # Replace with your function to get the price
        print ("price", price)
        calculated_value = value
        self.value_display.config(text=str(calculated_value))

    def update_device_graph(self, device_id):
        if device_id not in self.device_graphs:
            # Create a new graph for the device
            self.device_graphs[device_id] = plt.figure(figsize=(18.5, 10.5), dpi=90)

        plt.figure(self.device_graphs[device_id].number)
        plt.clf()  # Clear the previous graph content

        if device_id in self.data:
            device_data = self.data[device_id]
            device_name = device_data['name']
            values = device_data['values']
            timestamps, device_values = zip(*values)

            price = download_litgrid_current()  # Replace with your function to get the price
            calculated_device_values = [value for value in device_values]

            plt.plot(timestamps, calculated_device_values, 'b-')
            plt.xticks(rotation=45)

            plt.title(f"{device_name} Value Over Time", fontweight='bold', fontsize=14)
            plt.xlabel("Time", fontweight='bold', fontsize=12)
            plt.ylabel("Value", fontweight='bold', fontsize=12)

        self.update_device_graph_canvas(device_id)

    def update_device_graph_canvas(self, device_id):
        if device_id in self.device_graphs:
            graph_figure = self.device_graphs[device_id]
            
            if self.graph_canvas is not None:
                self.graph_canvas.get_tk_widget().destroy()
            
            self.graph_canvas = FigureCanvasTkAgg(graph_figure, master=self.graph_frame)
            self.graph_canvas.get_tk_widget().pack()

            self.graph_canvas.draw()

    def clear_device_graphs(self):
        for device_id, graph in self.device_graphs.items():
            plt.close(graph.number)
        self.device_graphs = {}


if __name__ == '__main__':
    app = DeviceGUI()
    app.mainloop()