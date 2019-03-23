import gspread
from oauth2client.service_account import ServiceAccountCredentials
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin, login_manager
import datetime
import os
from .config import config

BUDGET_SHEET="Budget"
EXPENSE_TEMPLATE="ExpenseTemplate"

class Spreadsheet(object):
    """
    Spreadsheet interface to google drive budget spreadsheet.
    """
    def __init__(self):
        """
        Initialization code for budget spreadsheet.
        """
        self._scope = ['https://spreadsheets.google.com/feeds',
                       'https://www.googleapis.com/auth/drive']
        self._creds = ServiceAccountCredentials.from_json_keyfile_name(config['default'].CERTIFICATE_LOCATION, self._scope)
        self._client = gspread.authorize(self._creds)
        self._spreadsheet = self._client.open("Budget")

class Budget(Spreadsheet):
    """
    Subclass of spreadsheet for accessing the budget items of the spreadsheet.
    """

    def __init__(self):
        super().__init__()

    def _get_budget_total(self):
        """
        Retrieve the budget summary dictionary
        """
        sheet = self._spreadsheet.sheet1
        records = sheet.get_all_records()[0]
        return records

    def _get_budget_current(self):
        """
        Get the current total budget and expenses and calculate the current budget remaining.
        """
        total_budget = self._get_budget_total()
        current_month_expenses = self._get_latest_expense_sheet().get_all_records()

        for item in current_month_expenses:
            try:
                total_budget[item["Account"]] -= item["Amount"]
            except:
                print ("Mismatched accounts")

        return total_budget

    budget_total = property(fget=_get_budget_total)
    budget_current = property(fget=_get_budget_current)

    def _get_latest_expense_sheet(self):
        """
        Get a sheet reference to the latest months expense sheet. Persistent
        for the instance of the class.
        """
        sheet_name = self._get_current_month_worksheet_name()
        try:
            latest = self._spreadsheet.worksheet(sheet_name)
        except gspread.exceptions.WorksheetNotFound:
            template = self._spreadsheet.worksheet(EXPENSE_TEMPLATE)
            header = template.get_all_values()[0]
            latest = self._spreadsheet.add_worksheet(sheet_name, len(header), 0)
            latest.append_row(header)
        
        return latest

    @staticmethod
    def _get_current_month_worksheet_name():
        """
        Get the current months sheets name (based on current datetime.)
        """
        today = datetime.date.today()
        return today.strftime('%Y-%b')

    def add_expense(self, user, account, amount, notes=None):
        """
        Add an expense to the sheet.
        """
        budget_sheet = self.budget_total
        if not account in budget_sheet.keys():
            raise RuntimeError ("Account {} is not part of the budget.".format(account))
        expense_sheet = self._get_latest_expense_sheet()
        now = str(datetime.datetime.now())
        row = [str(now), str(user), str(account), amount, "" if not notes else notes]
        expense_sheet.append_row(row)

class User(Spreadsheet):
    """
    Spreadsheet interface to get user information and authenticate.
    """
    USERS_TABLE="Users"

    def __init__(self, username):
        """
        Implements the Flask-Login methods.
        """
        super().__init__()
        self._username = username
        table = self._spreadsheet.worksheet(self.USERS_TABLE).get_all_records()
        matching_users = list(filter(lambda person: person["User"]==self._username, table))
        self.is_authenticated = False
        self.is_anonymous = False
        if len(matching_users) == 0:
            self.is_active = False
            self._password_hash = None
            return
        
        self.is_active = True
        self._password_hash = matching_users[0]["Password"]
    
    def get_id(self):
        return self._username
        
    def _verify_password(self, password):
        if not self.is_active:
            return False
        return check_password_hash(self._password_hash, password)

    def authenticate_user(self, password):
        """
        Authenticate the user and password from the users table.
        """
        if not self.is_active:
            return False
        if not self._verify_password (password):
            return False
        return True   

    @staticmethod
    def generate_password(password):
        """
        Generate a password hash to be put into the spreadsheet manuall
        """
        return generate_password_hash(password)

    def generate_auth_token(self, expiration):
        """
        Generate a time limited token and encode the username under the field id.
        """
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self._username}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        """
        Verify that the token that was encoded with the secret key unpacks to generate the correct id/username.
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except: 
            return None
        return data['id']

@login_manager.user_loaded_from_request
def load_user(user_id):
    return User(user_id)


if __name__=="__main__":
    #budget_spreadsheet = Budget()

    #budget_spreadsheet.add_expense ("Ryan", "Groceries", 50.12)
    #budget_spreadsheet.add_expense ("Marja", "Groceries", 100.12)
    #budget_spreadsheet.add_expense ("Marja", "Clothes", 49.99, "Tessa's coat.")

    #print(budget_spreadsheet.budget_current)
    
    #print(User.generate_password("wrong_password"))
    user_spreadsheet = User("Ryan")

    print(user_spreadsheet.authenticate_user("bad_password"))
    print (user_spreadsheet.authenticate_user("does not exist"))

    user_spreadsheet = User("Marja")
    print (user_spreadsheet.authenticate_user("wrong_password"))
    
    user_spreadsheet = User("Tim")
    print (user_spreadsheet.authenticate_user("No tim here."))

