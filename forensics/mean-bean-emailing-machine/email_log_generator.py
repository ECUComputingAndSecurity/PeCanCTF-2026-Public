import json, random, base64, uuid, datetime
from pathlib import Path

program_dir=Path(__file__).parent

file_path=Path(__file__).parent/"bean_co_email_logs.JSON"
employees=["Horatio Humberfloob","Daniel Dumpy","Alexander Axenson","Garby McGoopy","Kip Krenshaw","Frank Flump","Larry Larp","Sir Jason Jasonson", "Laura Lumperdink","Min Maxius","Chárlótté Gëtdównfrómthéré","Jasmine Jasperklump","Ebony Iverson","Nina Dorplop","Ningle Bimbus","Trisha Shwartz"]

spam_senders=["Bean Co competitor", "Bixby's Car Insurance", "Customer Complaints", "Bean Bros", "Captain Pinto", "Jennifa Lorense", "Prince"]

spam_subjects=["WIN FREE BEANPHONE", "Reel prinse need yuor help", "Your beans suck", "Car Insurance", "I will find you.", "It's cold"]

spam_bodies=["YOU WIN GET FREE BEANPHONE NOW", "Sned money I will pay back promise", "Your beans are worse than ours, give up Bean Co.", "334 Bean Street, Dogtown", 
             "I'm stuck in Antarctica please send help"]

spf_fail_attachment_names=["Bigger, Better, Bean", "Send money here", "Not malware, trust", "WIN FREE BEANPHONE"]



spam_domains=["betterbeans.co","pinto.me", "bixby.co", "bean.co", "realprince.ng", "beanbro.co", "celeb.aq", "pinto.me"]

#150 normal attachments
normal_attachment_names=[{"attachment_name":"Bean_Quarterly", "file_type":"pdf"}, 
                         {"attachment_name":"How've You Bean? Employee Wellness Survey", "file_type":"pdf"},
                         {"attachment_name":"Bean Farts: A Meta Analysis on Oligosaccharides and Leprosy", "file_type":"pdf"},
                         {"attachment_name":"Why Mung Beans are the Superior Bean", "file_type":"pdf"},
                         {"attachment_name":"How To Increase Bean Stock", "file_type":"pdf"}]

#50 suspicious
suss_attachment_names=[{"attachment_name":"Why I Secretly Hate Beans...", "file_type":".gz"},
                       {"attachment_name":"10 Secrets Big Bean Doesn't Want You to Know", "file_type":".gz"},
                       {"attachment_name":"Black Market Beans 4 Sale", "file_type":".gz"}]
#6 phishing emails
phishing_attachment_name=[{"attachment_name":"BIG BEAN EMERGENCY HELP", "file_type":".gz"}]

start_date=datetime.datetime(2025, 1, 1, 8, 0)

def b64_gibberish():
    return base64.b64encode(random.randbytes(4881)).decode()

email_logs=[]

#legitimate emails without attachments
for i in range(9000):
    sender=random.choice(employees)
    recipient=random.choice([employee for employee in employees if sender!=employee])
    email_logs.append({"message_id":f"<{uuid.uuid4()}@bean.co>",
                        "from":f"{sender}", 
                        "to":f"{recipient}",
                        "subject":random.choice(["How great are beans?", "Bean business is boomin",
                                                 "The beans have been real good to me lately", "You need to increase your bean numbers",
                                                "Bean Appreciation", "Bean Stock Growth Strategy", "Pinto"]),
                        "body":random.choice(["The bean business is good. I love beans", "You need to get your bean numbers up, those are rookie numbers", 
                                              "Beans continue to be excellent for Bean Co.", "We should celebrate our bean success",
                                              "Beans are the future and the bean business is thriving"]),
                        "attachment":None,
                        "spf":"pass", "dkim":"pass", "dmarc":"pass"})

#legitimate emails with attachments
for i in range(75):
    file_name=random.choice(normal_attachment_names)
    sender=random.choice(employees)
    recipient=random.choice([employee for employee in employees if sender!=employee])
    email_logs.append({"message_id":f"<{uuid.uuid4()}@bean.co>",
                        "from":f"{sender}", 
                        "to":f"{recipient}",
                        "subject":random.choice(["How great are beans?", "Bean business is boomin",
                                                 "The beans have been real good to me lately", "You need to increase your bean numbers",
                                                "Bean Appreciation", "Bean Stock Growth Strategy", "Pinto"]),
                        "body":f"Please review {file_name["attachment_name"]} " + random.choice(["The bean business is good. I love beans", "You need to get your bean numbers up, those are rookie numbers", 
                                              "Beans continue to be excellent for Bean Co.", "We should celebrate our bean success",
                                              "Beans are the future and the bean business is thriving"]),
                        "attachment":file_name, "data":b64_gibberish(),
                        "spf":"pass", "dkim":"pass", "dmarc":"pass"})

#spf fails
for i in range(75):
    file_name=random.choice(spf_fail_attachment_names)
    sender=random.choice(spam_senders)
    recipient=random.choice(employees)
    email_logs.append({"message_id":f"<{uuid.uuid4()}@{random.choice(spam_domains)}>",
                        "from":f"{sender}", 
                        "to":f"{recipient}",
                        "subject":random.choice(spam_subjects),
                        "body":random.choice(spam_bodies),
                        "attachment":file_name, "data":b64_gibberish(),
                        "spf":"fail", "dkim":"pass", "dmarc":"pass"})

#dkim fails
for i in range(75):
    file_name=random.choice(normal_attachment_names)
    sender=random.choice(employees)
    recipient=random.choice([employee for employee in employees if sender!=employee])
    email_logs.append({"message_id":f"<{uuid.uuid4()}@bean.co>",
                        "from":f"{sender}", 
                        "to":f"{recipient}",
                        "subject":random.choice(["How great are beans?", "Bean business is boomin",
                                                 "The beans have been real good to me lately", "You need to increase your bean numbers",
                                                "Bean Appreciation", "Bean Stock Growth Strategy", "Pinto"]),
                        "body":f"Please review {file_name["attachment_name"]}" + random.choice(["The bean business is good. I love beans", "You need to get your bean numbers up, those are rookie numbers", 
                                              "Beans continue to be excellent for Bean Co.", "We should celebrate our bean success",
                                              "Beans are the future and the bean business is thriving"]),
                        "attachment":file_name, "data":b64_gibberish(),
                        "spf":"pass", "dkim":"fail", "dmarc":"pass"})

email_logs.append({"message_id":f"<{uuid.uuid4()}@bbet.sc>",
                "from":"Big Bean Emergency Team", 
                "to":"Horatio Humberfloob",
                "subject":"BIG BEAN EMERGENCY",
                "body":"BIG BEAN EMERGENCY OPEN NOW",
                "attachment":phishing_attachment_name, "data":"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",
                "spf":"fail", "dkim":"fail", "dmarc":"pass"})

for i in range(2):
    random.shuffle(email_logs)

for i, email in enumerate(reversed(email_logs)):
    email["date"]=(start_date+datetime.timedelta(minutes=i * 5)).isoformat()

with open(program_dir/"bean_co_email_logs.json", "w") as fi:
    json.dump(email_logs, fi, ensure_ascii=False)

data=[]
with open(file_path, "r") as file:
    data=json.load(file)
print(data)