"""Caleb Cano — CSD-325 Module 4.

Changes from sitka_highs.py:
* Added startup instructions and a repeating Highs/Lows/Exit menu.
* Read TMIN along with TMAX, using CSV field names for clarity.
* Added separate plotting function: highs are red and lows are blue.
* Return to the menu after the graph window closes; reject invalid choices.
* Resolve the CSV beside this script, regardless of the working directory.
* Added an exit message and a main guard with sys.exit().
"""
import csv
import sys
from datetime import datetime
from pathlib import Path

from matplotlib import pyplot as plt


def load_weather(filename):
    """Read matching dates, high temperatures, and low temperatures."""
    dates, highs, lows = [], [], []
    with open(filename, newline='', encoding='utf-8') as weather_file:
        reader = csv.DictReader(weather_file)
        for row in reader:
            dates.append(datetime.strptime(row['DATE'], '%Y-%m-%d'))
            highs.append(int(row['TMAX']))
            lows.append(int(row['TMIN']))
    return dates, highs, lows


def show_temperatures(dates, temperatures, selection):
    """Display the selected graph and wait until its window closes."""
    color = 'red' if selection == 'highs' else 'blue'
    fig, ax = plt.subplots()
    ax.plot(dates, temperatures, c=color)
    ax.set_title(f'Daily {selection} temperatures - 2018', fontsize=24)
    ax.set_xlabel('', fontsize=16)
    ax.set_ylabel('Temperature (F)', fontsize=16)
    ax.tick_params(axis='both', which='major', labelsize=16)
    fig.autofmt_xdate()
    fig.tight_layout()
    plt.show(block=True)
    plt.close(fig)


def main():
    """Keep displaying the menu until the user chooses Exit."""
    print('Welcome to the Sitka 2018 temperature viewer!')
    print('Type Highs for daily high temperatures, Lows for daily lows,')
    print('or Exit to quit. Close the graph window to return to the menu.')
    filename = Path(__file__).with_name('sitka_weather_2018_simple.csv')
    dates, highs, lows = load_weather(filename)

    while True:
        selection = input('\nChoose Highs, Lows, or Exit: ').strip().lower()
        if selection == 'exit':
            print('Thank you for using the Sitka temperature viewer. Goodbye!')
            return 0
        elif selection == 'highs':
            show_temperatures(dates, highs, selection)
        elif selection == 'lows':
            show_temperatures(dates, lows, selection)
        else:
            print('Invalid selection. Please enter Highs, Lows, or Exit.')


if __name__ == '__main__':
    sys.exit(main())
