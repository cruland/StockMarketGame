The Stock Market Game -By Chris Ruland

Installation and Run Instructions:
The modules required to run the game are Beautiful Soup 4 (a web scraping module for Python) and MatPlotLib (a graphing utility).
Both of these are available through Canopy through searching in the package manager. The other imports listed in the .py file are
pre-packaged with python such as Tkinter, urllib2, random, etc.... To actually run the game first run the file
Stock Market Game Final V2.py in a python editor, wait for the program to finish pulling the stock data from the internet.
You will know it's ready to play when the game will ask for your name in the python interpreter. Enter name and hit enter, the
tkinter canvas will pop-up and the game is ready to begin.

Description:
This is a stock market simulator game that pulls stock market prices from the internet (Specifically Yahoo Finance),
and then puts this data into the game. From there it is modified in-game based on random chance to either
increase, decrease, stay the same, or if you're really lucky almost double. Stocks also have the potential to change
based on random news stories that are generated in-game. The player starts with $100,000 and the goal is to double the
amount and reach $200,000. Additionally, the player will lose if all of the cash is lost and there are no stocks in
the portfolio.