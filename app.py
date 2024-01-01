from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    total_amount = db.Column(db.Float, default=0)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    type = db.Column(db.String(50))  # 'expense' or 'income'
    note = db.Column(db.String(200))  # Optional note

    def __repr__(self):
        return f'<Category {self.name}>'

# db.init_app(app)
# db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        category_name = request.form['category']
        amount = float(request.form['amount'])
        category_type = request.form['type']
        note = request.form.get('note', '')
        date_str = request.form.get('date', '')
        category = Category.query.filter_by(name=category_name).first()
        if date_str:
            date = datetime.strptime(date_str, '%Y-%m-%d')
        else:
            date = datetime.utcnow()

        if category:
            category.total_amount += amount
        else:
            new_category = Category(name=category_name, total_amount=amount, type=category_type, note=note, date=date)
            db.session.add(new_category)

        db.session.commit()

    categories = Category.query.all()
 
    expense_categories = Category.query.filter_by(type='expense').all()
    print(expense_categories)
    print([a.total_amount for a in expense_categories])
    income_categories = Category.query.filter_by(type='income').all()
    pie_data_expense = {
        "labels": [category.name for category in expense_categories],
        "values": [category.total_amount for category in expense_categories]
    }
    # print("HHHHHHHH")
    # print(pie_data_expense)
    pie_data_income = {
        "labels": [category.name for category in income_categories],
        "values": [category.total_amount for category in income_categories]
    }
    # Data preparation for Line Chart
    # This requires additional logic to accumulate data over time
    # return render_template('index.html', categories=categories)

    return render_template('index.html', categories=categories, pie_data_expense=pie_data_expense, pie_data_income=pie_data_income, line_chart_data=process_line())

def process_line():
    # Initialize default dictionaries to store aggregated data
    expenses_by_date = defaultdict(float)
    income_by_date = defaultdict(float)

    # Aggregate expenses and income by date
    expenses = Category.query.filter_by(type='expense').all()
    for expense in expenses:
        print(expense.date)
        date_str = expense.date.strftime('%Y-%m-%d')
        expenses_by_date[date_str] += expense.total_amount

    income = Category.query.filter_by(type='income').all()
    for inc in income:
        date_str = inc.date.strftime('%Y-%m-%d')
        income_by_date[date_str] += inc.total_amount

    # Prepare dates and values for the chart
    dates = sorted(set(expenses_by_date.keys()) | set(income_by_date.keys()))
    expense_values = [expenses_by_date[date] for date in dates]
    income_values = [income_by_date[date] for date in dates]

    line_chart_data = {
        "labels": dates,
        "expenses": expense_values,
        "income": income_values
    }
    return line_chart_data
if __name__ == '__main__':
    app.run(debug=True)
