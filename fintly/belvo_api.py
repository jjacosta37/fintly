from belvo.client import Client
from belvo.enums import AccessMode
from belvo.exceptions import RequestError
from fintly_back.models import Transaction
from fintly import settings
from datetime import date, timedelta
import time


# Choose Enviroment
BELVO_ENV = settings.BELVO_ENV


if BELVO_ENV == "sandbox":
    secretKey = settings.SAND_SECRET_KEY
    secretPass = settings.SAND_SECRET_PASS
    URL = "https://sandbox.belvo.com"
elif BELVO_ENV == "development":
    secretKey = settings.DEV_SECRET_KEY
    secretPass = settings.DEV_SECRET_PASS
    URL = "https://development.belvo.com"



# Generate access token for connect widget
def generateToken():
    client = Client(secretKey, secretPass, URL)
    token = client.WidgetToken.create()
    return token


#  POST call Get all transactions associated with a link

def post_transactions(link_id):
    # Login to Belvo API
    client = Client(secretKey, secretPass, URL)
    end_date = date.today().strftime("%Y-%m-%d")
    start_date = (date.today() - timedelta(days=180)).strftime("%Y-%m-%d")

    transactions = client.Transactions.create(
        link=link_id,
        date_from=start_date,
        date_to=end_date
    )
    return transactions

#  GET call Get all transactions associated with a link

def get_transactions(link_id):
    transactions = []
    client = Client(secretKey, secretPass, URL)
    start_date = (date.today() - timedelta(days=90)).strftime("%Y-%m-%d")
    accounts = get_accounts(link_id)
    
    for account_id in accounts:
        max_retries = 4
        retry_count = 0
        delay = 3
        
        while retry_count <= max_retries:
            try:
                iterator = client.Transactions.list(
                link=link_id,
                account=account_id,
                value_date__gte=start_date,
                )
                for transaction in iterator:
                    transactions.append(transaction)
                break
                    
            except Exception as e:
                if retry_count >= max_retries:
                    raise e
                else:
                    retry_count +=1
                    print(f"Error on retry {retry_count}: {e}")
                    time.sleep(delay)
                    delay *= 2  
        
    return transactions# Double the delay time after each retry
    


#  POST Call to get balances associated with a link

def post_balances(link_id):
    client = Client(secretKey, secretPass, URL)
    # Retrieve accounts
    accounts = client.Accounts.create(link=link_id)
    lst = [{'institution':item['institution']['name'],
            'category':item['category'],
            'name':item['name'] or "",
            'bank_product_id':item['bank_product_id'] or "",
            'public_identification_value':item['public_identification_value'] or "",
            'balance':item['balance']['current']
    }
           for item in accounts]
    return lst

# GET call to get balances

def get_balances(link_id):
    accounts = []
    client = Client(secretKey, secretPass, URL)  
    try:
        iterator = client.Accounts.list(
        link=link_id,
        raise_exception = True, # Set this optional paramter
        )
        for account in iterator:
            accounts.append(account)

    except RequestError as e:
        print(e)
    else:
        lst = [{'institution':item['institution']['name'],
            'category':item['category'],
            'name':item['name'] or "",
            'bank_product_id':item['bank_product_id'] or "",
            'public_identification_value':item['public_identification_value'] or "",
            'balance':float(item['balance']['current'])
    }
           for item in accounts]
        return lst
    
# Get Accounts
def get_accounts(link_id):
    
    # Function to reorganize accounts list so that credit cards and loan accounts are last
    def reorganize_accounts(lst):
        lst_no_credit_loan = [item for item in lst if item['category'] not in ['CREDIT_CARD', 'LOAN_ACCOUNT']]
        lst_credit_loan = [item for item in lst if item['category'] in ['CREDIT_CARD', 'LOAN_ACCOUNT']]
        
        return lst_no_credit_loan + lst_credit_loan
    
    # Get accounts from belvo and return list. Reorganize list so credit card and loan accounts are last
    accounts = []
    client = Client(secretKey, secretPass, URL)  
    max_retries = 4
    retry_count = 0
    delay = 3
    
    while retry_count <= max_retries:
        try:
            iterator = client.Accounts.list(
            link=link_id,
            raise_exception = True, # Set this optional paramter
            )
            for account in iterator:
                accounts.append(account)
            accounts = reorganize_accounts(accounts)
            lst = [item['id'] for item in accounts]
            return lst
        except Exception as e:
            if retry_count >= max_retries:
                raise e
            else:
                retry_count +=1
                print(f"Error on retry {retry_count}: {e}")
                time.sleep(delay)
                delay *= 2  
            
           


#  Save transactions JSON to Database

def addTransactionsToDB(transactions, user):

    for i in range(len(transactions)):

        # Checking that the transaction does not exist already
        if (Transaction.objects.filter(belvo_id=transactions[i]['id']).exists() == False):
            
            # Marking all savings and checkings accounts inflows as income
            # Adding category to transactions with None or Unknown category
            cat = 'Income & Payments' if transactions[i]['account']['category'] in ['SAVINGS_ACCOUNT', 'CHECKING_ACCOUNT'] and (transactions[i]["type"]=='INFLOW') else ('N/A' if transactions[i]['category'] in [None, 'Unknown'] else transactions[i]['category'])

             
            # Check debit outflows for credit card payments and loan payments with mark_credit_card_payment function
            isTransaction = False    
            if (transactions[i]['account']['category'] in ['CREDIT_CARD', 'LOAN_ACCOUNT']) and (transactions[i]["type"]=='INFLOW'):
                isTransaction = mark_credit_card_payment(transaction=transactions[i], user=user)
            
            # Check for credit card payments with is_transaction_accounts_movement function    
            isTransaction = True if is_transaction_accounts_movement(transactions[i]['description']) == True else isTransaction
                

            tranObject = Transaction(
                user_id=user,
                belvo_id=transactions[i]['id'],
                amount=transactions[i]["amount"],
                type=transactions[i]["type"],
                institution_name=transactions[i]['account']['institution']['name'],
                bank_product_id=transactions[i]['account']['bank_product_id'] or "",
                product_name=transactions[i]['account']['name'] or "",
                product_number=transactions[i]['account']['public_identification_value'] or "",
                acc_category=transactions[i]['account']['category'],
                currency=transactions[i]['account']['currency'],
                transaction_date=transactions[i]['value_date'],
                description=transactions[i]['description'] or "",
                category=cat,
                isTransaction=isTransaction
            )
            tranObject.save()




# Function to determine whether a transaction is an account movement using list with descriptions of transaction. Returns true or false
def is_transaction_accounts_movement(description):
    
    strings_tuple = ('PAGO SUC VIRT TC',
                    'ABONO SUCURSAL VIRTUAL',
                    'ABONO DEBITO AUTOMATIC',
                    'PAGO AUTOM TC')
    
    return description.startswith(strings_tuple)


# Function to determine whether a transaction is credit card payments. It takes credit card payments and looks for transactions with the exact same value. Returns true if it is a credit card transaction and false if not
def mark_credit_card_payment(transaction, user):
    if (Transaction.objects
        .exclude(acc_category='CREDIT_CARD')
        .filter(user_id=user, amount=transaction["amount"]).exists() == True):
        transaction_to_edit = Transaction.objects.get(user_id=user, amount=transaction["amount"])
        transaction_to_edit.isTransaction = True
        transaction_to_edit.save()
        return True
    return False
        
    


def delete_user_links(links):
    client = Client(secretKey, secretPass, URL)
    for i in links:
        client.Links.delete(i['link_id'])
        
