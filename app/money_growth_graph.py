import matplotlib.pyplot as plt
import seaborn as sns
import os

plt.switch_backend('Agg')

def calculate_growth(principal, rate, months):
    """
    Calculates the growth of an investment.

    :param principal: initial amount of money invested.
    :param rate: monthly interest rate in decimal form.
    :param months: number of months the money is invested for.
    :return: a list representing the value of the investment at each month.
    """
    values = [principal]
    for month in range(1, months + 1):
        principal += principal * rate
        values.append(principal)
    return values

def save_plot(principal, rate, maturity):
    time_mapping = {
        '3month': 3,
        '2year': 24,
        '5year': 60,
        '7year': 84,
        '10year': 120,
        '30year': 360
    }

    months = time_mapping[maturity]

    # convert rate returned by API to monthly rate
    rate = (rate / 100) / 12 

    y_values = calculate_growth(principal, rate, months)
    x_values = list(range(months + 1))
    
    sns.set_style("darkgrid")

    plt.figure(figsize=(10, 6))
    plt.plot(x_values, y_values, marker='o')
    plt.title(f'Growth of a ${principal} Investment Over {months} Months at {rate*100:.2f}% Monthly Interest')
    plt.xlabel('Months')
    plt.ylabel('Investment Value ($)')
    plt.grid(True)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    IMAGE_DIR = os.path.join(BASE_DIR, 'static', 'images')
    # save the graph as a png with the format principal_months_graph.png
    plt.savefig(os.path.join(IMAGE_DIR, f"{principal}_{maturity}_graph.png"))
    plt.close()
