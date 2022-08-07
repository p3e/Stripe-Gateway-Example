import stripe,os,json,requests,sys,socket
def cls():
    os.system('cls')
cls()
live_key = "sk_live_key_here"
stripe.api_key = live_key
card_total = 0
card_invalid = 0
card_live = 0
cls()
print("Your key has been loaded: " + live_key +"\n")
file = open("cc.txt","r")
cards = file.readlines()
file.close()
for line in cards:
    card_total +=1
print("Card loaded : " + str(card_total))
for cc in cards:
    cc = cc.strip()
    data = cc.split("|")
    number = data[0]
    exp_month = int(data[1])
    exp_year = int(data[2])
    cvc = data[3]
    try:
        client = stripe.Token.create(
            card={
                'number': number,
                'exp_month': exp_month,
                'exp_year': exp_year,
                'cvc': cvc,
                },
        )
        pay = stripe.Charge.create(
            amount=100,
            currency="usd",
            source=client['id'],
            description="Test Charge"
        )
        info = json.loads(str(pay))
        try:
            why = info['error']
        except KeyError:
            print("-----------------------------------------------------")
            print('[+] ACTIVE : ' +cc)
            print("[i] MESSAGE : " +info['outcome']['seller_message'])
            print("[i] RISK : " +info['outcome']['risk_level'] +" | Score: "+str(info['outcome']))
            print("-----------------------------------------------------\n")
            card_live+=1
    except stripe.error.CardError:
        print("[!] Card/Stripe Error\n")
        card_invalid+=1
ratio = card_live/card_total*100
cls()
print("                     [STATS]")
print("-----------------------------------------------------")
print("Total Cards : "+str(card_total))
print("Active : "+str(card_live)) 
print("Invalid : "+str(card_invalid))
print("Active Ratio : "+str(ratio)[:4]+"%")
print("-----------------------------------------------------")
