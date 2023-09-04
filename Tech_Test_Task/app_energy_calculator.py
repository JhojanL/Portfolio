import tkinter as tk
from tkinter import ttk
import psutil

def get_application_energy_consumption(app_name, duration, table, result_label_widget):
    proc = next((p for p in psutil.process_iter(attrs=['pid', 'name'])
                 if app_name.lower() in p.info['name'].lower() or app_name == str(p.info['pid'])), None)
    
    if proc:
        for seconds in range(1, duration + 1):
            # Schedule the next update after 1 second
            root.after(1000 * seconds, update_display, app_name, table, result_label_widget)
    else:
        result_label['text'] = "No matching process found.\n"


def update_display(app_name, table, result_label_widget):
    seconds = root.after_info['seconds']
    energy_consumption = 0  # Total energy consumption in Joules
    if seconds <= duration:
        # Get the CPU and memory usage for the current application
        proc = next((p for p in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_percent'])
                     if app_name.lower() in p.info['name'].lower() or app_name == str(p.info['pid'])), None)

        cpu_usage = proc.info['cpu_percent'] / psutil.cpu_count()  # Normalize the CPU usage
        memory_usage = proc.info['memory_percent']

        # Calculate the power consumption in Watts (average of CPU and memory)
        power_consumption = (cpu_usage + memory_usage) / 2

        # Update the table, make sure that the values have at most 2 decimal places
        table.insert(parent = '', index = 0, values=(seconds, f"{cpu_usage:.2f}", f"{memory_usage:.2f}", f"{power_consumption:.2f}"))
        root.after_info['seconds'] += 1

    if seconds == duration:
        name = proc.info['name']
        pid = proc.info['pid']

        # Select all the values of the column 'Power Consumption' and sum them up
        for child in table.get_children():
            energy_consumption += float(table.item(child)['values'][3])

        result_label_widget['text'] = f"\nTotal energy consumption of {name} (PID:{pid}) over {duration} seconds: {energy_consumption:.2f} J\n"

def calculate_energy():
    app_name = app_name_entry.get()
    global duration  # Make 'duration' a global variable
    duration = int(duration_entry.get())
    table.delete(*table.get_children())  # Clear existing table
    result_label['text'] = '' # Clear existing result label
    root.after_info = {'seconds': 1}
    get_application_energy_consumption(app_name, duration, table, result_label)


root = tk.Tk()
root.title("Energy Consumption Calculator")

app_name_label = tk.Label(root, text="Application Name/PID:", font=("Arial", 10, "bold"))
app_name_entry = tk.Entry(root)
duration_label = tk.Label(root, text="Duration (seconds):", font=("Arial", 10, "bold"))
duration_entry = tk.Entry(root)
calculate_button = tk.Button(root, text="Calculate", command=calculate_energy, font=("Arial", 10, "bold"), bg="green", fg="white", padx=10, pady=5, borderwidth=3, relief=tk.RAISED)
table = ttk.Treeview(root, columns=('Time','CPU Usage', 'Memory Usage', 'Power Consumption'), show='headings', height=10)
table.heading('Time', text='Time (s)')
table.heading('CPU Usage', text='CPU Usage (%)')
table.heading('Memory Usage', text='Memory Usage (%)')
table.heading('Power Consumption', text='Power Consumption (W)')
# Center text in the table
table.column('Time', anchor=tk.CENTER)
table.column('CPU Usage', anchor=tk.CENTER)
table.column('Memory Usage', anchor=tk.CENTER)
table.column('Power Consumption', anchor=tk.CENTER)
# Scrollbar for the table
scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=table.yview)
table.configure(yscroll=scrollbar.set)
scrollbar.grid(row=4, column=2, sticky='ns')

result_label = tk.Label(root, text="", font=("Arial", 10, "bold"))
creator_label = tk.Label(root, text="Created by: Jhojan Lerma", font=("Arial", 8, "italic"))

app_name_label.grid(row=0, column=0)
app_name_entry.grid(row=0, column=1)
duration_label.grid(row=1, column=0)
duration_entry.grid(row=1, column=1)
calculate_button.grid(row=2, columnspan=2)
# Blank row
tk.Label(root, text="").grid(row=3, columnspan=2)
table.grid(row=4, columnspan=2)
result_label.grid(row=5, columnspan=2)
creator_label.grid(row=6, columnspan=2)

root.mainloop()