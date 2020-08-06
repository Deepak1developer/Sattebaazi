import os
import pandas as pd
from datetime import date
from concurrent.futures.thread import ThreadPoolExecutor
from nsetools import Nse
from nsepy.history import get_history
from concurrent import futures
def save_nse_500_tickers():
    list_of_stock_codes = list(pd.read_csv('nifty50list.csv')['Symbol'])
    return list_of_stock_codes
def store_nse_data(ticker, start, end):
    print('Start fetching: ',ticker)
    if not os.path.exists('nse_data/{}.csv'.format(ticker)):
        try:
            df_nse = get_history(symbol=ticker, start=start, end=end)
        except Exception as e:
            # NSE_INDICES_TO_BE_SKIPPED.append(ticker)
            return None
        df_nse.to_csv('nse_data/{}.csv'.format(ticker))
        print('Save data for {}'.format(ticker))
        return 'Success'
    else:
        print('Already have {}'.format(ticker))
        return 'Already there'
def get_data_from_nsepy():
    # Create a directory if it does not exist.
    if not os.path.exists('nse_data'):
        os.makedirs('nse_data')
    tickers = save_nse_500_tickers()
    start=date(2010,1,1)
    end=date(2020,5,14)
    pools = dict()
    with ThreadPoolExecutor(max_workers=4) as executor:
        for ticker in tickers:
            pools[executor.submit(store_nse_data, ticker, start, end)] = ticker
        for future in futures.as_completed(pools):
            if future.exception() is not None:
                raise future.exception()
    print('Completed')
get_data_from_nsepy()