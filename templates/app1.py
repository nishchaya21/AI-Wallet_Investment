from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class InvestmentRecommendationSystem:
    def __init__(self):
        self.stocks = {
            'AAPL': {'name': 'Apple Inc.', 'risk': 'high', 'return': 0.1},
            'GOOGL': {'name': 'Alphabet Inc.', 'risk': 'medium', 'return': 0.08},
            'MSFT': {'name': 'Microsoft Corporation', 'risk': 'medium', 'return': 0.09},
            # Add more stocks and their attributes here
        }
    
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
        fd_allocation = fd_allocation = int(amount * allocation['fixed_deposit'] * (1 + 0.03) ** duration)
        
        recommendations = []
        
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
        if fd_allocation > 0:
            fd_recommendation = {
                'asset_type': 'Fixed Deposit',
                'allocation': fd_allocation
            }
            recommendations.append(fd_recommendation)
        
        return recommendations

# Create an instance of the InvestmentRecommendationSystem
recommendation_system = InvestmentRecommendationSystem()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        amount = float(request.form.get("amount"))
        risk_tolerance = request.form.get("risk_tolerance")
        duration = int(request.form.get("duration"))
        target_amount = float(request.form.get("target_amount"))
        
        recommendations = recommendation_system.recommend_investments(amount, risk_tolerance, duration, target_amount)
        return jsonify(recommendations)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
