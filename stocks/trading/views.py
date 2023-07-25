from django.shortcuts import render
import yfinance as yahooFinance
from .models import Position

# Create your views here.
def home (request):
    if request.method == 'POST':
        ticker=request.POST['ticker']
        stock_data = yahooFinance.Ticker(ticker)
        try:
            apiCall= stock_data.info
        except:
            apiCall = "Error..."
        return render(request, 'home.html', {'apiCall' : apiCall})
    else:
        return render(request, 'home.html', {'defaultMessage' : "Enter a ticker symbol above..."})



def portfolio(request):
    portfolio = Position.objects.all()
    for stock in portfolio:
       stock_data = yahooFinance.Ticker(stock.asset)
       stock_price = stock_data.info['currentPrice']
       stock.price = stock_price
       stock.value = stock_price * stock.quantity
       
       
    return render(request, 'portfolio.html', {'portfolio' : portfolio})

def buySell(request):

    return render(request, 'buySell.html')
