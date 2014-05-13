import random
from Tkinter import *
import tkMessageBox
import tkSimpleDialog
import urllib2
from bs4 import BeautifulSoup as Soup
import string
import matplotlib.pyplot as plt
import numpy as np

###########################################
# Animation class
###########################################
#Animation Class taken from class notes by David Kosbie
#http://www.kosbie.net/cmu/fall-12/15-112/handouts/AnimationWithClasses
#/Animation.py

class Animation(object):
        
    global PLAYER
    # Override these methods when creating your own animation]]]
    #runs the events for when mouse clicked, such as inside button
    def mousePressed(self, event): 
        self.helpButton.mousePressed(event)
        self.buyButton.mousePressed(event)
        self.sellButton.mousePressed(event)
        self.graphButton.mousePressed(event)
        self.nextMarketPageButton.mousePressed(event)
        self.previousMarketPageButton.mousePressed(event)
        self.nextPortfolioPageButton.mousePressed(event)
        self.previousPortfolioPageButton.mousePressed(event)
        
    def keyPressed(self, event):
        pass
                 
#made a fake time cycle, since its going at a delay of
#250 milliseconds probably not a bad idea to set 2 seconds = 1 hour therefore
#one hour = (timerFired * 4) * 2     
    def timerFired(self):
        self.timer += 1
        if self.timer % 8 == 0 and self.timer != 0:
            self.hour += 1
#modifies the prices that have actually been invovled in game, this way they
#wont be different and re-pulled info from internet, instead they'll be based
#on the in-game algorithms
            self.modifyStocksInGame(PLAYER.pricesOfStocksBought)
        self.news.writeStory()
        PLAYER.calculateMoneyMade()
        PLAYER.calculateNetWorth()
        if self.news.locX < 0:
            self.news.pickRandomCompany()
            self.news.changeType()
            self.news.locX = 1000
        if self.hour == 24:
            self.day += 1
            self.hour = 0
        if PLAYER.cash >= 200000.00 and self.displayedVictoryMessage == False:
            self.displayVictory()
            self.displayedVictoryMessage = True
        if (PLAYER.cash <= 0 and PLAYER.value <= 0 and
            self.displayedDefeatMessage == False):
            self.displayDefeat()
            self.displayedDefeatMessage = True
            
#This modifies the stock prices, depends on if there is a news story about the
#company, otherwise it is a random change in price
    def modifyStocksInGame(self,pricesOfStocksBought):
        value,randomPos,randomNeg,good,bad = 0,1.01,.99,1.02,.98
        superGood = 1.5
        superBad = .5
        for stock in pricesOfStocksBought:
            superChance = random.randint(0,100000)
            chance = random.randint(0,2) 
#if stock hasnt been involved in game adds to game so it will get modified
            if stock not in PLAYER.oldPrices:
                    PLAYER.oldPrices[stock] = []
#super lukcy events make stocks go way up or way down, small chance
            if superChance == 69: pricesOfStocksBought[stock] *= superGood
            elif superChance == 156: pricesOfStocksBought[stock] *= superBad
#If there is a positive news story active about company it increases value
            elif (self.news.company == stock and self.news.type == 'Good'):
                pricesOfStocksBought[stock] *= good     
#if negative news story it decreases value
            elif (self.news.company == stock and self.news.type == 'Bad'):
                pricesOfStocksBought[stock] *= bad
#neutral news story means nothing happens to stock price
            elif (self.news.company == stock and self.news.type == 'Neutral'):
                pricesOfStocksBought[stock] = pricesOfStocksBought[stock]
#if no news stories then it randomly changes value of stocks but not by as
#much as if there are news stories
            elif chance == 0: pricesOfStocksBought[stock] *= randomPos
            elif chance == 1: pricesOfStocksBought[stock] *= randomNeg
            PLAYER.oldPrices[stock].append(pricesOfStocksBought[stock])
#assesses the value of the portfolio       
        for stock in PLAYER.portfolio:
            value += pricesOfStocksBought[stock] * PLAYER.portfolio[stock]
        if value != PLAYER.value:
            PLAYER.value = value       
     
#creates all the needed variables and what not, inits the news as well as
#creates all the buttons,screens, and timer
    def init(self):
        self.timer,self.hour,self.day = 0,0,0
        self.displayedVictoryMessage = False
        self.displayedDefeatMessage = False
        self.helpButton = Button('Help',700,700,75,25,self.canvas)
        self.buyButton = Button('Buy', 100,600,75,25,self.canvas)
        self.sellButton = Button('Sell',300,600,75,25,self.canvas)
        self.portfolioScreen = Screen('Portfolio', self.canvas)
        self.graphButton = Button('Graph',700,150,75,25,self.canvas)
        self.marketScreen = Screen('Market Screen',self.canvas)
        self.news = News(self.canvas,PLAYER, 'Neutral')
        self.nextPortfolioPageButton = Button('Next Portfolio',300,550,75,10,
                                                self.canvas)
        self.previousPortfolioPageButton = Button('Previous Portfolio',100,550,
                                                    75,10,self.canvas)
        self.nextMarketPageButton = Button('Next Market',800,550,75,10,
                                            self.canvas)
        self.previousMarketPageButton = Button('Previous Market',600,550,75,
                                                10,self.canvas)
        self.news.pickRandomCompany()
        self.helpScreen = Screen('Help',self.canvas)
        self.helpScreen.drawMessage()
        
#Shows the victory, need 200,000 cash to win
    def displayVictory(self):
        title = 'Victory!'
        message = '''Congratulations on reaching $200,000!
                     Technically you've won but feel free to keep playing!'''
        tkMessageBox.showinfo(title,message)

#shows when players lose all their money
    def displayDefeat(self):
        title = 'Defeat!'
        message = ('So sorry you lost, maybe you should study a little ' +
                    'and try again later')
        tkMessageBox.showinfo(title,message)        
                        
#redraws everything on the canvas, all the buttons, screens, news, etc...
    def redrawAll(self): 
        spacer = 40
        self.helpButton.draw()
        self.buyButton.draw()
        self.sellButton.draw()
        self.portfolioScreen.drawPortfolioScreen()
        self.marketScreen.drawMarketScreen()
        self.graphButton.draw()
        self.nextPortfolioPageButton.draw()
        self.previousPortfolioPageButton.draw()
        self.nextMarketPageButton.draw()
        self.previousMarketPageButton.draw()
#displays the timer
        self.canvas.create_text(self.width,self.height,
        text = 'Day: %d  Hour: %d' % (self.day,self.hour), anchor = 'se')
        self.canvas.create_rectangle(0,0,self.width,spacer, fill = 'yellow',
        outline = 'yellow')
        self.canvas.create_text(self.width/2,spacer,anchor = 'n',
        text = 'News Stories', font = 'bold 14')
        self.news.writeStory()
               
    # Call app.run(width,height) to get your app started
    def run(self, width=1000, height=800):
        # create the root and the canvas
        root = Tk()
        self.width = width
        self.height = height
        self.canvas = Canvas(root, width=width, height=height)
        self.canvas.pack()
        # set up events
        def redrawAllWrapper():
            self.canvas.delete(ALL)
            self.redrawAll()
        def mousePressedWrapper(event):
            self.mousePressed(event)
            redrawAllWrapper()
        def keyPressedWrapper(event):
            self.keyPressed(event)
            redrawAllWrapper()
        root.bind("<Button-1>", mousePressedWrapper)
        root.bind("<Key>", keyPressedWrapper)
        # set up timerFired events
        self.timerFiredDelay = 250 # milliseconds
        def timerFiredWrapper():
            self.timerFired()
            redrawAllWrapper()
            # pause, then call timerFired again
            self.canvas.after(self.timerFiredDelay, timerFiredWrapper)
        # init and get timerFired running
        self.init()
        timerFiredWrapper()
        # and launch the app
        root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)
  
  
#creates the generic class for buttons, which take a type, location of center,
#length,height, and the canvas upon which they are placed
class Button(Animation):
    
    #creates each instance and stores the inputs into the self
    def __init__(self, typeOfButton, centerX, centerY, length, height,canvas):
        self.type = typeOfButton
        self.centerX = centerX
        self.centerY = centerY
        self.length = length
        self.height = height
        self.canvas = canvas
        
    #makes each button (rectangle) given a type, center, length, and height
    def draw(self):
        centerX = self.centerX
        centerY = self.centerY
        length = self.length
        height = self.height
        self.canvas.create_rectangle(centerX - length, centerY - height,
                                centerX + length, centerY + height, width = 4)
        self.canvas.create_text(centerX,centerY, text = self.type)
    
    #checks to see if button clicked by checking if click was within
    #the boundaries of the rectangle, creates the associated screen if
    #clicked
    def mousePressed(self, event):    
        xCoord = event.x
        yCoord = event.y
        folio = PLAYER.portfolio
        stocks = PLAYER.pricesOfStocksBought
        marketPage = PLAYER.marketScreenPage
        portfolioPage = PLAYER.portfolioScreenPage
        leftBound = self.centerX - self.length
        rightBound = self.centerX + self.length
        topBound = self.centerY - self.height
        bottomBound = self.centerY + self.height
#makes it so the screen can go display the next set of stocks in game
        if (xCoord >= leftBound and xCoord <= rightBound and
            yCoord >= topBound and yCoord <= bottomBound and self.type ==
            'Next Market'):
            if len(stocks) %((marketPage+1) * 5) > 0 or len(stocks) > 5:
                PLAYER.marketScreenPage += 1
            if ((marketPage+2) * 5) > len(stocks):
                PLAYER.marketScreenPage -= 1
#makes it so the screen can display the previous set of stocks in game
        elif (xCoord >= leftBound and xCoord <= rightBound and
            yCoord >= topBound and yCoord <= bottomBound and self.type ==
            'Previous Market'):
            if marketPage >= 1:
                PLAYER.marketScreenPage -= 1
#makes it so screen can display the next set of stocks in portfolio              
        elif (xCoord >= leftBound and xCoord <= rightBound and
            yCoord >= topBound and yCoord <= bottomBound and self.type ==
            'Next Portfolio'):
            if len(folio) > 5:
                PLAYER.portfolioScreenPage += 1
            if ((portfolioPage+1)*5) > len(folio) and len(folio) > 5:
                PLAYER.portfolioScreenPage -= 1
#makes it so the screen can display the previous set of stocks in portfolio       
        elif (xCoord >= leftBound and xCoord <= rightBound and
            yCoord >= topBound and yCoord <= bottomBound and self.type ==
            'Previous Portfolio'):
            if portfolioPage >= 1:
                PLAYER.portfolioScreenPage -= 1
        elif (xCoord >= leftBound and xCoord <= rightBound and
            yCoord >= topBound and yCoord <= bottomBound):
            newScreen = Screen(self.type,self.canvas)
            #draws each screen's individual and type specific message
            newScreen.drawMessage()

#makes the player class, which contains all the stock info of the player
#as well as old prices of stocks
class Player(object):

#uses the global starting stocks to hold the info for several stocks to 
#have listed in the market screen for when game starts
    
     global STARTINGSTOCKS
     
#creates each instance of the player class, giving it a portfolio, value
     def __init__(self,name):
         self.cash = 100000.00
         self.name = name
         self.portfolio = {}
         self.pricesOfStocksBought = STARTINGSTOCKS
         self.value = 0.00
         self.oldPrices = {}
         self.marketScreenPage = 0
         self.portfolioScreenPage = 0
         self.moneyMade = 0.00
         self.netWorth = 100000.00
         self.priceBoughtAt = {}
         
#figures out the amount player has made since starting, includes value of
#portfolio
     def calculateMoneyMade(self):
         self.moneyMade = self.value + self.cash - 100000.00

#figures out the net worth of the player by adding value of portfolio
#and the amount of cash available    
     def calculateNetWorth(self):
         self.netWorth = self.value + self.cash
 
#buy function for the player, takes in stock info which holds the name, price,
#and amount to be bought                 
     def buy(self,stockInfo):
         stockName = stockInfo[0]
#checks to see if stock is already in game, if so uses the current price
#that has been modified by in game algorithms
         if stockName in self.pricesOfStocksBought:
             stockPrice = self.pricesOfStocksBought[stockName]
#if stock not in game then it uses the info pulled from yahoo finance
         else:
             stockPrice = stockInfo[1]
         numberBought = stockInfo[2]
#checks to make sure number bought from input is actually an integer, if it
#is carries out the normal buy function
         try: 
             type(numberBought) == int
             self.cash -= stockPrice * numberBought
             self.priceBoughtAt[stockName] = stockPrice
#checks to make sure player has enough cash, if cash goes below zero prevents
#the trade from going through
             if self.cash < 0:
                self.cash += stockPrice * numberBought
                title = 'Warning!'
                message = "You Don't Have Enough Cash!"
                tkMessageBox.showinfo(title,message)
#if stock already in portfolio adds to the amount already in it
             elif stockName in self.portfolio:
                self.portfolio[stockName] += numberBought
                for stock in self.portfolio:
                    self.value += self.pricesOfStocksBought[stock] 
#if stock not in portfolio adds it to dictionary
             else:
                self.portfolio[stockName] = numberBought
                self.pricesOfStocksBought[stockName] = stockPrice
#except clause for if player clicks cancel then it just closes window
         except:
             if type(numberBought) != int or type(numberBought) != str:
                 pass
#except clause for improper input, displays error message
             else: 
                displayErrorMessage()

#sell function for the player, takes in the name, price, and number to sell
#of the stock                        
     def sell(self, stockInfo):
#defines all of the variables for stock name and price
         stockName = stockInfo[0]
         stockPrice = self.pricesOfStocksBought[stockName]
#subtracts the number sold from the portfolio
         self.portfolio[stockName] -= stockInfo[2]
#if player tries to sell more than they own it stops them
         if self.portfolio[stockName] < 0:
             self.portfolio[stockName] += stockInfo[2]
             title = 'Warning!'
             message = "You Don't Own That Many!"
             tkMessageBox.showinfo(title,message)
         self.cash += stockPrice * stockInfo[2]
#if sold all of a stock owned then it removes from dictionary
         if self.portfolio[stockName] == 0: 
             del self.portfolio[stockName]
             
#sets up the screen class, which displays all the different screens and
#information for the game               
class Screen(Animation):
    
#initializes the screen class, takes in a canvas and type of screen
   def __init__(self,typeOfScreen,canvas):
       self.type = typeOfScreen
       self.canvas = canvas
       self.center = 200
  
#figures out which screen to draw based on the type            
   def drawMessage(self):
       if self.type == 'Help': self.drawHelpScreen()
       elif self.type == 'Buy': self.drawBuyScreen()
       elif self.type == 'Sell': self.drawSellScreen()
       elif self.type == 'Portfolio': self.drawPortfolioScreen()
       elif self.type == 'Graph': self.drawGraphScreen()
       elif self.type == 'Market': 
           self.drawMarketScreen()

#draws the portfolio
   def drawPortfolioScreen(self):
       width,height = 1000,800
       spacer = 15
       centerX = width / 5
       spacing = 0
       centerY = height / 2
       canvas = self.canvas
       portfolio = []
       #adds the info to a list to allow for multiple pages to be displayed
       for stock in PLAYER.portfolio.items():
           portfolio.append(stock)
       if len(portfolio) <= 5: pageStart,pageEnd = 0,len(portfolio)
       else: 
           pageStart = 5 * PLAYER.portfolioScreenPage
           pageEnd = 5 * (PLAYER.portfolioScreenPage + 1)
#creates the headers and information displays like name, cash, value
       canvas.create_text(spacer,height,text = 
                'Portfolio Value: %.2f' % PLAYER.value,anchor='sw')
       canvas.create_text(spacer,height-spacer,text =
                'Cash Remaining: %.2f' % PLAYER.cash, anchor = 'sw')
       canvas.create_text(spacer, height-(spacer*2), text = 
            'Net Worth: %.2f' % PLAYER.netWorth, anchor = 'sw')
       canvas.create_text(spacer, height - (spacer * 3), text = 
            'Money Made: %.2f' % PLAYER.moneyMade, anchor = 'sw')
       canvas.create_text(spacer,height-(spacer*4),text = 
                'Player Name: ' + str(PLAYER.name), anchor = 'sw') 
#height and width divided by 6 to create a better looking interface, makes
#it look nice and more evenly distributed
       canvas.create_rectangle(centerX - width/6, centerY - height/6,
                               centerX + width/6, centerY + height/6)
       canvas.create_text(centerX,centerY - height/6,
    text = '(Stock) (Number) (Bought at) (Current Price)', anchor = 's')
       canvas.create_text(centerX,centerY - height/6 - spacer,
                            text = 'Player Portfolio', anchor = 's', 
                            font = 'bold 14')
#draws the text for each stock in players portfolio
       if PLAYER.portfolio != {}:
            for i in xrange(pageStart,pageEnd):
                if i >= len(portfolio): break
                else:
#empty string used to space out the content to look more clean and
#to create a nicer looking user interface
                    canvas.create_text(centerX,centerY - height/6 + 
                    (spacing * spacer),text = str(portfolio[i][0]) + 
                    '        ' + str (portfolio[i][1]) + '             '
                    + '%.2f' % PLAYER.priceBoughtAt[portfolio[i][0]] + '         '
                    + '%.2f' % PLAYER.pricesOfStocksBought[portfolio[i][0]]
                    + '        ',
                    anchor = 'n')
                    spacing += 1
           
#creates the help info screen, which displays hints on how to play game           
   def drawHelpScreen(self):
       title = 'Help'
       message = '''Welcome To the Stock Market Game!
       Starting with $100,000, will you become the next Trump?
       Use the buttons to buy or sell stocks
       Click graph to show the stock trends
       Pay attention to the news for valuable information!
       Try to get to atleast $200,000 to win!
       You lose if you lose all your money and have no stocks left!'''
       tkMessageBox.showinfo(title,message)
      
#creates the market display
   def drawMarketScreen(self):
       market = []
       #adds the info to a list to allow for multiple pages to be displayed
       for stock in PLAYER.pricesOfStocksBought.items():
           market.append(stock)
       if len(market) <= 5: pageStart,pageEnd = 0,len(market)
       else: 
           pageStart = 5 * PLAYER.marketScreenPage
           pageEnd = 5 * (PLAYER.marketScreenPage + 1)
       width,height = 1000,800
       spacer = 15
       centerX = 700
       spacing = 0
       centerY = 400
       canvas = self.canvas
#draws the headers and again the height and width divided by 6 is used to
#create more viusally appealing interface
       canvas.create_rectangle(centerX - width/6, centerY - height/6,
                               centerX + width/6, centerY + height/6)
       canvas.create_text(centerX,centerY - height/6,
                            text = 'Stock        Price', anchor = 's')
       canvas.create_text(centerX,centerY - height/6 - spacer,
                            text = 'Current Market', anchor = 's', font = 
                            'bold 14')
#displays the text for each stock that's currently in the market
       for i in xrange(pageStart,pageEnd):
           if i >= len(market): break
           else:
                canvas.create_text(centerX,centerY - height/6 + (spacing * 20),
                text = str(market[i][0]) + '        ' + '%.2f' % 
                market[i][1], anchor = 'n')
                spacing += 1
        
#creates the pop up graph display
   def drawGraphScreen(self):
#dialog box asking what stock to look up and graph
        title = 'Stock Search'
        message = 'What stock would you like to graph?'
        search = tkSimpleDialog.askstring(title,message)
#checks to make sure it's a proper response that makes sense
        if type(search) == str:
            try: stock = searchYahoo(search)
#if it doesn't work displays error message
            except: displayErrorMessage()
            stockName = stock[0]
            data = PLAYER.oldPrices[stockName] 
            y = data
            x = np.arange(0,len(data))
            plt.plot(x,y)
#labels the axes
            plt.xlabel('Hours')
            yLabel = 'Price of %s' % stockName
            plt.ylabel(yLabel)
            plt.show()
#if player clicks cancel just closes window
        else: pass
        
#creates the box that first calls getStockQuoteString to ask what stock to
#search for, then uses getStockInfo to get name, price, and amount, then calls
#the buy function on that stockInfo
   def drawBuyScreen(self):
#try and except to make sure input is correct type
        try:
           stockString = getStockQuoteString()
           if type(stockString) == str:
                stockInfo = getStockInfo(stockString)
                PLAYER.buy(stockInfo)
#checks if player clicks cancel then it just closes
           else:
                pass
#this cals the same function again so if input invalid it just asks again
        except:
            stockString = getStockQuoteString()
            if type(stockString) == str:
                stockInfo = getStockInfo(stockString)
                PLAYER.buy(stockInfo)     
#for if player clicks cancel, it just closes
            else: pass
        
#creates the box that asks what stock to sell, then calls the getNumberToSell,
#which it then uses to call the sell function
   def drawSellScreen(self):
#checks if portfolio is empty, if so prevents from trying to sell
        if PLAYER.portfolio == {}: displayNothingToSell()
        else:
#checks which stock player wants to sell
            message = '''What would you like to sell?
Please type in the number corresponding to the stock you would like to sell
                        '''
            title = "Selling"
            options = []
            for stock in PLAYER.portfolio: options.append(stock)
            response = choose(message, title, options)
#checks to see if input is correct type, then calls the sell function if it is 
            try:
                type(response) == str or type(response) == int
                stockNameAndPrice = (response, 
                PLAYER.pricesOfStocksBought[response])
                stockInfo = (response,PLAYER.pricesOfStocksBought[response],
                    getNumberToSell(stockNameAndPrice)) 
                PLAYER.sell(stockInfo)
#if the player clicks cancel just closes window
            except:
                pass
                
#creates the news class, which needs a player, canvas, and type as input
class News(object):
    
#creates each instance, default type of news to start is neutral
    def __init__(self,canvas,player, typeOfNews='Neutral'):
        self.type = typeOfNews
        self.canvas = canvas
        self.locX = 1000
        self.player = player
        
#creates the story based on the type of news, can be bad, good, or neutral
    def writeStory(self):
        if self.type == 'Bad':
            self.message = '%s did a terrible job today, people' % self.company
            self.message += ' are losing faith'
        elif self.type == 'Neutral':
            self.message = "%s didn't do anything special"  % self.company 
            self.message += ' today, nothing has changed'
        elif self.type == 'Good':
            self.message = '%s did a good job today' %self.company
            self.message += ' people are interested'
#moves the text across the screen to make a news ticker effect
        if self.locX >= 0:
            self.canvas.create_text(self.locX,0,text = self.message,
                                    font = '16',anchor = 'ne')
#5 is used to make each news story last 12 hours
            self.locX -= 5
   
#randomly chooses a company from those available in the game
    def pickRandomCompany(self):
        player = self.player
        number = random.randint(0,len(player.pricesOfStocksBought)-1)
        listOfStocks = []  
        for key in player.pricesOfStocksBought.items():
            listOfStocks.append(key)
        self.company = listOfStocks[number][0]
      
#randomly changes the type of the news story  
    def changeType(self):
        number = random.randint(0,2)
        if number == 0:
            self.type = 'Neutral'
        elif number == 1:
            self.type = 'Good'
        elif number == 2:
            self.type = 'Bad'

  #taken from class notes from David Kosbie
#http://www.kosbie.net/cmu/fall-11/15-112/handouts/misc-demos
#/src/dialogs-demo1.py      
 #modified to have try and except clauses to handle all inputs      
def choose(message, title, options):
    msg = message + "\n" + "Choose one:"
    for i in xrange(len(options)):
        msg += "\n" + str(i+1) + ": " + options[i]
    response = tkSimpleDialog.askstring(title, msg)
    try:
        int(response)
        return options[int(response)-1]
#makes it so if player clicks cancel it just closes window
    except:
        if type(response) != str:
            pass
#if type of input not correct it calls error window
        else:
            displayErrorMessage()
            
#default error message for when input isnt correct type
def displayErrorMessage():
    title = 'Sorry'
    message = "That's not a valid answer"
    tkMessageBox.showinfo(title,message) 
                                                     
#takes a player as input and creates the animation instance to run game
def stockMarketGame(player):
    game = Animation()
    game.run()
       
#makes the player, takes in a name as input
def createPlayer(): 
    name = raw_input('Please Enter Your Name Here: ')
    return Player(name)

#gets the string to use to search for stocks
def getStockQuoteString():
    title = 'Stock Search'
    message = 'What stock would you like to search for?'
    stock = tkSimpleDialog.askstring(title,message)    
    return stock

#gets the number of shares the player wants to sell    
def getNumberToSell(stockInfo):
    title = 'Selling %s' % stockInfo[0]
    message = 'How many would you like to sell at %.2f' % stockInfo[1]
    number = tkSimpleDialog.askstring(title,message) 
#checks to make sure the input is correct
    try:
        number = int(number)
        return number
#if player clicks cancel just closes window
    except:
        if type(number) != str or type(number) != int:
            pass
#if incorrect input it displays error
        else:
            displayErrorMessage()
    
#gets the number of stocks the player wants to buy   
def getNumberToBuy(stockInfo):
    title = 'Buying %s' % stockInfo[0]
    message = 'How many would you like to buy at %.2f' % stockInfo[1]
    number = tkSimpleDialog.askstring(title,message)
    PLAYER.priceBoughtAt[stockInfo[0]] = stockInfo[1]
#checks to make sure input is right type   
    try:
        number = int(number)
        return number
#if player clicks cancel it just closes
    except:
        pass

#gets the stock information needed, name and price, and number wanted to buy
def getStockInfo(stockString):
    stockData = searchYahoo(stockString)
    stockName = stockData[0]
    if stockName in PLAYER.pricesOfStocksBought.keys():
        stockData = (stockName,
        PLAYER.pricesOfStocksBought[stockName])
    stockInfo = (stockData[0],stockData[1],
                    getNumberToBuy(stockData))
    return stockInfo 
                                                                    
#scrapes the stock prices off of yahoo, used to search for new stock prices
#to be added to the game, also sets initial prices for the starting set
#of stocks
def searchYahoo(stock):
#checks to see if it can find on yahoo finance
    try:
        stockWebsite = ('http://finance.yahoo.com/q;_ylt=AgxzbXDD5dfwnKs50kV'
        'jeYyiuYdG;_ylu=X3oDMTBxdGVyNzJxBHNlYwNVSCAzIERlc2t0b3AgU2VhcmNoIDEx'
        ';_ylg=X3oDMTBsdWsyY2FpBGxhbmcDZW4tVVMEcHQDMgR0ZXN0Aw--;_ylv=3?s=%s&uh'
        'b=uhb2&type=2button&fr=uh3_finance_web_gs' % stock)
        soup = Soup(urllib2.urlopen(stockWebsite).read())
        stockStuff = str(soup.find(attrs='time_rtq_ticker'))
        quote = ''
        for c in stockStuff:
            if c in string.digits or c == '.':
                quote += c
        quote = quote[2:]
        price = float(quote)
        title = str(soup.title)[7:11]    
        stockInfo = (title,price)  
        return stockInfo
#if it cant find it returns error
    except:
        title = 'Error'
        message = 'Sorry we couldn\'t find that stock, please try again'
        tkMessageBox.showinfo(title,message)

#called if player tries to sell stocks but doesn't have any
def displayNothingToSell():
    title = 'Sorry'
    message = "You don't have any stocks to sell"
    tkMessageBox.showinfo(title,message)

#searches for the stock info for a few stocks to place in the market at the
#start of the game
STARTINGSTOCKS = {
'GOOG':searchYahoo('GOOG')[1],'AAPL':searchYahoo('AAPL')[1],
'MSFT':searchYahoo('MSFT')[1], 'HES':searchYahoo('HES')[1],
'WMT':searchYahoo('WMT')[1], 'F':searchYahoo('F')[1],
'TGT':searchYahoo('TGT')[1], 'HMC':searchYahoo('HMC')[1],
'FOX':searchYahoo('FOX')[1], 'NFLX':searchYahoo('NFLX')[1]
}     

#initializes the game
PLAYER = createPlayer()    
stockMarketGame(PLAYER)

################################Test Functions################################


def testingAllFunctions():
    testStocks = {'GOOG': 531,'AAPL': 200}
    testStocks2 = {'GOOG': 100}
    TESTPLAYER = Player('Test')
    print 'Testing all functions...',
    testBuy()
    print 'All functions have passed!'
    
def testBuy():
    TESTPLAYER.cash = 531
    TESTPLAYER.portfolio = {}
    TESTPLAYER.pricesOfStocksBought = testStocks
    testStockInfo = ('GOOG',531,1)
    testStockInfo2 = ('GOOG',100,1)
    print 'Testing the buy function...',
    TESTPLAYER.buy(testStockInfo)
    assert(TESTPLAYER.value == 531)
    assert(TESTPLAYER.cash == 0)
    TESTPLAYER.portfolio = {}
    TESTPLAYER.cash = 100
    TESTPLAYER.value = 0
    TESTPLAYER.pricesOfStocksBought = testStocks2
    testStockInfo = ('GOOG',100,1)
    TESTPLAYER.buy(testStockInfo2)
    assert(TESTPLAYER.value == 100)
    assert(TESTPLAYER.cash == 0)
    print 'Passed!'

def testSell():
    TESTPLAYER.portfolio = {'GOOG': 1}
    TESTPLAYER.pricesOfStocksBought
    
#testingAllFunctions()