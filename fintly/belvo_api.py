from belvo.client import Client
from fintly_back.models import Transaction
from fintly import settings
from datetime import date, timedelta

# Choose Enviroment
BELVO_ENV = settings.BELVO_ENV


# TODO: Store keys in Env Variables
if BELVO_ENV == "sandbox":
    secretKey = settings.SAND_SECRET_KEY
    secretPass = settings.SAND_SECRET_PASS
    url = "https://sandbox.belvo.com"
elif BELVO_ENV == "development":
    secretKey = settings.DEV_SECRET_KEY
    secretPass = settings.DEV_SECRET_PASS
    url = "https://development.belvo.com"



#  Get all transactions associated with a link

def getTransactions(link_id):
    # Login to Belvo API
    client = Client(secretKey, secretPass, url)
    end_date = date.today().strftime("%Y-%m-%d")
    start_date = (date.today() - timedelta(days=180)).strftime("%Y-%m-%d")

    transactions = client.Transactions.create(
        link=link_id,
        date_from=start_date,
        date_to=end_date
    )
    return transactions


# Generate access token for connect widget
def generateToken():
    client = Client(secretKey, secretPass, url)
    token = client.WidgetToken.create()
    return token


#  Save transactions JSON to Database

def addTransactionsToDB(transactions, user):

    for i in range(len(transactions)):

        if (Transaction.objects.filter(belvo_id=transactions[i]['id']).exists() == False):

            if (transactions[i]['category'] == None):
                cat = 'N/A'
            else:
                cat = transactions[i]['category']

            tranObject = Transaction(
                user_id=user,
                belvo_id=transactions[i]['id'],
                amount=transactions[i]["amount"],
                type=transactions[i]["type"],
                institution_name=transactions[i]['account']['institution']['name'],
                bank_product_id=transactions[i]['account']['bank_product_id'],
                product_name=transactions[i]['account']['name'],
                product_number=transactions[i]['account']['public_identification_value'],
                acc_category=transactions[i]['account']['category'],
                currency=transactions[i]['account']['currency'],
                transaction_date=transactions[i]['value_date'],
                description=transactions[i]['description'],
                category=cat,
                isTransaction=is_transaction_accounts_movement(transactions[i]['description'])
            )
            tranObject.save()


#  Get balances associated with a link

def get_balances(link_id):
    client = Client(secretKey, secretPass, url)
    # Retrieve accounts
    accounts = client.Accounts.create(link=link_id)
    lst = [{'institution':item['institution']['name'],
            'category':item['category'],
            'name':item['name'],
            'bank_product_id':item['bank_product_id'],
            'public_identification_value':item['public_identification_value'],
            'balance':item['balance']['current']
    }
           for item in accounts]
    return lst

# Function to determine whether a transaction is an account movement
def is_transaction_accounts_movement(description):
    
    strings_tuple = ('PAGO SUC VIRT TC',
                    'ABONO SUCURSAL VIRTUAL',
                    'ABONO DEBITO AUTOMATIC',
                    'PAGO AUTOM TC')
    
    return description.startswith(strings_tuple)