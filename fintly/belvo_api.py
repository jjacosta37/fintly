from belvo.client import Client
from belvo.enums import AccessMode
from belvo.exceptions import RequestError
from fintly_back.models import Transaction
from fintly import settings
from datetime import date, timedelta

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
        iterator = client.Transactions.list(
        link=link_id,
        account=account_id,
        value_date__gte=start_date,
        )
        for transaction in iterator:
            transactions.append(transaction)
    return transactions    
    


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
            'balance':item['balance']['current']
    }
           for item in accounts]
        return lst
    
# Get Accounts
def get_accounts(link_id):
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
        lst = [item['id'] for item in accounts]
        return lst


#  Save transactions JSON to Database

def addTransactionsToDB(transactions, user):

    for i in range(len(transactions)):

        if (Transaction.objects.filter(belvo_id=transactions[i]['id']).exists() == False):

            if (transactions[i]['category'] == None or transactions[i]['category'] == "Unknown"):
                cat = 'N/A'
            else:
                cat = transactions[i]['category']

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
                isTransaction=is_transaction_accounts_movement(transactions[i]['description'])
            )
            tranObject.save()




# Function to determine whether a transaction is an account movement
def is_transaction_accounts_movement(description):
    
    strings_tuple = ('PAGO SUC VIRT TC',
                    'ABONO SUCURSAL VIRTUAL',
                    'ABONO DEBITO AUTOMATIC',
                    'PAGO AUTOM TC')
    
    return description.startswith(strings_tuple)


def delete_user_links(links):
    client = Client(secretKey, secretPass, URL)
    for i in links:
        client.Links.delete(i['link_id'])
        
