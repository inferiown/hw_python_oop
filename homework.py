import datetime as dt

# Setting time-based static variables we will need for calculators:
date_format = '%d.%m.%Y'
now = dt.datetime.now().strftime(date_format)
today_date = dt.datetime.strptime(now, date_format).date()


class Calculator:
    '''CashCalculator and CaloriesCalculator parent class.'''

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        todays_amount = 0
        for item in self.records:
            if item.date == today_date:
                todays_amount += item.amount
        return round(todays_amount, 2)

    def get_week_stats(self):
        # Setting variable for the date that was a week ago:
        week_ago = dt.datetime.today().date() - dt.timedelta(days=7)
        this_week_amount = 0
        for item in self.records:
            # If record date less than a week ago AND it's not in the future
            #    - adds item.amount to this_week_spent_amount:
            if (item.date >= week_ago) and (item.date <= today_date):
                this_week_amount += float(item.amount)
        return round(this_week_amount, 2)


class CashCalculator(Calculator):
    '''Cash calculator class.'''

    # Setting static variables for different currencies:
    USD_RATE = 73.4421
    EURO_RATE = 86.9114

    def get_today_cash_remained(self, currency):
        # Calling self.get_today_stats() to calculate remaining_cash:
        remaining_cash = self.limit - float(self.get_today_stats())
        currency_name = 'руб'

        # Generating a right cash amount and currency_name:
        if currency == 'eur':
            remaining_cash = remaining_cash / CashCalculator.EURO_RATE
            currency_name = 'Euro'
        elif currency == 'usd':
            remaining_cash = remaining_cash / CashCalculator.USD_RATE
            currency_name = 'USD'

        # Generating an answers prefix:
        if remaining_cash > 0:
            message = 'На сегодня осталось '
        elif remaining_cash == 0:
            return 'Денег нет, держись'
        else:
            message = 'Денег нет, держись: твой долг - '
            # Converting negative remaining_cash variable to positive value
            # for better visualization:
            remaining_cash = abs(remaining_cash)

        return (message + ('%.2f' % remaining_cash) + ' ' + currency_name)


class CaloriesCalculator(Calculator):
    '''Calories calculator class.'''

    def get_calories_remained(self):
        # Calling self.get_today_stats() to calculate remaining_calories:
        remaining_calories = self.limit - float(self.get_today_stats())

        if remaining_calories > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {int(remaining_calories)} кКал')
        else:
            return 'Хватит есть!'


class Record:
    '''Class that generates records for various calculators.'''

    def __init__(self, amount, comment, date=None):
        # Setting ifelse statement to
        # transform hand-written dates into datetime.date
        # or if no date was provided - setting current date:
        if date is None:
            date = today_date
        else:
            date = dt.datetime.strptime(date, date_format).date()

        self.date = date
        self.amount = amount
        self.comment = comment
