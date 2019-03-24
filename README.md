# BudgetTrackingTool
Frontend and backend for a simple budget tracking tool.

This is a flask applications that communicates with google sheets to enter stuff my family has bought, and keep track of how much is left in the bugdget for different items.

Setting up permissions and certificates with google sheets:

Taken from this video:

https://www.youtube.com/watch?v=vISRn5qFrkM&t=340s

# Setting up the server

There are a few environment variables you should set up on the server:

* SECRET_KEY - The secret key used by it's dangerous for certificate signing of forms.
* BUDGET_TRACKER_CERTIFICATE - The location of the google certificate for letting the site access google.
* BUDGET_TRACKER_APP_CONFIG - Should be set to "Production".