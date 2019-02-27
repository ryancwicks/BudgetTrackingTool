import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import os


CERTIFICATE_LOCATION=os.environ['BUDGET_TRACKER_CERTIFICATE']
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
        self._creds = ServiceAccountCredentials.from_json_keyfile_name(CERTIFICATE_LOCATION, self._scope)
        self._client = gspread.authorize(self._creds)
        self._spreadsheet = self._client.open("Budget")
        self._latest_expense_sheet = self._get_latest_expense_sheet()

    def _get_budget_summary(self):
        """
        Retrieve the budget summary dictionary
        """
        sheet = self._spreadsheet.sheet1
        records = sheet.get_all_records()[0]
        return records

    budget_summary = property(fget=_get_budget_summary)

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
        """
        now = str(datetime.datetime.now())
        row = [str(now), str(user), str(account), amount, "" if not notes else notes]
        self._latest_expense_sheet.append_row(row)



if __name__=="__main__":
    budget_spreadsheet = Spreadsheet()

    budget_spreadsheet.add_expense ("Ryan", "Animals", 50.12)

