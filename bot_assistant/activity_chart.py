import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from collections import UserDict
from datetime import datetime, timedelta
import functools
import copy
import pickle

class Charts(UserDict):
    def __init__(self, chart_name) -> None:
        super().__init__()
        self.chart_name = chart_name
        self.default_values()
        
    def days_list(self):
        end = datetime.now()
        start = end - timedelta(days=30)
        date_of_range = [start + timedelta(days=delta) for delta in range((end - start).days + 1)]
        return date_of_range

    def default_values(self):
        for day in self.days_list():
            self.data[day.strftime('%d-%m')] = 0
    
    def add_point(self):
        today = datetime.now().strftime('%d-%m')
        try:
            self.data[today] += 1
        except KeyError:
            self.data[today] = 1
    
    # Autosave functions
    def load_from_file(self, file):
        try:
            with open(file, "rb") as fh:
                self.data = pickle.load(fh)
        except:
            return "The file with saved chart not found, corrupted or empty."

    def save_to_file(self, file):
        with open(file, "wb") as fh:
            pickle.dump(self.data, fh)


def update_chart(current_page_data, page_type, ax):
    ax.clear()
    ax.set_facecolor((0.8,0.8,0.8))

    bars = ax.bar(current_page_data['Days'], current_page_data['Values'])

    for bar in bars:
        bar.set_edgecolor('black')
        bar.set_facecolor('#EA6D20')
        bar.set_linewidth(1)
        bar.set_antialiased(True)

    if page_type == 'week':
        ax.set_title('Activity chart (week)')
    elif page_type == 'month':
        ax.set_title('Activity chart (month)')

def switch_page(event, data_dict, week_data, month_data, ax):
    if data_dict['current_page'] == 'month':
        data_dict['current_page'] = 'week'
        data_dict['current_data'] = copy.deepcopy(week_data)

    elif data_dict['current_page'] == 'week':
        data_dict['current_page'] = 'month'
        data_dict['current_data'] = copy.deepcopy(month_data)

    update_chart(data_dict['current_data'], data_dict['current_page'], ax)
    plt.draw()

def return_data(ch):
    week_data = {'Days': list(ch.data.keys())[-7:], 'Values': list(ch.data.values())[-7:]}
    month_data = {'Days': list(ch.data.keys())[-30:], 'Values': list(ch.data.values())[-30:]}
    return week_data, month_data

def set_font(ax):
    font = {'family': 'cursive',
        'weight': 'bold',
        'size': 8}
    
    plt.rc('font', **font)

    ax.tick_params(axis='x', labelrotation = 60)


def chart_main_func(ch):
    week_data, month_data = return_data(ch)
    current_data = {'current_page': 'week', 'current_data': week_data}

    fig, ax = plt.subplots(figsize=(10, 5))

    set_font(ax)

    update_chart(current_data['current_data'], current_data['current_page'], ax)
    

    button_ax = plt.axes([0.15, 0.89, 0.15, 0.05])
    button = Button(button_ax, 'Change time interval')


    button.on_clicked(functools.partial(switch_page, data_dict=current_data, week_data=week_data, month_data=month_data, ax=ax))
    plt.show()