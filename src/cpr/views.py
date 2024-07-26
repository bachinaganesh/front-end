from django.shortcuts import render
from .forms import CPRForm
import psycopg2
import pandas as pd
from threading import *
import os
from datetime import datetime, timedelta
import time
import csv
import numpy as np
from utilities.constants.CPRConstants import CPRConstants
from nd_range_breakout.ndrange.nd_range import TimeStampConvertor
from utilities.visualizer.plotting_chart import DataFetching, ChartPlotting
from utilities.trades.trade import Trade, Line, Symbol
import json
from utilities.visualizer import plotting_chart
from utilities.conversions.convert import round_to_nearest_0_05
from .form_handling import CPRFormData
from utilities.fetchingdata.fetchdata import FetchingData
from utilities.connection.dbconnection import DBConnector
from utilities.strikes.get_strike import ATMStrikePrice


class ReportGeneration:
    @staticmethod
    def create_base_folder():
        if not os.path.exists('./cpr/reports'):
            os.mkdir('./cpr/reports')

    def create_timestamp_folder(timestamp):
        if not os.path.exists(f'./cpr/reports/{timestamp}'):
            os.mkdir(f'./cpr/reports/{timestamp}')
    
    def create_expiry_date_folder(timestamp, expiry_date):
        if not os.path.exists(f'./cpr/reports/{timestamp}/{expiry_date}'):
            os.mkdir(f'./cpr/reports/{timestamp}/{expiry_date}')
    
    @staticmethod
    def generate_report(timestamp, expiry_date, dict_data):
        ReportGeneration.create_base_folder()
        ReportGeneration.create_timestamp_folder(timestamp)
        ReportGeneration.create_expiry_date_folder(timestamp, expiry_date)

        
        file_exists = os.path.isfile(f'./cpr/reports/{timestamp}/{expiry_date}/output.csv')
        with open(f'./cpr/reports/{timestamp}/{expiry_date}/output.csv', 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=dict_data.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(dict_data)
    
    @staticmethod
    def create_directory():
        """
        This function is used create a new directory if it not exists
        :return: It returns None Value
        """
        if not os.path.exists('./cpr/reports'):
            os.mkdir('./cpr/reports')

    @staticmethod
    def extended_trade_report(report_base_folder, report_content, expiry_date):
        """
        :param report:
        :return:
        """
        ReportGeneration.create_directory()
        if not os.path.exists(f'./cpr/reports/{report_base_folder}'):
            os.mkdir(f'./cpr/reports/{report_base_folder}')
        expiry_date = expiry_date.strftime('%Y-%m-%d')
        file_name = f'{expiry_date}.json'
        if os.path.exists(f'./cpr/reports/{report_base_folder}/{file_name}'):
            with open(f'./cpr/reports/{report_base_folder}/{file_name}', 'r') as file:
                data = json.load(file)
            
            with open(f'./cpr/reports/{report_base_folder}/{file_name}', 'w') as file:
                data.update(report_content)
                json.dump(data, file, indent=2)
        else:
            with open(f'./cpr/reports/{report_base_folder}/{file_name}', 'w') as file:
                json.dump(report_content, file, indent=2)
    
    @staticmethod
    def generate_single_report(report_base_folder, extended_file_name):
        try:
            if not os.path.exists(f'./cpr/reports/{report_base_folder}/{extended_file_name}'):
                with open(f'./cpr/reports/{report_base_folder}/extended_trade_report.json', 'w') as file:
                    json.dump({}, file, indent=2)
            for filename in sorted(os.listdir(f'./cpr/reports/{report_base_folder}')):
                if filename != 'extended_trade_report.json':
                    with open(f'./cpr/reports/{report_base_folder}/{filename}', 'r') as file:
                        data = json.load(file)
                        os.remove(f'./cpr/reports/{report_base_folder}/{filename}')
                    with open(f'./cpr/reports/{report_base_folder}/{extended_file_name}', 'r') as file:
                        new_data = json.load(file)
                        new_data.update(data)
                    with open(f'./cpr/reports/{report_base_folder}/{extended_file_name}', 'w') as file:
                        json.dump(new_data, file, indent=2)
        except Exception as e:
            print(f'No Folder Found {e}')

class NewReportGeneration:
    @staticmethod
    def create_directory():
        """
        This function is used create a new directory if it not exists
        :return: It returns None Value
        """
        if not os.path.exists('./cpr/reports'):
            os.mkdir('./cpr/reports')

    @staticmethod
    def generate_json_report(base_folder, content, expiry_date):
        NewReportGeneration.create_directory()
        if not os.path.exists(f'./cpr/reports/{base_folder}'):
            os.mkdir(f'./cpr/reports/{base_folder}')
        expiry_date = expiry_date.strftime('%Y-%m-%d')
        file_name = f'{expiry_date}.json'
        if not os.path.exists(f'./cpr/reports/{base_folder}/{file_name}'):
            with open(f'./cpr/reports/{base_folder}/{file_name}', 'w') as json_file:
                json_file.write(json.dumps([content], indent=4))
        else:
            with open(f'./cpr/reports/{base_folder}/{file_name}', 'r+') as json_file:
                data = json.load(json_file)
                data.append(content)
                json_file.seek(0)  # Reset file pointer to the beginning
                json_file.write(json.dumps(data, indent=4))
                json_file.truncate()

    @staticmethod
    def generate_extended_trade_report(base_folder, extended_file_name):
        try:
            combined_data = []

            # Path to the extended report file
            extended_file_path = f'./cpr/reports/{base_folder}/{extended_file_name}'

            # Check if the extended report file exists, create it if it doesn't
            if not os.path.exists(extended_file_path):
                with open(extended_file_path, 'w') as file:
                    json.dump([], file, indent=2)

            # Iterate over all JSON files in the specified folder
            for filename in sorted(os.listdir(f'./cpr/reports/{base_folder}')):
                file_path = os.path.join(f'./cpr/reports/{base_folder}', filename)
                
                # Skip the extended report file itself
                if filename != extended_file_name and filename.endswith('.json'):
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        combined_data.extend(data)
                    
                    # Remove the file after reading its content
                    os.remove(file_path)

            # Write the combined data to the extended report file
            with open(extended_file_path, 'w') as file:
                json.dump(combined_data, file, indent=2)
                
        except Exception as e:
            print(f'No Folder Found: {e}')

    @staticmethod
    def generate_error_report(expiry_date, time_stamp, content):
        # create a base directory "report"
        NewReportGeneration.create_directory()
        # create an identical timestamp for every run strategy
        if not os.path.exists(f'./cpr/reports/{time_stamp}'):
            os.mkdir(f'./cpr/reports/{time_stamp}') 
        # create a folder based on expiry date it store all related error info
        if not os.path.exists(f'./cpr/reports/{time_stamp}/{expiry_date}'):
            os.mkdir(f'./cpr/reports/{time_stamp}/{expiry_date}')
        
        file_name = 'error.json'

        if not os.path.exists(f'./cpr/reports/{time_stamp}/{expiry_date}/{file_name}'):
            with open(f'./cpr/reports/{time_stamp}/{expiry_date}/{file_name}', 'w') as json_file:
                json_file.write(json.dumps([content], indent=4))
        else:
            with open(f'./cpr/reports/{time_stamp}/{expiry_date}/{file_name}', 'r+') as json_file:
                data = json.load(json_file)
                data.append(content)
                json_file.seek(0)  # Reset file pointer to the beginning
                json_file.write(json.dumps(data, indent=4))
                json_file.truncate()


class CPR:
    def __init__(self, cpr_form_data, timestamp) -> None:
        self.from_date = cpr_form_data.from_date
        self.to_date = cpr_form_data.to_date
        self.long_choices = cpr_form_data.long_choices
        self.short_choices = cpr_form_data.short_choices
        self.long_signal = cpr_form_data.long_signal
        self.short_signal = cpr_form_data.short_signal
        self.exit_time = cpr_form_data.exit_time
        self.trailing_values = [cpr_form_data.trailing_type, cpr_form_data.x, cpr_form_data.y]
        self.timestamp = timestamp
        self.cpr_range = cpr_form_data.cpr_range

    def start(self):
        self.t_expires = []
        for expiry_date, start_date in DBConnector.get_expiry_list(self.from_date, self.to_date):
            t = Thread(target=self.execute, args=(start_date, expiry_date))
            t.start()
            self.t_expires.append(t)
        for t in self.t_expires:
            t.join()

    def create_extended_report(self):
        NewReportGeneration.generate_extended_trade_report(self.timestamp, 'extended_trade_report.json')
    
    def get_extended_report_data(self):
        if os.path.exists(f'./cpr/reports/{self.timestamp}/extended_trade_report.json'):
            with open(f'./cpr/reports/{self.timestamp}/extended_trade_report.json', 'r') as file:
                data = json.load(file)
        return [data, self.timestamp]
    
    def execute(self, start_date, expiry_date):
        if expiry_date.year == self.from_date.year and expiry_date.month == self.from_date.month:
            fetch_date = self.from_date - timedelta(days=5)
            data_frame = FetchingData.fetch_data(fetch_date, expiry_date, self.to_date)
            return self.run(self.from_date, expiry_date, data_frame)
        else:
            fetch_date = start_date - timedelta(days=5)
            data_frame = FetchingData.fetch_data(fetch_date, expiry_date, self.to_date)
            return self.run(start_date, expiry_date, data_frame)

    def run(self, start_date, expiry_date, data_frame):
        data_frame = self.calculate_cpr(data_frame)
        data_frame.reset_index(inplace=True)
        data_frame = data_frame[data_frame['datetime'].dt.date>=start_date]
        return self.execute_strategy(expiry_date, data_frame)
    
    def calculate_cpr(self, data_frame):
        # calculate the cpr values
        data_frame['pivot'] = (data_frame['y_high'] + data_frame['y_low'] + data_frame['y_close']) / 3
        # data_frame['bcp_temp'] = (data_frame['y_high'] + data_frame['y_low']) / 2
        # data_frame['tcp_temp'] = (data_frame['pivot'] - data_frame['bcp_temp']) + data_frame['pivot']
        # data_frame['bcp'] = None
        # data_frame['tcp'] = None
        # data_frame.loc[data_frame['tcp_temp'] < data_frame['bcp_temp'], 'tcp'] = data_frame['bcp_temp']
        # data_frame.loc[data_frame['bcp_temp'] > data_frame['tcp_temp'], 'bcp'] = data_frame['tcp_temp']
        # data_frame.drop(columns=['tcp_temp', 'bcp_temp'], inplace=True)
        data_frame['bcp'] = abs((data_frame['y_high'] + data_frame['y_low']) / 2)
        data_frame['tcp'] = abs((data_frame['pivot'] - data_frame['bcp']) + data_frame['pivot'])
        data_frame['trading_day'] = (data_frame['tcp'] - data_frame['bcp']) < (float(self.cpr_range) * data_frame['bcp'])
        return data_frame
    
    def get_atm_strike(self, price, points, difference):
        """
        Calculate the atm strike based on price
        """
        price = (price // difference) * difference
        return price + int(points[0])*difference

    def classify_type(self, index, data_frame):
        """
        classify the open type based on first candle of every day
        """
        if data_frame.loc[index, 'open'] < data_frame.loc[index, 'y_high'] and data_frame.loc[index, 'open'] > data_frame.loc[index, 'y_low'] and data_frame.loc[index, 'close'] < data_frame.loc[index, 'y_high'] and data_frame.loc[index, 'close'] > data_frame.loc[index, 'y_low']:
            return CPRConstants.inside
        elif data_frame.loc[index, 'open'] > data_frame.loc[index, 'y_high'] and data_frame.loc[index, 'close'] > data_frame.loc[index, 'y_high']:
            return CPRConstants.above
        elif data_frame.loc[index, 'open'] < data_frame.loc[index, 'y_low'] and data_frame.loc[index, 'close'] < data_frame.loc[index, 'y_low']:
            return CPRConstants.below
    
    def check_range_breakout(self, open, high, low, close, range_high, range_low):
        """
        checks whether the candle value performs the range breakout or not
        """
        if close > range_high and open <= range_high:
            return "Long Signal"
        elif close < range_low and open >= range_low:
            return "Short Signal"
        else:
            return None
    
    def validate_options_data(self, options_data, entry_time, signal_price, atm_strike, option_type, expiry_date):
        # validate options data if it is not available return -1 else return entry_price
        if options_data is not None:
            options_data.reset_index(inplace=True)
            try:
                entry_price = options_data.loc[options_data['datetime'] == entry_time, 'close'].values[0]
                if np.isnan(entry_price):
                    raise Exception("Entry Price is Nan")
                else:
                    return entry_price
            except Exception as e:
                data = {'Datetime': entry_time.strftime('%Y-%m-%d %H:%M:%S'), 'Signal Price': signal_price,
                        'ATM Strike': atm_strike, 'Option_type': option_type}
                NewReportGeneration.generate_error_report(expiry_date, self.timestamp, data)
                return -1
        else:
            return -1
    
    def selecting_strike(self, is_trade, signal_price, expiry_date):
        # get the options_data, contract_name. atm_strike, trade_type(Buy, Sell) and option_type(CE or PE)
        if self.long_signal == "long call" or self.short_signal == "long call" or self.long_signal == "long put" or self.short_signal == "long put":
            trade_type = "Buy"
        elif self.long_signal == "short call" or self.short_signal == "short call" or self.long_signal == "short put" or self.short_signal == "short put":
            trade_type = "Sell"
        if is_trade == "Long Signal":
            atm_points_value = self.long_choices[0]
            option_type = 'CE'
        elif is_trade == "Short Signal":
            atm_points_value = self.short_choices[0]
            option_type = 'PE'

        atm_strike = ATMStrikePrice.get_atm_price(signal_price, atm_points_value, 50)
        options_data, contract_name = FetchingData.fetch_options_data(atm_strike, '5min', option_type, expiry_date)
        return (options_data, contract_name, trade_type, atm_strike, option_type)


    def execute_strategy(self, expiry_date, data_frame):
        # execute the cpr strategy of entire dataframe
        is_buy = False
        is_sell = False
        data_frame.reset_index(inplace=True)
        is_start_day = True
        is_cpr_above = False
        trade_list = []
        for i in range(len(data_frame)):
            # by default first candle of dataframe is new day candle
            if is_start_day:
                previous_date = data_frame.loc[i, 'datetime'].date()
                is_start_day =  False
                opening_type = self.classify_type(i, data_frame)
                if opening_type != CPRConstants.above and opening_type != CPRConstants.below:
                    continue
            # check the previous candle and current candle dates are different date or not
            elif previous_date != data_frame.loc[i, 'datetime'].date():
                opening_type = self.classify_type(i, data_frame)
                previous_date = data_frame.loc[i, 'datetime'].date()
                if opening_type != CPRConstants.above and opening_type != CPRConstants.below:
                    continue
            # check the candle is greater than exit time
            if data_frame.loc[i, 'datetime'].time() > datetime.strptime(self.exit_time, '%H:%M').time():
                continue
            if not (is_buy or is_sell):
                if opening_type == CPRConstants.inside:
                    is_trade = self.check_range_breakout(data_frame.loc[i, 'open'], data_frame.loc[i, 'high'], data_frame.loc[i, 'low'], data_frame.loc[i, 'close'], data_frame.loc[i, 'y_high'], data_frame.loc[i, 'y_low'])
                    if is_trade is not None:
                        signal_price = data_frame.loc[i, 'close']
                        entry_time = data_frame.loc[i, 'datetime']
                        
                        options_data, contract_name, trade_type, atm_strike, option_type = self.selecting_strike(is_trade, signal_price, expiry_date)

                        entry_price = self.validate_options_data(options_data, entry_time, signal_price, atm_strike, option_type, expiry_date)

                        if entry_price != -1:
                            if trade_type == "Buy":
                                is_buy = True
                                initial_stop_loss = entry_price - self.trailing_values[1]
                            else:
                                is_sell = True
                                initial_stop_loss = entry_price + self.trailing_values[1]
                            stop_loss = initial_stop_loss

                        if is_buy or is_sell:
                            trade = Trade()
                            symbol = Symbol("Entry Point")
                            symbol.x = entry_time.strftime('%Y-%m-%d %H:%M:%S')
                            symbol.y = signal_price
                            symbol.color = "green"
                            trade.symbols.append(symbol)
                            trade.symbol = "NIFTY"
                            trade.instrument_type = "FUT"
                            trade.contract_name = contract_name
                            tsl = Line('tsl')
                            trade.trade_type = is_trade
                            tsl.x.append(entry_time.strftime('%Y-%m-%d %H:%M:%S'))
                            tsl.y.append(stop_loss)

                            cpr_high = data_frame.loc[i, 'y_high']
                            cpr_low = data_frame.loc[i, 'y_low']

                            y_high_line = Line("Y_High")
                            y_high_line.x.append(datetime.combine(entry_time.date(), datetime.strptime("09:15", '%H:%M').time()).strftime('%Y-%m-%d %H:%M:%S'))
                            y_high_line.x.append(datetime.combine(entry_time.date(), datetime.strptime(self.exit_time, '%H:%M').time()).strftime('%Y-%m-%d %H:%M:%S'))
                            y_high_line.y.append(cpr_high)
                            y_high_line.y.append(cpr_high)
                            y_high_line.color = "green"

                            y_low_line = Line("Y_Low")
                            y_low_line.x.append(datetime.combine(entry_time.date(), datetime.strptime("09:15", '%H:%M').time()).strftime('%Y-%m-%d %H:%M:%S'))
                            y_low_line.x.append(datetime.combine(entry_time.date(), datetime.strptime(self.exit_time, '%H:%M').time()).strftime('%Y-%m-%d %H:%M:%S'))
                            y_low_line.y.append(cpr_low)
                            y_low_line.y.append(cpr_low)
                            y_low_line.color = "red"

                # elif opening_type == CPRConstants.above:
                #     if not is_cpr_above:
                #         cpr_high = data_frame.loc[i, 'high']
                #         cpr_low = data_frame.loc[i, 'low']
                #         is_cpr_above = True
                #         continue
                #     else:
                #         result = {}
                #         is_trade = self.check_range_breakout(data_frame.loc[i, 'open'], data_frame.loc[i, 'high'], data_frame.loc[i, 'low'], data_frame.loc[i, 'close'], cpr_high, cpr_low)
                #         if is_trade is not None:
                #             tsl = Line('tsl')
                #             trade = Trade()
                #             trade.symbol = "NIFTY"
                #             trade.instrument_type = "FUT"
                #             atm_strike = ATMStrikePrice.get_atm_price(entry_price, self.short_choices[0], 50)
                #             if is_trade == 'Buy':
                #                 initial_stop_loss = cpr_low
                #                 stop_loss = initial_stop_loss
                #                 is_buy = True
                #             else:
                #                 initial_stop_loss = cpr_high
                #                 stop_loss = initial_stop_loss
                #                 is_sell = True
                            
                #             trade.trade_type = is_trade
                #             entry_price = data_frame.loc[i, 'close']
                #             entry_time = data_frame.loc[i, 'datetime']
                #             tsl.x.append(entry_time.strftime('%Y-%m-%d %H:%M:%S'))
                #             tsl.y.append(stop_loss)
            else:
                if data_frame.loc[i, 'datetime'].time() == datetime.strptime(self.exit_time, '%H:%M').time():
                    # exit_price = data_frame.loc[i, 'close']
                    exit_time = data_frame.loc[i, 'datetime']
                    exit_price = options_data.loc[options_data['datetime'] == exit_time, 'close'].values[0]
                    if not np.isnan(exit_price):
                        if is_buy or is_sell:
                            trade.set_entry_price(entry_price)
                            trade.set_exit_price(exit_price)
                            tsl.x.append(exit_time.strftime('%Y-%m-%d %H:%M:%S'))
                            tsl.y.append(stop_loss)

                            trade.set_date_time(entry_time.strftime('%Y-%m-%d %H:%M:%S'))
                            trade.set_entry_time(entry_time.strftime('%Y-%m-%d %H:%M:%S'))
                            trade.set_exit_time(exit_time.strftime('%Y-%m-%d %H:%M:%S'))
                            if is_buy:
                                pl = float(round_to_nearest_0_05(trade.exit_price - trade.entry_price))
                            else:
                                pl = float(round_to_nearest_0_05(trade.entry_price - trade.exit_price))
                            trade.pl = pl

                            entry_line = Line('entry_line')
                            entry_line.x.append(entry_time.strftime('%Y-%m-%d %H:%M:%S'))
                            entry_line.x.append(exit_time.strftime('%Y-%m-%d %H:%M:%S'))
                            entry_line.y.append(entry_price)
                            entry_line.y.append(entry_price)
                            entry_line.color = "green"

                            exit_line = Line('exit_line')
                            exit_line.x.append(entry_time.strftime('%Y-%m-%d %H:%M:%S'))
                            exit_line.x.append(exit_time.strftime('%Y-%m-%d %H:%M:%S'))
                            exit_line.y.append(exit_price)
                            exit_line.y.append(exit_price)
                            exit_line.color = "red"
                            
                            symbol = Symbol("Exit Point")
                            symbol.x = exit_time.strftime('%Y-%m-%d %H:%M:%S')
                            symbol.y = data_frame.loc[i, 'close']
                            symbol.color = "red"
                            trade.symbols.append(symbol)

                            trade.lines.append(entry_line)
                            trade.lines.append(exit_line)
                            trade.lines.append(tsl)
                            trade.lines.append(y_high_line)
                            trade.lines.append(y_low_line)
                            trade_list.append(trade)
                    else:
                        if is_buy:
                            option_type = 'CE'
                        if is_sell:
                            option_type = 'PE'
                        data = {'Datetime': exit_time.strftime('%Y-%m-%d %H:%M:%S'), 'Signal Price': signal_price,
                        'ATM Strike': atm_strike, 'Option_type': option_type}
                        NewReportGeneration.generate_error_report(expiry_date, self.timestamp, data)
                    
                    is_buy = False
                    is_sell = False
                    is_cpr_above = False

                else:
                    if is_buy:
                        current_price = options_data.loc[options_data['datetime'] == data_frame.loc[i, 'datetime'], 'low'].values[0]
                        if not np.isnan(current_price):
                            if current_price <= stop_loss:
                                exit_price = stop_loss
                                exit_time = data_frame.loc[i, 'datetime']
                                if is_buy:
                                    tsl.x.append(exit_time.strftime('%Y-%m-%d %H:%M:%S'))
                                    tsl.y.append(stop_loss)
                                    trade.set_date_time(entry_time.strftime('%Y-%m-%d %H:%M:%S'))
                                    trade.set_entry_price(entry_price)
                                    trade.set_exit_price(exit_price)
                                    trade.set_entry_time(entry_time.strftime('%Y-%m-%d %H:%M:%S'))
                                    trade.set_exit_time(exit_time.strftime('%Y-%m-%d %H:%M:%S'))
                                    trade.pl = float(round_to_nearest_0_05(trade.exit_price - trade.entry_price))

                                    entry_line = Line('entry_line')
                                    entry_line.x.append(entry_time.strftime('%Y-%m-%d %H:%M:%S'))
                                    entry_line.x.append(exit_time.strftime('%Y-%m-%d %H:%M:%S'))
                                    entry_line.y.append(entry_price)
                                    entry_line.y.append(entry_price)
                                    entry_line.color = "green"

                                    exit_line = Line('exit_line')
                                    exit_line.x.append(entry_time.strftime('%Y-%m-%d %H:%M:%S'))
                                    exit_line.x.append(exit_time.strftime('%Y-%m-%d %H:%M:%S'))
                                    exit_line.y.append(exit_price)
                                    exit_line.y.append(exit_price)
                                    exit_line.color = "red"

                                    symbol = Symbol("Exit Point")
                                    symbol.x = exit_time.strftime('%Y-%m-%d %H:%M:%S')
                                    symbol.y = data_frame.loc[i, 'close']
                                    symbol.color = "red"
                                    trade.symbols.append(symbol)

                                    trade.lines.append(entry_line)
                                    trade.lines.append(exit_line)
                                    trade.lines.append(tsl)
                                    trade.lines.append(y_high_line)
                                    trade.lines.append(y_low_line)
                                    trade_list.append(trade)
                                is_buy = False
                                is_cpr_above = False
                            # ReportGeneration.extended_trade_report(self.timestamp, result, expiry_date)
                            else:
                                # TODO: Trading stop loss logic
                                # current_price = data_frame.loc[i, 'close']
                                diff = current_price - entry_price
                                if diff >= self.trailing_values[1]:
                                    increase_times = diff // self.trailing_values[1]
                                    new_stop_loss = (increase_times * self.trailing_values[2]) + initial_stop_loss
                                    if new_stop_loss > stop_loss:
                                        tsl.x.append(data_frame.loc[i, 'datetime'].strftime('%Y-%m-%d %H:%M:%S'))
                                        tsl.x.append(data_frame.loc[i, 'datetime'].strftime('%Y-%m-%d %H:%M:%S'))
                                        tsl.y.append(stop_loss)
                                        tsl.y.append(new_stop_loss)
                                        stop_loss = new_stop_loss
                    if is_sell:
                        current_price = options_data.loc[options_data['datetime'] == data_frame.loc[i, 'datetime'], 'high'].values[0]
                        if not np.isnan(current_price):
                            if current_price >= stop_loss:
                                exit_price = stop_loss
                                exit_time = data_frame.loc[i, 'datetime']

                                if is_sell:
                                    tsl.x.append(exit_time.strftime('%Y-%m-%d %H:%M:%S'))
                                    tsl.y.append(stop_loss)
                                    trade.set_date_time(entry_time.strftime('%Y-%m-%d %H:%M:%S'))
                                    trade.set_entry_price(entry_price)
                                    trade.set_exit_price(exit_price)
                                    trade.set_entry_time(entry_time.strftime('%Y-%m-%d %H:%M:%S'))
                                    trade.set_exit_time(exit_time.strftime('%Y-%m-%d %H:%M:%S'))
                                    trade.pl = float(round_to_nearest_0_05(trade.entry_price - trade.exit_price))

                                    entry_line = Line('entry_line')
                                    entry_line.x.append(entry_time.strftime('%Y-%m-%d %H:%M:%S'))
                                    entry_line.x.append(exit_time.strftime('%Y-%m-%d %H:%M:%S'))
                                    entry_line.y.append(entry_price)
                                    entry_line.y.append(entry_price)
                                    entry_line.color = "green"

                                    exit_line = Line('exit_line')
                                    exit_line.x.append(entry_time.strftime('%Y-%m-%d %H:%M:%S'))
                                    exit_line.x.append(exit_time.strftime('%Y-%m-%d %H:%M:%S'))
                                    exit_line.y.append(exit_price)
                                    exit_line.y.append(exit_price)
                                    exit_line.color = "red"
                                    
                                    symbol = Symbol("Exit Point")
                                    symbol.x = exit_time.strftime('%Y-%m-%d %H:%M:%S')
                                    symbol.y = data_frame.loc[i, 'close']
                                    symbol.color = "red"
                                    trade.symbols.append(symbol)

                                    trade.lines.append(entry_line)
                                    trade.lines.append(exit_line)
                                    trade.lines.append(tsl)
                                    trade.lines.append(y_high_line)
                                    trade.lines.append(y_low_line)
                                    trade_list.append(trade)

                                is_sell = False
                                is_cpr_above = False
                            
                            # ReportGeneration.extended_trade_report(self.timestamp, result, expiry_date)
                            else:
                                # TODO: Trading stop loss logic
                                diff = entry_price - current_price
                                if diff >= self.trailing_values[1]:
                                    increase_times = diff // self.trailing_values[1]
                                    new_stop_loss = initial_stop_loss - (increase_times * self.trailing_values[2]) 
                                    if new_stop_loss < stop_loss:
                                        tsl.x.append(data_frame.loc[i, 'datetime'].strftime('%Y-%m-%d %H:%M:%S'))
                                        tsl.x.append(data_frame.loc[i, 'datetime'].strftime('%Y-%m-%d %H:%M:%S'))
                                        tsl.y.append(stop_loss)
                                        tsl.y.append(new_stop_loss)
                                        stop_loss = new_stop_loss

        for trade in trade_list:
            NewReportGeneration.generate_json_report(self.timestamp, trade.to_dict(), expiry_date)
        return trade_list

def execute(request):
    if request.method == 'POST':
        form = CPRForm(request.POST)
        if form.is_valid():
            data = dict()
            instrument = form.cleaned_data['instrument']
            conditional_trade = form.cleaned_data['conditional_trade']
            # handle conditional trade
            if conditional_trade:
                # handle on long signal values
                on_long_signal = request.POST.get('onlongsignal')
                long_total_fields = 0
                if on_long_signal == "long call":
                    long_total_fields = 1
                elif on_long_signal == "short call":
                    long_total_fields = 1
                elif on_long_signal == "long put":
                    long_total_fields = 1
                elif on_long_signal == "short put":
                    long_total_fields = 1
                on_long_strike_value = request.POST.get('onlongstrikeselection')
                # store everything into the list
                long_choices = []
                long_inputs = []
                long_optimize = []
                long_optimize_sub_values = []
                if on_long_strike_value == "greeks":
                    for i in range(1, long_total_fields+1):
                        sub_values = []
                        delta_choice_value = request.POST.get(f'choice_delta_{on_long_strike_value}_long_{i}')
                        delta_input_value = request.POST.get(f'input_delta_{on_long_strike_value}_long_{i}')
                        delta_optimize_value = request.POST.get(f'optimize_delta_{on_long_strike_value}_long_{i}')
                        if delta_optimize_value:
                            delta_max_value = request.POST.get(f'max_delta_{on_long_strike_value}_long_{i}')
                            delta_min_value = request.POST.get(f'min_delta_{on_long_strike_value}_long_{i}')
                            delta_step_value = request.POST.get(f'step_delta_{on_long_strike_value}_long_{i}')
                            sub_values.append((delta_max_value, delta_min_value, delta_step_value))

                        gama_choice_value = request.POST.get(f'choice_gama_{on_long_strike_value}_long_{i}')
                        gama_input_value = request.POST.get(f'input_gama_{on_long_strike_value}_long_{i}')
                        gama_optimize_value = request.POST.get(f'optimize_gama_{on_long_strike_value}_long_{i}')
                        if gama_optimize_value:
                            gama_max_value = request.POST.get(f'max_gama_{on_long_strike_value}_long_{i}')
                            gama_min_value = request.POST.get(f'min_gama_{on_long_strike_value}_long_{i}')
                            gama_step_value = request.POST.get(f'step_gama_{on_long_strike_value}_long_{i}')
                            sub_values.append((gama_max_value, gama_min_value, gama_step_value))
                        
                        vega_choice_value = request.POST.get(f'choice_vega_{on_long_strike_value}_long_{i}')
                        vega_input_value = request.POST.get(f'input_vega_{on_long_strike_value}_long_{i}')
                        vega_optimize_value = request.POST.get(f'optimize_vega_{on_long_strike_value}_long_{i}')
                        if vega_optimize_value:
                            vega_max_value = request.POST.get(f'max_vega_{on_long_strike_value}_long_{i}')
                            vega_min_value = request.POST.get(f'min_vega_{on_long_strike_value}_long_{i}')
                            vega_step_value = request.POST.get(f'step_vega_{on_long_strike_value}_long_{i}')
                            sub_values.append((vega_max_value, vega_min_value, vega_step_value))

                        theta_choice_value = request.POST.get(f'choice_theta_{on_long_strike_value}_long_{i}')
                        theta_input_value = request.POST.get(f'input_theta_{on_long_strike_value}_long_{i}')
                        theta_optimize_value = request.POST.get(f'optimize_theta_{on_long_strike_value}_long_{i}')
                        if theta_optimize_value:
                            theta_max_value = request.POST.get(f'max_theta_{on_long_strike_value}_long_{i}')
                            theta_min_value = request.POST.get(f'min_theta_{on_long_strike_value}_long_{i}')
                            theta_step_value = request.POST.get(f'step_theta_{on_long_strike_value}_long_{i}')
                            sub_values.append((theta_max_value, theta_min_value, theta_step_value))

                        long_choices.append((delta_choice_value, gama_choice_value, vega_choice_value, theta_choice_value))
                        long_inputs.append((delta_input_value, gama_input_value, vega_input_value, theta_input_value))
                        long_optimize.append((delta_optimize_value, gama_optimize_value, vega_optimize_value, theta_optimize_value))
                        long_optimize_sub_values.append(sub_values)

                else:
                    for i in range(1, long_total_fields+1):
                        choice_value = int(request.POST.get(f'choice_{on_long_strike_value}_long_{i}'))
                        input_value = request.POST.get(f'input_{on_long_strike_value}_long_{i}')
                        optimize_value = request.POST.get(f'optimize_{on_long_strike_value}_long_{i}')
                        # if user checked optimize then only handle optimize fields
                        if optimize_value:
                            max_value = request.POST.get(f'max_{on_long_strike_value}_long_{i}')
                            min_value = request.POST.get(f'min_{on_long_strike_value}_long_{i}')
                            step_value = request.POST.get(f'step_{on_long_strike_value}_long_{i}')
                            long_optimize.append(optimize_value)
                            long_optimize_sub_values.append((max_value, min_value, step_value))
                        long_choices.append(choice_value)
                        long_inputs.append(input_value)
                    
                # handle on short signal values
                on_short_signal = request.POST.get('onshortsignal')
                short_total_fields = 0
                if on_short_signal == "long put":
                    short_total_fields = 1
                elif on_short_signal == "short put":
                    short_total_fields = 1
                elif on_short_signal == "long call":
                    short_total_fields = 1
                elif on_short_signal == "short call":
                    short_total_fields = 1
                on_short_strike_value = request.POST.get('onshortstrikeselection')
                # store everything into the list
                short_choices = []
                short_inputs = []
                short_optimize = []
                short_optimize_sub_values = []
                if on_short_strike_value == "greeks":
                    for i in range(1, short_total_fields+1):
                        sub_values = []
                        delta_choice_value = request.POST.get(f'choice_delta_{on_short_strike_value}_short_{i}')
                        delta_input_value = request.POST.get(f'input_delta_{on_short_strike_value}_short_{i}')
                        delta_optimize_value = request.POST.get(f'optimize_delta_{on_short_strike_value}_short_{i}')
                        if delta_optimize_value:
                            delta_max_value = request.POST.get(f'max_delta_{on_short_strike_value}_short_{i}')
                            delta_min_value = request.POST.get(f'min_delta_{on_short_strike_value}_short_{i}')
                            delta_step_value = request.POST.get(f'step_delta_{on_short_strike_value}_short_{i}')
                            sub_values.append((delta_max_value, delta_min_value, delta_step_value))

                        gama_choice_value = request.POST.get(f'choice_gama_{on_short_strike_value}_short_{i}')
                        gama_input_value = request.POST.get(f'input_gama_{on_short_strike_value}_short_{i}')
                        gama_optimize_value = request.POST.get(f'optimize_gama_{on_short_strike_value}_short_{i}')
                        if gama_optimize_value:
                            gama_max_value = request.POST.get(f'max_gama_{on_short_strike_value}_short_{i}')
                            gama_min_value = request.POST.get(f'min_gama_{on_short_strike_value}_short_{i}')
                            gama_step_value = request.POST.get(f'step_gama_{on_short_strike_value}_short_{i}')
                            sub_values.append((gama_max_value, gama_min_value, gama_step_value))
                        
                        vega_choice_value = request.POST.get(f'choice_vega_{on_short_strike_value}_short_{i}')
                        vega_input_value = request.POST.get(f'input_vega_{on_short_strike_value}_short_{i}')
                        vega_optimize_value = request.POST.get(f'optimize_vega_{on_short_strike_value}_short_{i}')
                        if vega_optimize_value:
                            vega_max_value = request.POST.get(f'max_vega_{on_short_strike_value}_short_{i}')
                            vega_min_value = request.POST.get(f'min_vega_{on_short_strike_value}_short_{i}')
                            vega_step_value = request.POST.get(f'step_vega_{on_short_strike_value}_short_{i}')
                            sub_values.append((vega_max_value, vega_min_value, vega_step_value))

                        theta_choice_value = request.POST.get(f'choice_theta_{on_short_strike_value}_short_{i}')
                        theta_input_value = request.POST.get(f'input_theta_{on_short_strike_value}_short_{i}')
                        theta_optimize_value = request.POST.get(f'optimize_theta_{on_short_strike_value}_short_{i}')
                        if theta_optimize_value:
                            theta_max_value = request.POST.get(f'max_theta_{on_short_strike_value}_short_{i}')
                            theta_min_value = request.POST.get(f'min_theta_{on_short_strike_value}_short_{i}')
                            theta_step_value = request.POST.get(f'step_theta_{on_short_strike_value}_short_{i}')
                            sub_values.append((theta_max_value, theta_min_value, theta_step_value))

                        short_choices.append((delta_choice_value, gama_choice_value, vega_choice_value, theta_choice_value))
                        short_inputs.append((delta_input_value, gama_input_value, vega_input_value, theta_input_value))
                        short_optimize.append((delta_optimize_value, gama_optimize_value, vega_optimize_value, theta_optimize_value))
                        short_optimize_sub_values.append(sub_values)
                else:
                    for i in range(1, short_total_fields+1):
                        choice_value = int(request.POST.get(f'choice_{on_short_strike_value}_short_{i}'))
                        input_value = request.POST.get(f'input_{on_short_strike_value}_short_{i}')
                        optimize_value = request.POST.get(f'optimize_{on_short_strike_value}_short_{i}')
                        # if user checked optimize then only handle optimize fields
                        if optimize_value:
                            max_value = request.POST.get(f'max_{on_short_strike_value}_short_{i}')
                            min_value = request.POST.get(f'min_{on_short_strike_value}_short_{i}')
                            step_value = request.POST.get(f'step_{on_short_strike_value}_short_{i}')
                            short_optimize.append(optimize_value)
                            short_optimize_sub_values.append((max_value, min_value, step_value))
                        short_choices.append(choice_value)
                        short_inputs.append(input_value)

            # handle the form cpr bottom fields
            from_date = form.cleaned_data['from_date']
            to_date = form.cleaned_data['to_date']
            cpr_range = form.cleaned_data['cpr_range']
            cpr_optimize = form.cleaned_data['cpr_optimize']
            data['instrument'] = instrument
            data['conditional_trade'] = conditional_trade
            data['from_date'] = from_date
            data['to_date'] = to_date
            data['cpr_range'] = cpr_range
            if cpr_optimize:
                cpr_min = form.cleaned_data['cpr_min']
                cpr_max = form.cleaned_data['cpr_max']
                cpr_step = form.cleaned_data['cpr_step']
                data['cpr_min'] = cpr_min
                data['cpr_max'] = cpr_max
                data['cpr_step'] = cpr_step
            exit_type = form.cleaned_data['exit_type']
            if exit_type == "time price":
                exit_time = request.POST.get("exit_time")
                data['exit_time'] = exit_time
                if request.POST.get('exit_time_optimize'):
                    exit_min = request.POST.get('exit_min_field')
                    exit_max = request.POST.get('exit_max_field')
                    exit_step = request.POST.get('exit_step_field')
                    data['exit_min'] = exit_min
                    data['exit_max'] = exit_max
                    data['exit_step'] = exit_step

            # handling trailing data
            trailing_type = form.cleaned_data['trailing_type']
            x = float(request.POST.get('x'))
            y = float(request.POST.get('y'))

            timestamp = time.time()
            timestamp = TimeStampConvertor.get_local_timestamp(timestamp)

            cpr_from = CPRFormData()
            cpr_from.from_date = from_date
            cpr_from.to_date = to_date
            cpr_from.instrument_type = instrument
            cpr_from.x = x
            cpr_from.y = y
            cpr_from.trailing_type = trailing_type
            cpr_from.exit_time = exit_time
            cpr_from.long_choices = long_choices
            cpr_from.short_choices = short_choices
            cpr_from.long_signal = on_long_signal
            cpr_from.short_signal = on_short_signal
            cpr_from.cpr_range = cpr_range

            # if conditional_trade:
            #     cpr = CPR(from_date, to_date, timestamp, exit_time, trailing_values, long_choices, short_choices)
            # else:
            #     cpr = CPR(from_date, to_date, timestamp, exit_time, trailing_values)
            cpr = CPR(cpr_from, timestamp)
            # start the strategy
            cpr.start()
            # create extended report
            cpr.create_extended_report()
            # get the data from the extended report
            result = cpr.get_extended_report_data()
            return render(request, 'visualizer/trade_table.html', {'data': result[0], 'file_path': f'./cpr/reports/{result[1]}/extended_trade_report.json'})   
    else:
        form  = CPRForm()
    return render(request, 'cpr/cpr_home.html', {'form': form})
