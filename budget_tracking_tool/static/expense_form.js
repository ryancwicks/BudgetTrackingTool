'use strict';

var ExpenseFormApp = (function() {

    const api_update_table="/api/v1/budget/";
    const api_submit_expense="/api/v1/add_expense/";

    let clear_flash_message = function(){
        let flash_div = document.getElementById("alert_field");
        while (flash_div.firstChild) {
            flash_div.removeChild (flash_div.firstChild);
        }
    };

    let flash_message = function(message) {
        clear_flash_message();
        let flash_div = document.getElementById("alert_field");
        let text = document.createElement("p");
        text.innerHTML = message;
        flash_div.appendChild(text);
    }

    let clear_budget_table = function(){
        let expense_table = document.getElementById("expense_table");
        while (expense_table.firstChild) {
            expense_table.removeChild(expense_table.firstChild);
        }
        let account_select = document.getElementById("account_select");
        while (account_select.firstChild) {
            account_select.removeChild(account_select.firstChild);
        }
    }

    let update_budget_table = async function() {
        flash_message("Updating budget table...");
        let raw_response;
        try {
            raw_response = await fetch (api_update_table, {
                method: "GET",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            });
        } catch (err) {
            flash_message("Failed to load budget table.");
            console.log(err);
            return;
        };
        let response;
        try {
            response = await raw_response.json();
        } catch (err) {

            flash_message("Failed to parse budget table.");
            console.log(err);
            return;
        }

        clear_budget_table();
        clear_flash_message();

        let expense_table = document.getElementById("expense_table");
        let first_row = document.createElement("tr");
        let account_head = document.createElement("th");
        let amount_head = document.createElement("th");
        account_head.innerHTML = "Account";
        amount_head.innerHTML = "Remaining ($)";
        first_row.appendChild(account_head);
        first_row.appendChild(amount_head);
        expense_table.appendChild(first_row);

        let account_select = document.getElementById("account_select");

        Object.keys(response).forEach(
            function(key) {
                let row = document.createElement("tr");
                let account = document.createElement("td");
                let amount = document.createElement("td");
                account.innerHTML = key;
                amount.innerHTML = response[key].toLocaleString('en');
                let value = Number(response[key]);
                if (value >= 0) {
                    amount.style="color:green";
                } else {
                    amount.style="color:red";
                }
                
                row.appendChild(account)
                row.appendChild(amount)
                expense_table.appendChild(row)

                let account_option = document.createElement("option");
                account_option.value = key
                account_option.innerHTML = key
                account_select.appendChild(account_option);
            });
    };

    let submit_expense = async function () {

        flash_message("Updating Expense...")
        //Get the account field.
        let account_select = document.getElementById("account_select")
        let account = account_select.options[account_select.options.selectedIndex].text;
        //Get the amount field.
        let amount = document.getElementById("cost").value;
        document.getElementById("cost").value = 0;
        //Get the notes.
        let notes = document.getElementById("notes").value;
        document.getElementById("notes").value = ""

        try {
            let raw_response = await fetch(api_submit_expense, {
                method: "POST",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify ({
                    account: account,
                    amount: amount,
                    notes: notes
                })
            })
        } catch (err) {
            flash_message ("Could not submit expense.");
            console.log(err);
            return;
        }
        flash_message ("Successfully submitted expense.")
        await update_budget_table();
    };

    return {
        update_budget_table: update_budget_table,
        submit_expense: submit_expense
    };
});

var ExpenseForm = ExpenseFormApp();

ExpenseForm.update_budget_table();

var submit_button = document.getElementById("submit");
submit_button.addEventListener("click", ExpenseForm.submit_expense);

var amount_field = document.getElementById("cost");
amount_field.addEventListener("focus", ()=>{amount_field.value = "";});
