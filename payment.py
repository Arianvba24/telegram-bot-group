import stripe
import pandas as pd



def payment_fetch():

    stripe.api_key = "YOUR_TOKEN"
    bank_digits = []
    name = []
    estado = []

    bank_data = {

        "Digits" : bank_digits,
        "Name" : name,
        "Estado" : estado

    }


    charges = stripe.Charge.list()

    for charge in charges.auto_paging_iter():
        card = charge.payment_method_details.card
        # print(f"ID: {charge.id}")
        # print(f"Monto: {charge.amount / 100:.2f} {charge.currency.upper()}")
        

        # print(f"Marca: {card.brand}")
        # print(f"Últimos 4 dígitos: {card.last4}")
        bank_digits.append(card.last4)
        # print(f"Tipo: {card.funding}")  # credit, debit, prepaid
        # print(f"Nombre del titular: {charge.billing_details.name}")
        name.append(charge.billing_details.name)
        # print(f"Estado: {charge.status}")
        estado.append(charge.status)
        # print("-" * 30)

    df = pd.DataFrame(bank_data)

    df["Digits"] = df["Digits"].astype(str)

    return df

df = payment_fetch()

print(df)
print(df.info())