"""

Making trades

"""

def moving_average(prices, n):
    """
    Calculates n-period moving average of a list of floats/integers.

    Parameters:
        prices: list of values (ordered in time),
        n: integer moving-average parameter

    Returns:
        list with None for the first n-1 values in prices and the appropriate moving average for the rest

    Example use:
    >>> ma = moving_average([2,3,4,5,8,5,4,3,2,1], 3)
    >>> [round(m, 2) if m is not None else None for m in ma]
    [None, None, 3.0, 4.0, 5.67, 6.0, 5.67, 4.0, 3.0, 2.0]
    >>> moving_average([2,3,4,5,8,5,4,3,2,1], 2)
    [None, 2.5, 3.5, 4.5, 6.5, 6.5, 4.5, 3.5, 2.5, 1.5]
    """
    # Your code here. Don't change anything above.

    ma = []
    for i in range(0,n-1):
        ma.append(None)
    for i in range(n, len(prices)+1):
        total = 0
        for j in range(0,n):
            total = total + prices[i-j-1]
        average = total/n
        ma.append(average)
    return ma


def cross_overs(prices1, prices2):
    """ 
    Identify cross-over indices for two equal-length lists of prices (here: moving averages)

    Parameters:
        prices1, prices2: lists of prices (ordered by time)

    Returns:
        list of crossover points

    Each item in the returned list is a list [time_index, higher_index], where:
        - time_index is the crossover time index (when it happends
        - higher_index indicates which price becomes higher at timeIndex: either 1 for first list or 2 for second list
    
    There are no crossovers before both price lists have values that are not None.
    You can start making comparisons from the point at which both have number values.
    
    Example use:
    >>> p1 = [1, 2, 4, 5]
    >>> p2 = [0, 2.5, 5, 3]
    >>> cross_overs(p1, p2)
    [[1, 2], [3, 1]]
    >>> p1 = [None, 2.5, 3.5, 4.5, 4.5, 3.5, 2.5, 1.5, 3.5, 3.5]
    >>> p2 = [None, None, 3.0, 4.0, 4.333333333333333, 4.0, 3.0, 2.0, 3.0, 2.6666666666666665]
    >>> cross_overs(p1, p2)
    [[5, 2], [8, 1]]
    >>> l3 = [1,22,5,14,8,20,4]
    >>> l4 = [38,21,4,15,10,17,6]
    >>> cross_overs(l3, l4)
    [[1, 1], [3, 2], [5, 1], [6, 2]]
    """
    # Your code here. Don't change anything above.
    crossovers = []
    for i in range(len(prices1)-1):
        if prices1[i] != None and prices2[i] != None and prices1[i+1] != None and prices2[i+1] != None: 
            if prices1[i] > prices2[i]:
                if prices2[i+1] > prices1[i+1]:
                    crossovers.append([i+1,2])
            if prices2[i] > prices1[i]:
                if prices1[i+1] > prices2[i+1]:
                    crossovers.append([i+1,1])
    return crossovers



def make_trades(starting_cash, prices, crossovers):
    """
    Given an initial cash position, use a list of crossovers to make trades

    Parameters:
        starting_cash: initial cash position
        prices: list of prices (ordered by time)
        crossovers: list of crossover points on the prices

    Returns:
        list containing current value of trading position (either in stock value or cash) at each time index
    
    Assume each item crossovers[i] is a list [time_index, buy_index]
    Assume that buy_index = 1 means "buy"
    Assume that buy_index = 2 means "sell"

    We buy stock at any time_index where crossover's buy_index indicates 1, and sell at 2.
    In more detail:
        - We want to buy at time_index whenever buy_index = 1 and we currently hold a cash position
            - We buy at the stock price at time_index. We buy with the entire cash position we have and only hold stock
        - We want to sell at time_index when buy_index = 2 and we hold a stock position
            - We sell at the stock price at time_index. We sell our entire stock position and will only hold cash

    Whenever we trade, we buy with our entire cash position, or sell our entire stock position.
    We will therefore always hold either stock or cash, but never both.
    
    Assume we can hold fractional stock quantities, and there are no transaction fees.

    Example use:
    # In the first example, We start with cash 1.0.
    # We hold cash until we buy at index 1 at the price 4. We then hold 0.25 shares. 
    # After that, our portfolio is in stock, so its value fluctuates with the stock price.
    # As the stock price goes from 4 to 6, our portfolio value goes from 1.0 to 1.5.
    # This goes on until we sell at index 3 at the price 5. 
    # Then we hold cash again and the value of the portfolio does not change as it is in cash.
    >>> starting_cash = 1.0
    >>> prices = [2,4,6,5,1]
    >>> cos = [[1, 1], [3, 2]] # not real crossovers, just to illustrate portfolio value when trading
    >>> values = make_trades(starting_cash, prices, cos)
    >>> values 
    [1.0, 1.0, 1.5, 1.25, 1.25]
    >>> starting_cash = 1000.0
    >>> prices = [2,3,4,5,4,3,2,1,6,1,5,7,8,10,7,9]
    >>> cos = [[5, 2], [8, 1], [10, 2], [11, 1], [15, 2]]
    >>> values = make_trades(starting_cash, prices, cos)
    >>> [round(v, 2) for v in values] # round every value of the returned list using list comprehension
    [1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 166.67, 833.33, 833.33, 952.38, 1190.48, 833.33, 1071.43]
    >>> prices =[38,21,20,13,7,14,22,23,27,23,44,26,48,32,48,60,70,40,34,35,33]
    >>> crossovers = [[7, 1], [19, 2]]
    >>> money = 100.0
    >>> values = make_trades(money, prices, crossovers)
    >>> [round(v, 2) for v in values] # round every value of the returned list using list comprehension
    [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 117.39, 100.0, 191.3, 113.04, 208.7, 139.13, 208.7, 260.87, 304.35, 173.91, 147.83, 152.17, 152.17]
    >>> l2 = [39,22,5,14,8,15,23,27,23,44,26,48,32,48,13,34,15,34,35]
    >>> c2 = [[4, 1], [5, 2], [6, 1], [11, 2], [12, 1], [13, 2], [16, 1], [17, 2], [18, 1]]
    >>> values = make_trades(10.0, l2, c2)
    >>> [round(v, 3) for v in values] # round every value of the returned list using list comprehension
    [10.0, 10.0, 10.0, 10.0, 10.0, 18.75, 18.75, 22.011, 18.75, 35.87, 21.196, 39.13, 39.13, 58.696, 58.696, 58.696, 58.696, 133.043, 133.043]
    """
    # Your code here. Don't change anything above.
    # Note: the rounding in the examples happens *after* the function call. Your function should not round the results.
    current_value = [starting_cash]  # value of portfolio
    cross_over_index = 0
    price_bought_index = 0
    become_stock = 0
    
    #should be ordered by index
    crossovers = sorted(crossovers, key = lambda x: x[0])

    #Initally, need to start with cash, thats why must only can start with buy    
    start_buy = 0
    while crossovers[start_buy][1] != 1:
        start_buy += 1
    crossovers = crossovers[start_buy:]
    
    #Can only buy all, and sell all. cannot consecutive buy for two times.
    crossovers_clean = []
    now_stock = 0
    for i in range(len(crossovers)):
        #buy, provided that its currently all cash
        if crossovers[i][1] == 1 and now_stock == 0:
            now_stock = 1
            crossovers_clean.append(crossovers[i])
        #sell, provided that its currently stock
        elif crossovers[i][1] == 2 and now_stock == 1:
            now_stock = 0
            crossovers_clean.append(crossovers[i])            
        else:
            continue
        
    #now that the crossovers is clean and proper, can start making trades
    for i in range(len(prices)):
            #BECOME STOCK
            if crossovers_clean[cross_over_index][0] == i and crossovers_clean[cross_over_index][1] == 1:
                become_stock = 1
                price_bought_index = i
                current_value.append(current_value[-1])
                cross_over_index = cross_over_index + 1
                cross_over_index = min(cross_over_index, len(crossovers)-1)
            #BECOME CASH
            elif crossovers_clean[cross_over_index][0] == i and crossovers_clean[cross_over_index][1] == 2:
                become_stock = 0
                new_value = prices[i]/prices[price_bought_index]*current_value[price_bought_index]
                current_value.append(new_value)
                cross_over_index = cross_over_index + 1
                cross_over_index = min(cross_over_index, len(crossovers)-1)
            else:
                if become_stock == 1:    
                    new_value = prices[i]/prices[price_bought_index]*current_value[price_bought_index]
                    current_value.append(new_value)
                elif become_stock == 0:
                    current_value.append(current_value[-1])
    return current_value[1:]



