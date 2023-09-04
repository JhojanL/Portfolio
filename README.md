# Energy Consumption Calculator

## Introduction
The Energy Consumption Calculator is a Python-based tool that allows users to measure the energy consumption of a specified application over a defined duration. This README provides an overview of the application, how to use it, and its functionalities.

## Usage
1. Run the application by executing the app_energy_calculator.py script.
1. Input the application name or PID that you want to measure.
1. Enter the duration (in seconds) for which you want to measure energy consumption.
1. Click the "Calculate" button.

The application will display real-time CPU and memory usage, as well as power consumption, in a table. After the specified duration, the total energy consumption will be displayed.

## Functionality
The Application Energy Consumption Calculator provides the following functionalities:

- Measure CPU and memory usage of a specified application.
- Calculate and display power consumption over a defined duration.
- Display real-time usage in a table format.

## Results and Output
The table displays the following information during the measurement:

- Time (s): Elapsed time in seconds.
- CPU Usage (%): Normalized CPU usage in percentage.
- Memory Usage (%): Memory usage of the application in percentage.
- Power Consumption (W): Estimated power consumption in Watts.

After the specified duration is reached, the application will display the total energy consumption of the application in Joules.

## Technical Details
The application uses the psutil library to monitor a specified application's CPU and memory usage. Power consumption is estimated using an average of CPU and memory usage. The GUI is built using the tkinter and ttk libraries.

## How to Run
### Terminal Version
In your terminal, `cd` into the `Tech_Test_Task` directory.
Then run the following commands:
```bash
pip install -r requirements.txt
python app_energy_calculator.py
```
### Executable Version
- Download the `app_ecc.exe` file from [Here](https://drive.google.com/file/d/1GWtoD8LdB7puclEQZfjLeeYkoZugrBGC/view?usp=sharing).
- Double-click on the `app_ecc.exe` file to run the application.
- If you see a warning message like "Windows protected your PC" or "Windows SmartScreen prevented an unrecognized app from starting." Despite the warning, the "More info" option usually allows the user to proceed and run the application.

## Additional Information
- The application was developed and tested on a Windows 10 machine. It is not guaranteed to work on other operating systems.
- The application was developed and tested using Python 3.10. It is not guaranteed to work on other versions of Python.

## Images
![image](https://drive.google.com/uc?id=1smF3xxDv9BY7pe_OCr04w70nZgrcwVnr)

![image](https://drive.google.com/uc?id=1ofggw3Fu8eRXt9atZwrGpSGJIA4cwTti)
