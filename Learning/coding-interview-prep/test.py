def filter_transactions(transactions: list) -> dict:
    category = {}
    greaterThan100 = {}
    for transaction in transactions:
        type , amount = transaction
        category.setdefault(type,[]).append(amount)
                
    for key,val in category.items():
        if sum(val) > 100:
           greaterThan100[key] = val

    return greaterThan100

print(filter_transactions([('food',60),('transport',30),('food',80),('transport',20),('food',10)]))