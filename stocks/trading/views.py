from django.shortcuts import render, redirect
import yfinance as yahooFinance
from .models import Position, Balance, Transaction
from django.contrib import messages
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import mpld3
import matplotlib.dates as mdates



def home (request):
    if request.method == 'POST':
        ticker=request.POST['ticker']
        stockData = yahooFinance.Ticker(ticker)
        end_date = datetime.today()
        start_date = end_date - timedelta(days=30)
        stock_data = yahooFinance.download(ticker, start=start_date, end=end_date)
    
        

        try:
            apiCall= stockData.info
            history = stockData.history(period="1mo")

             # Prepares data for the line chart
            dates = stock_data.index
            opening_prices = stock_data['Open']

            dates = stock_data.index
            opening_prices = stock_data['Open']

            plt.switch_backend('Agg')

            # Creates line chart
            fig, ax = plt.subplots(figsize=(9, 6))
            ax.plot(dates, opening_prices, label='Opening Prices')

            # Sets title and labels
            ax.set_title(f'Daily Opening Prices for {ticker}')
            ax.set_xlabel('Date')
            ax.set_ylabel('Opening Price')

            # Formats the x-axis as dates
            ax.xaxis.set_major_locator(mdates.AutoDateLocator())
            date_format = '%Y-%m-%D'
            ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))

        

            # Shows the plot
            chart_html = mpld3.fig_to_html(fig)
            plt.close()
            return render(request, 'home.html', {'apiCall' : apiCall, 'history' : history, 'chart_html': chart_html})
        except:
            apiCall = "Error..."
            return render(request, 'home.html', {'apiCall' : apiCall, 'history' : history, 'chart_html': chart_html})
    else:
        return render(request, 'home.html', {'defaultMessage' : "Enter a ticker symbol above..."})



def portfolio(request):
    balance = Balance.objects.get(pk=1).cash
    portfolio = Position.objects.all()
    for stock in portfolio:
       stock_data = yahooFinance.Ticker(stock.asset)
       stock_price = stock_data.info['currentPrice']
       stock.price = stock_price
       stock.value = stock_price * stock.quantity
       
       
    return render(request, 'portfolio.html', {'portfolio' : portfolio, 'balance': balance})

def buy(request):
    balance = Balance.objects.get(pk=1)
    if request.method == 'POST':
        obj, created = Position.objects.get_or_create(asset = request.POST.get("asset"))
        purchasedAmount = request.POST.get("quantity")
        purchasedAsset = obj.asset
        stockData = yahooFinance.Ticker(purchasedAsset)
        priceCheck = stockData.info['currentPrice']
        spendAmount = int(priceCheck) * int(purchasedAmount)
        dateTime = datetime.now()
        
        if obj.quantity:
            obj.quantity += int(purchasedAmount)
            balance.cash = (int(balance.cash) - spendAmount)
            balance.save()
            transaction_instance = Transaction(quantity= purchasedAmount, price= priceCheck, symbol= purchasedAsset, date= dateTime)
            transaction_instance.save()

        else:
            obj.quantity = purchasedAmount

        


        obj.save()

        return redirect('portfolio')
        

    else:
        return render(request, 'buySell.html', {})
    
def sell(request):
    balance = Balance.objects.get(pk=1)
    if request.method == 'POST':
        obj, created = Position.objects.get_or_create(asset = request.POST.get("asset"))
        soldAmount = int(request.POST.get("quantity"))
        previousAmount = int(obj.quantity)
        soldAsset = obj.asset
        stockData = yahooFinance.Ticker(soldAsset)
        priceCheck = stockData.info['currentPrice']
        gainAmount = int(priceCheck) * int(soldAmount)
        dateTime = datetime.now()

        
        if previousAmount == soldAmount:
            obj.delete()
            balance.cash = (int(balance.cash) + gainAmount)
            balance.save()
            transaction_instance = Transaction(quantity= soldAmount, price= priceCheck, symbol= soldAsset, date= dateTime)
            transaction_instance.save()
            return redirect('portfolio')
        
        
        elif previousAmount < soldAmount:
            errorMessage = "quantityError"
            return render(request, 'buySell.html', {'errorMessage' : errorMessage, 'previousAmount': previousAmount})
        
        else:
            obj.quantity -= int(soldAmount)
            obj.save()
            balance.cash = (int(balance.cash) + gainAmount)
            balance.save()
            transaction_instance = Transaction(quantity= soldAmount, price= priceCheck, symbol= soldAsset, date= dateTime)
            transaction_instance.save()
            return redirect('portfolio')

def transaction(request):
    List = Transaction.objects.all()
    transactionRev = List[::-1]
    transactions = transactionRev
    print(transactions)
    

    return render(request, "transaction.html", {'transactions' : transactions})
        
        

    
    

