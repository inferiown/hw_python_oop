import datetime as dt


class Calculator:
    '''CashCalculator and CaloriesCalculator parent class.'''

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        # As we discussed, my first list comprehension :)
        date_now = dt.date.today()
        todays_amount = sum([item.amount for item
                             in self.records if item.date == date_now])
        return todays_amount

    def get_week_stats(self):
        # Setting variable for the date that was a week ago:
        # I've Decided to put date like that, probably not the best option
        date_now = dt.date.today()
        week_ago = date_now - dt.timedelta(days=7)
        # Another list comprehension!
        this_week_amount = sum([item.amount for item in self.records if
                               week_ago <= item.date <= date_now])
        return round(this_week_amount, 2)

    def remaining_stat_calculation(self):
        return self.limit - float(self.get_today_stats())


class CashCalculator(Calculator):
    '''Cash calculator class.'''

    # Setting those static variables because pytest fails
    # if they don't exist:
    USD_RATE = 73.19
    EURO_RATE = 86.47

    def get_today_cash_remained(self, currency):
        # Generating currencies list to get rid of if/else statements:
        # I made it as a link to the static variables because
        # pytest fails if I set cost in this block.
        currencies_list = {'rub': ('руб', 1),
                           'eur': ('Euro', CashCalculator.EURO_RATE),
                           'usd': ('USD', CashCalculator.USD_RATE)}
        # Using unpacking to get currency name and rate:
        currency_name, currency_rate = currencies_list[currency]
        # Calculating the amount of cash remaining.
        remaining_cash = round((self.remaining_stat_calculation()
                                / currency_rate), 2)
        # Generating an answers prefix:
        if remaining_cash > 0:
            message = 'На сегодня осталось'
        elif remaining_cash == 0:
            return 'Денег нет, держись'
        else:
            message = 'Денег нет, держись: твой долг -'
        # Converting negative remaining_cash variable to positive value
        # for better visualization:
            remaining_cash = abs(remaining_cash)
        return f'{message} {remaining_cash} {currency_name}'


class CaloriesCalculator(Calculator):
    '''Calories calculator class.'''

    def get_calories_remained(self):
        # Calling self.get_today_stats() to calculate remaining_calories:
        remaining_calories = int(self.remaining_stat_calculation())

        if remaining_calories > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {remaining_calories} кКал')
        else:
            return 'Хватит есть!'


class Record:
    '''Class that generates records for various calculators.'''

    def __init__(self, amount, comment, date=None):
        # Setting ifelse statement to
        # transform hand-written dates into datetime.date
        # or if no date was provided - setting current date:
        if date is None:
            date = dt.date.today()
        else:
            date = dt.datetime.strptime(date, '%d.%m.%Y').date()

        self.date = date
        self.amount = amount
        self.comment = comment
