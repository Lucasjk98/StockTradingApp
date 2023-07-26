from django.shortcuts import render, redirect
import yfinance as yahooFinance
from .models import Position, Balance, Transaction
from django.contrib import messages

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

def buy(request):
    if request.method == 'POST':
        obj, created = Position.objects.get_or_create(asset = request.POST.get("asset"))
        purchasedAmount = request.POST.get("quantity")
        if obj.quantity:
            obj.quantity += int(purchasedAmount)
        else:
            obj.quantity = purchasedAmount

        


        obj.save()

        return redirect('portfolio')
        

    else:
        return render(request, 'buySell.html', {})
    
def sell(request):
    if request.method == 'POST':
        obj, created = Position.objects.get_or_create(asset = request.POST.get("asset"))
        soldAmount = int(request.POST.get("quantity"))
        previousAmount = int(obj.quantity)
        print(soldAmount)
        print(previousAmount)
        if previousAmount == soldAmount:
            obj.delete()
            return redirect('portfolio')
        
        elif previousAmount < soldAmount:
            print(soldAmount)
            print(previousAmount)
            errorMessage = "quantityError"
            return render(request, 'buySell.html', {'errorMessage' : errorMessage, 'previousAmount': previousAmount})


        
        else:
            obj.quantity -= int(soldAmount)
            obj.save()
            return redirect('portfolio')

        
        

    
    

