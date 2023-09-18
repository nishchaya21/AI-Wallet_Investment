from flask import Flask, render_template, request
import random
import json
app = Flask(__name__)

class InvestmentRecommendationSystem:
    def __init__(self):
        self.stocks = {}
        # Load data from data.json
        with open('data.json', 'r') as json_file:
            self.stocks = json.load(json_file)
    
    def recommend_investments(self, amount, risk_tolerance, duration, target_amount=None):
        # Determine asset allocation based on risk tolerance
        if risk_tolerance == 'low':
            allocation = {'stocks': 0.2, 'fixed_deposit': 0.8}
        elif risk_tolerance == 'medium':
            allocation = {'stocks': 0.5, 'fixed_deposit': 0.5}
        elif risk_tolerance == 'high':
            allocation = {'stocks': 0.8, 'fixed_deposit': 0.2}
        else:
            return "Invalid risk tolerance level."
        
        # Calculate investment amounts
        stock_allocation = amount * allocation['stocks']
        
        # Calculate fixed deposit allocation with compound interest
        x = amount * allocation['fixed_deposit']
        fd_allocation = int(amount * allocation['fixed_deposit'] * (1 + 0.03) ** duration)
        
        recommendations = []
        rec_fd = []
        
        # Recommend stocks based on risk tolerance
        if stock_allocation > 0:
            for symbol, stock in self.stocks.items():
                if stock['risk'] == risk_tolerance:
                    expected_return = stock['return']
                    recommended_investment = {
                        'asset_type': 'Stock',
                        'symbol': symbol,
                        'name': stock['name'],
                        'allocation': stock_allocation,
                        'expected_return': int(stock_allocation*((1+expected_return)**duration))
                    }
                    recommendations.append(recommended_investment)
        
        # Recommend fixed deposits
        if x > 0:
            fd_recommendation = {
                'asset_type': 'Fixed Deposit',
                'allocation': x,
                'expected_return':fd_allocation
            }
            rec_fd.append(fd_recommendation)
        
        random.shuffle(recommendations)
        selected_recommendations = recommendations[:3]
        return selected_recommendations, rec_fd

# Create an instance of the InvestmentRecommendationSystem
recommendation_system = InvestmentRecommendationSystem()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        amount = float(request.form.get("amount"))
        risk_tolerance = request.form.get("risk_tolerance")
        duration = int(request.form.get("duration"))
        target_amount = float(request.form.get("target_amount"))
        recommendation_system = InvestmentRecommendationSystem()
        recommendations,rec_fd = recommendation_system.recommend_investments(amount, risk_tolerance, duration, target_amount)
        if recommendations:
            # Shuffle the recommendations list to make it random
            random.shuffle(recommendations)

            # Select only the first 3 recommendations
            selected_recommendations = recommendations[:3]
            selected_recommendations.sort(key=lambda x: x['expected_return'], reverse=True)
        else:
            selected_recommendations = []
        
        return render_template('index.html', selected_recommendations=selected_recommendations, rec_fd = rec_fd)

    return render_template('index.html', selected_recommendations=[], rec_fd=[])

if __name__ == "__main__":
    app.run(debug=True)