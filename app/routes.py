from flask import render_template, request, redirect, url_for, session
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

        # TODO: add more alternatives to compare such as:
        # current savings account interest rates at different banks
        # current CD rates
        # predicted performance of relevant index/mutual funds, stock market indices
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
    articles = session.get('articles', [])  # retrieve articles from session

    maturity, date = session.get('treasury_yield', (None, None))

    readable_equivalents = {
        '3month': '3 months',
        '2year': '2 years',
        '5year': '5 years',
        '7year': '7 years',
        '10year': '10 years',
        '30year': '30 years'
    }
    # default to raw maturity if not found in the dictionary
    readable_maturity = readable_equivalents.get(maturity, maturity)

    return render_template('output.html', articles=articles, maturity=readable_maturity, date=date)
