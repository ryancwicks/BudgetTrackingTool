import gspread
from oauth2client.service_account import ServiceAccountCredentials
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



if __name__=="__main__":
    budget_spreadsheet = Spreadsheet()

    #budget_spreadsheet.add_expense ("Ryan", "Groceries", 50.12)
    #budget_spreadsheet.add_expense ("Marja", "Groceries", 100.12)
    #budget_spreadsheet.add_expense ("Marja", "Clothes", 49.99, "Tessa's coat.")

    print(budget_spreadsheet.budget_current)

