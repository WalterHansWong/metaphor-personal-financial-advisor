from flask import Flask, render_template, request, redirect, url_for, session
from app import app
from app.financial_calculations import get_stock_articles, get_treasury_yield
from app.money_growth_graph import save_plot

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        dollar_amount = request.form.get('dollar_amount')
        timeframe = request.form.get('timeframe')
        timeframe_unit = request.form.get('timeframe_unit')

        # Convert the dollar amount and timeframe to appropriate data types
        try:
            dollar_amount = float(dollar_amount)
            timeframe = int(timeframe)
        except ValueError:
            # Handle invalid input (non-numeric, etc.)
            error = "Please enter valid numeric values."
            return render_template('index.html', error=error)

        # Convert timeframe to days if it's in years
        if timeframe_unit == 'years':
            timeframe = timeframe * 365  # Assuming 1 year = 365 days

        # TODO: process the data and generate the output
        # output is current interest rates at different banks
        # return on current GIC and government bonds
        # compared to benchmark S&P 500 growth (past x timeframe) for reference
        # articles from experts - the best stocks to buy today
        articles = get_stock_articles()
        session['articles'] = articles

        maturity, date, value = get_treasury_yield(timeframe=timeframe)
        save_plot(principal=dollar_amount, rate=float(value), maturity=maturity)
        session['treasury_yield'] = (maturity, date)

        filename = f"{dollar_amount}_{maturity}_graph.png"
        session['graph_filename'] = filename

        return redirect(url_for('output'))

    return render_template('index.html')

@app.route('/output')
def output():
    # TODO: code to display the output
    articles = session.get('articles', [])  # retrieve articles from session
    maturity, data = session.get('treasury_yield', (None, None))
    return render_template('output.html', articles=articles)

