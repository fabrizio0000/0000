
from func_connections import connect_dydx
from constants import ABORT_ALL_POSITIONS, FIND_COINTEGRATED, PLACE_TRADES, MANAGE_EXITS
from func_private import place_market_order, abort_all_positions
from func_public import construct_market_prices
from func_cointegration import store_cointegration_results
from func_entry_pairs import open_positions
from func_exit_pairs import manage_trade_exits

if __name__=="__main__":

    # Connect to client
    try:
        print("Connecting to client...")
        client=connect_dydx()
    except Exception as e:
        print("!ERROR! Error connecting to client: ", e)
        exit(1)

    # Aborting all positions
    if ABORT_ALL_POSITIONS:
        try:
            print("Closing all positions...")
            close_orders= abort_all_positions(client)
        except Exception as e:
            print("!ERROR! Error closing all positons: ", e)
            exit(1)

    # Find Cointegrated Pairs
    if FIND_COINTEGRATED:

        # Construct Market Prices
        try:
            print("Fetching market prices...")
            df_market_prices = construct_market_prices(client)
        except Exception as e:
            print("!ERROR! Error constructing market prices: ", e)
            exit(1)

        # Store Cointegrated Pairs
        try:
            print("Storing cointegrated pairs...")
            store_result = store_cointegration_results(df_market_prices)
            if store_result != "saved": #if it doens't find cointegrated pairs
                print("!ERROR! Error storing cointegrated pairs ") 
                exit(1)
        except Exception as e:
            print("!ERROR! Error storing cointegrated pairs ", e)
            exit(1)

    while True:
        # Manage exits
        if MANAGE_EXITS:
            try:
                print("Managing exits...")
                manage_trade_exits(client)
            except Exception as e:
                print("Error managing exits: ", e)
                exit(1)

        # Place trades for opening positions
        if PLACE_TRADES:
            try:
                print("Finding trading opportunities...")
                open_positions(client)
            except Exception as e:
                print("Error trading pairs: ", e)
                exit(1)
