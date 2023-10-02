from flask import Flask, render_template, request, redirect, url_for
from app import app

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

        # Redirect to the output page TODO: output function and template
        return redirect(url_for('output'))

    return render_template('index.html')

@app.route('/output')
def output():
    # TODO: code to display the output
    return render_template('output.html')

