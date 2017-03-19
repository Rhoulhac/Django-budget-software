import datetime

from django import test

from budget.models import Transaction, Category, Store


class TransactionManagerTest(test.TestCase):

    def setUp(self):
        self.store = Store.objects.create(name='StoreName')

    def test_gets_all_transactions_for_category(self):
        category = Category.objects.create()
        transaction1 = self.create_transaction(category)
        transaction2 = self.create_transaction(category)
        result = Transaction.objects.current_monthly_spending_by_category(category)
        self.assertEqual(2, len(result))
        self.assertEqual(result[0], transaction1)
        self.assertEqual(result[1], transaction2)

    def test_gets_only_transactions_for_specified_category(self):
        category1 = Category.objects.create(name='cat1')
        category2 = Category.objects.create(name='cat2')
        transaction1 = self.create_transaction(category1)
        self.create_transaction(category2)
        result = Transaction.objects.current_monthly_spending_by_category(category1)
        self.assertEqual(1, len(result))
        self.assertEqual(result[0], transaction1)

    def test_gets_only_this_month_by_category(self):
        category = Category.objects.create(name='cat1')
        date_past = datetime.date.today() - datetime.timedelta(days=100)
        date_now = datetime.date.today()
        date_future = datetime.date.today() + datetime.timedelta(days=100)
        self.create_transaction(category, date_past)
        transaction1 = self.create_transaction(category, date_now)
        self.create_transaction(category, date_future)
        result = Transaction.objects.current_monthly_spending_by_category(category)
        self.assertEqual(1, len(result))
        self.assertEqual(result[0], transaction1)

    def test_gets_all_current_by_all_categories(self):
        category1 = Category.objects.create(name='cat1')
        category2 = Category.objects.create(name='cat2')
        transaction1 = self.create_transaction(category1)
        transaction2 = self.create_transaction(category2)
        result = Transaction.objects.current_monthly_spending()
        self.assertEqual(2, len(result))
        self.assertEqual(result[0], transaction1)
        self.assertEqual(result[1], transaction2)

    def test_get_all_for_this_month(self):
        category = Category.objects.create(name='cat1')
        date_past = datetime.date.today() - datetime.timedelta(days=100)
        date_now = datetime.date.today()
        date_future = datetime.date.today() + datetime.timedelta(days=100)
        self.create_transaction(category, date_past)
        transaction1 = self.create_transaction(category, date_now)
        self.create_transaction(category, date_future)
        result = Transaction.objects.current_monthly_spending()
        self.assertEqual(1, len(result))
        self.assertEqual(result[0], transaction1)

    def create_transaction(self, category, date=None):
        return Transaction.objects.create(
            category=category,
            purchase_date=date or datetime.date.today(),
            amount='2.00',
            store=self.store
        )