import json
from pykrx import stock

# 종목 목록을 가져와서 JSON 파일로 저장하는 부분
pk_counter = 1
stocks = []
ticker_name_list = []
tickers = stock.get_market_ticker_list()

for t in tickers:
    name = stock.get_market_ticker_name(t)
    ticker_name_list.append(name)
    
for i in range(20):
    stock_item = {
        'model': 'stock.StockList',
        'pk': pk_counter,
        'fields': {
            'ticker': tickers[i],
            'ticker_name': ticker_name_list[i]
        }
    }
    stocks.append(stock_item)
    pk_counter += 1

# Save the StockList data to a JSON file
# stock_list_file_path = 'make_data/stocklist_data.json'
# with open(stock_list_file_path, 'w', encoding='utf-8') as stock_list_file:
#     json.dump(stocks, stock_list_file, ensure_ascii=False, indent=4)

# print(f'StockList data saved to {stock_list_file_path}')

# 주식의 OHLCV 데이터를 가져와서 JSON 파일로 저장하는 부분
ohlcv_data = []
ohlcv_pk_counter = 1

for i in range(20):
    ticker = tickers[i]
    df = stock.get_market_ohlcv("20240401", "20240522", ticker)
    df.reset_index(inplace=True)
    
    for _, row in df.iterrows():
        ohlcv_record = {
            'model': 'stock.Stock',
            'pk': ohlcv_pk_counter,
            'fields': {
                'ticker': ticker,
                'date': row['날짜'].strftime('%Y-%m-%d'),
                'opening_price': int(row['시가']),
                'highest_price': int(row['고가']),
                'lowest_price': int(row['저가']),
                'closing_price': int(row['종가']),
                'volume': int(row['거래량']),
                'fluctuation_rate': float(row['등락률'])
            }
        }
        ohlcv_data.append(ohlcv_record)
        ohlcv_pk_counter += 1

# Save the OHLCV data to a JSON file
ohlcv_file_path = 'make_data/stock_ohlcv_data.json'
with open(ohlcv_file_path, 'w', encoding='utf-8') as ohlcv_file:
    json.dump(ohlcv_data, ohlcv_file, ensure_ascii=False, indent=4)

print(f'Stock OHLCV data saved to {ohlcv_file_path}')
