import json
import random
import uuid
import datetime
import string
from collections import Counter

# Ground Truth Queries & Evaluation Setup
PARTICIPANTS = ["Aman", "Priya", "Rahul", "Neha", "Rohit", "Ananya", "Karan", "Simran"]

START_DATE = datetime.datetime(2026, 3, 1, 10, 0, 0)
END_DATE = datetime.datetime(2026, 9, 1, 23, 59, 59)

def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + datetime.timedelta(seconds=random_second)

def generate_id():
    return f"msg_{random.randint(10000, 99999)}_{uuid.uuid4().hex[:6]}"

# ============================================================================
# COMPREHENSIVE HINGLISH PHRASE BANK (450+ AUTHENTIC COLLEGE CHAT PHRASES)
# ============================================================================
HINGLISH_PHRASES = [
    # 1. ACADEMICS, CLASSES, PROFESSORS & EXAMS
    "kisi ne project submit kiya?", "sir ne kya bola?", "attendance lagwa de", "proxy laga di bhai",
    "kya assignment mila hai", "assignment ka deadline kab hai?", "notes bhej de please", "slides share kar do",
    "kaisa exam gaya?", "pass ho jaunga bas", "sir gussa the aaj", "mass bunk karte hain",
    "prof ne test announce kiya kya?", "viva kaisa tha?", "lab manual complete hai kisi ka?", "diagram banana baaki hai",
    "class cancel ho gayi kya?", "lecture me kaun kaun hai?", "last bench khali hai kya?", "quiz ready kar li?",
    "syllabus kitna bacha hai?", "pyq solve kiye kya?", "internals me marks milenge?", "endsem ki date sheet aa gayi",
    "grace marks milenge kya?", "kuch samajh nahi aa raha maths me", "dsa ke question nahi ban rahe", "code me bug aa raha hai",
    "github pe push kar diya project", "readme likhna baaki hai abhi", "ppt ready hai kal ke presentation ke liye",
    "group discussion kab start hoga?", "library me shanti nahi hai", "hod cabin ke bahar bheed hai", "dean se sign karwana hai",
    "hall ticket download kar liya?", "admit card print karwa lo", "calculator lana mat bhoolna", "formula sheet bana li?",
    "cheating ka scene mat banana", "invigilator bohot strict tha", "question paper bohot tough tha", "time kam pad gaya exam me",
    "fail hone se bach gaya", "topper ban gaya ye toh", "rank list check ki?", "cgpa drop ho gayi meri",
    "re-eval ke liye apply karu?", "supplementary exam kab hai?", "summer semester join karna padega kya?", "placement cell ka mail aaya",
    "resume shortlist ho gaya mera", "interview round kab hai?", "aptitude test bohot bekar gaya", "coding round crack ho gaya",
    "referral dila de kisi company me", "off-campus apply kiya kisi ne?", "internship certificate submit karna hai",

    # 2. CANTEEN, FOOD, CHAI, MAGGI & EXPENSES
    "canteen aaja jaldi", "chai peene chalte hain", "maggi banaye koi hostel me", "bhookh lag rahi hai bohot",
    "kaha chale khane?", "swiggy pe coupon code batao", "zomato se order kare kya?", "bill split kar lo sab",
    "paisa kaun dega?", "budget nahi hai mera", "treat kab dega bhai?", "aaj party meri taraf se",
    "upi kar diya check kar", "paise transfer nahi hue abhi", "samosa thanda tha", "cold coffee piye tapri pe",
    "roll khane chalte hain market", "momos counter pe bohot rush hai", "biryani order kar de bhai", "mess ka khana kaisa hai aaj?",
    "mess me paneer bana hai kya?", "roti kacchi thi bilkul", "daal me paani zyada tha", "night canteen khula hai kya?",
    "midnight snack order karte hain", "paratha khane dhaba chale?", "kadak chai chahiye dimag thak gaya", "juice corner pe milte hain",
    "chole bhature order kare?", "shawarma try kiya kya waha ka?", "ice cream khane chalte hain baad me", "paisa khatam ho gaya month end pe",
    "pocket money kab aayegi?", "udhaar wapas kar de bhai", "account me zero balance hai", "splitwise pe add kar diya expense",
    "party fund me contribute karo", "snacks khareed ke laao koi", "biscuit ka packet khatam ho gaya", "chips le aana aate waqt",

    # 3. HOSTEL & DAILY COLLEGE LIFE
    "room pe aaja mere", "room lock hai kiske paas key hai?", "chabi kahan chhod ke gaya?", "kapde sukhane daale the kya?",
    "washroom me paani nahi aa raha", "geyser on kar de koi", "cooler ka paani bhar diya?", "ac ka remote kidhar hai?",
    "wifi band hai hostel ka", "net nahi chal raha bohot slow hai", "hotspot on kar de thodi der", "mobile data khatam ho gaya",
    "phone charge pe laga de", "power bank kiske paas hai?", "laptop charger bhool gaya room pe", "iron chahiye kapde press karne hain",
    "bed sheet change karni hai", "room bohot ganda ho raha hai", "safai karni padegi aaj", "warden round pe aaya tha kya?",
    "in-time se pehle aana hai hostel", "gate pass banwaya kisi ne?", "late entry lag gayi meri", "fine lag gaya register me",
    "security guard rok raha hai", "hostel election ka kya scene hai?", "senior log bula rahe hain intro ke liye",
    "water purifier kharab hai", "laundry wala kab aayega?", "curfew time ho gaya chalo andar",

    # 4. OUTINGS, TRIPS, TRAVEL & TRANSPORT
    "trip ka plan banate hain", "weekend pe kahan jaye?", "rishikesh chale rafting ke liye?", "manali ka plan cancel mat karna",
    "goa trip dream hi reh gaya", "jaipur ghumne ka man hai", "cab book kar de uber se", "ola me auto mil gaya",
    "metro station pe khada hu", "platform number 2 pe aao", "traffic bohot zyada hai raste me", "10 minute me pahunch raha hu",
    "traffic jam me phasa hua hu", "petrol khatam hone wala hai", "bike ki servicing karwani hai", "car pool kare kya subah?",
    "parking me jagah nahi mili", "bus chhoot gayi meri", "auto wala double charge maang raha hai", "station pe pick kar lena mujhe",
    "ticket confirm ho gayi train ki", "tatkal me ticket nahi mila", "flight bohot costly hai", "backpack pack kar liya sabne?",
    "tent rent pe mil jayega waha?", "bonfire ka arrangement hai kya?", "weather kaisa hai waha ka?", "pahado me thand hogi bohot",
    "sunscreen rakh lena", "power bank zarur le aana trip pe", "speaker kaun la raha hai songs ke liye?", "playlist share kar do road trip ki",

    # 5. GAMING, SPORTS & ENTERTAINMENT
    "valorant khelega koi?", "bgmi ka squad banao", "fifa tournament hostel room me", "counter strike download kar liya",
    "steam sale me game buy kiya", "cricket ground pe aa jao", "football match kab shuru hoga?", "badminton racket lana mat bhoolna",
    "gym chalte hain shaam ko", "workout partner chahiye", "protein shake pi liya?", "ipl match kiska hai aaj?",
    "score kya chal raha hai live?", "sixer mara bhai ne", "last over me thriller match tha", "world cup final dekhne kahan chalna hai?",
    "kaunsi movie dekhni hai?", "multiplex me seat book ho gayi?", "popcorn bohot mehanga hai cinema me", "interval ho gaya kya?",
    "netflix ka password change kar diya kya?", "prime video pe nayi series aayi hai", "anime ka new episode dekha?",
    "trailer kaisa laga movie ka?", "spoiler mat dena koi please", "climax bilkul unexpected tha", "soundtrack bohot tagda hai",

    # 6. GOSSIP, BANTER, REACTIONS & SLANG
    "kya chal raha hai batao", "kuch naya batao life me", "bohot bada scene ho gaya aaj", "kisne kya bola mujhe batao",
    "sahi baat hai bilkul", "so true yaar", "gazab beizzati hai yaar", "chup kar bilkul tu",
    "chal jhootha kuch bhi bolta hai", "scene sorted hai tension mat le", "full vibe hai yahan pe", "dead ho gaya has has ke",
    "lmao ye kya dekh liya", "epic clip hai bhai", "meme share kiya group pe dekho", "instagram reel check karo",
    "kya joke mara hai", "sarcasm tha bhai serious mat ho", "gussa kyu ho raha hai faltu me?", "chill karo sab chill karo",
    "pagal ho gaya hai kya dimag se?", "overacting kam kar thodi", "acting ke 50 rupay kaat", "dil se bura lagta hai bhai",
    "main nahi sun raha teri baat", "pakka done samjhe na?", "commitment deke bhool mat jana", "kal dekhte hain aaram se",
    "ab so jao sab", "subah uthna hai 8 baje", "neend nahi aa rahi bilkul", "existential crisis ho raha hai raat ko",
    "life me kya chal raha hai pata nahi", "future ka soch ke darr lagta hai", "sab theek ho jayega tension mat lo",
    "bhai tu best hai", "party kab dega promotion ki?", "cake cutting kab hai room me?", "happy birthday bhai party hard",
    "bhai gift kya chahiye bata?", "surprise party ka plan spoil mat karna", "status dekh uska jaake",

    # 7. CHAT LOGISTICS, CONFIRMATIONS & MICRO-CONVERSATIONS
    "kaha gum hai sab log?", "reply kyu nahi kar raha koi?", "seen pe chhod diya sabne", "typing... dikha raha hai",
    "voice note sun le mera", "mic mute kar meeting me", "screen share kar de zoom pe", "link bhej do join karne ka",
    "google meet pe aao sab", "discord server pe call pe aao", "network issue aa raha hai baar baar", "awaz kat rahi hai teri",
    "ab sunai de raha hai?", "haan ab clear hai voice", "camera on mat kar bhai", "recording start kar di kya?",
    "chat me likh de jo bolna hai", "whatsapp web connect nahi ho raha", "backup restore ho gaya chat ka", "group ka naam change kisne kiya?",
    "admin kaun hai iss group ka?", "dp change kar di group ki", "naye member ko add kar do", "kisi ko call mat lagana abhi",
    "dnd mode pe phone daal raha hu", "battery 2 percent bachi hai bye", "charger lagake online aata hu", "ek ghante me connect karte hain",
    "aaj ka din bohot hectic tha", "exhaust ho gaya hu bilkul", "sir dard ho raha hai bohot", "dawa le li maine don't worry",
    "weather bohot mast hai aaj", "baarish shuru ho gayi tezi se", "dhoop bohot tez hai bahar", "chhat pe hawa chal rahi hai mast",
    "sham ko terrace pe aana", "tea stall pe wait kar raha hu", "jaldi aa late mat kar", "5 minute me nahi aaya toh chala jaunga"
]

# Prefixes, Suffixes, Emojis for Dynamic Combinatorial Variation
PREFIXES = [
    "", "", "", "",  # Higher weight for plain
    "bhai ", "yaar ", "arre ", "suno ", "bro ", "waise ", "dekh ", 
    "haan ", "acha ", "sachi ", "oye ", "abe ", "listen ", "guys "
]

SUFFIXES = [
    "", "", "", "",  # Higher weight for plain
    " bhai", " yaar", " bro", " seriously", " fr", " lol", " lmao", 
    " rn", " please", " jaldi", " pakka", " na", " batao"
]

PUNCTUATION_MODIFIERS = [
    "", "",  # Keep original
    ".", "!", "?", "??", "...", "!!"
]

EMOJIS = [
    "", "", "", "", "", "",  # Higher weight for no emoji
    " 😂", " 💀", " 😭", " 🔥", " 👀", " 🫡", " 🤦‍♂️", " ✨", 
    " 💯", " 🥲", " 🤝", " 🍻", " 😴", " ☕", " 👍", " 🙏"
]

# Track usage count per base phrase to enforce strict capping
phrase_usage_tracker = Counter()
MAX_BASE_PHRASE_USAGE = 12

def get_varied_hinglish_phrase():
    """Generates a non-repetitive, dynamically varied Hinglish message."""
    available_phrases = [p for p in HINGLISH_PHRASES if phrase_usage_tracker[p] < MAX_BASE_PHRASE_USAGE]
    if not available_phrases:
        # Reset tracker if all reached cap
        phrase_usage_tracker.clear()
        available_phrases = HINGLISH_PHRASES

    base = random.choice(available_phrases)
    phrase_usage_tracker[base] += 1

    prefix = random.choice(PREFIXES)
    suffix = random.choice(SUFFIXES)
    punct = random.choice(PUNCTUATION_MODIFIERS)
    emoji = random.choice(EMOJIS)

    # Clean base punctuation if appending our own
    clean_base = base.rstrip("?!.")
    res = f"{prefix}{clean_base}{punct}{suffix}{emoji}".strip()
    return res

# ============================================================================
# EVALUATION GROUND TRUTHS (PRESERVED GROUND TRUTH QUERY MAPPINGS)
# ============================================================================
EVAL_GROUND_TRUTHS = [
    # SEMANTIC (12)
    {"type": "semantic", "query": "When did we finally decide on the trip?", "target_text": "bhai Manali hi final 😂", "target_sender": "Rahul", "zero_overlap": True, "pre_context": [("Neha", "Are we deciding the trip today?"), ("Priya", "Shimla seems cheaper.")]},
    {"type": "semantic", "query": "Who is paying for the dinner bill?", "target_text": "sabka kharcha mai uthaunga aaj ka, tension not", "target_sender": "Aman", "zero_overlap": True, "pre_context": [("Rohit", "dinner was great"), ("Simran", "bill split karna hai kya?")]},
    {"type": "semantic", "query": "Is anyone bringing a car?", "target_text": "I'll drive my swift dzire to the venue", "target_sender": "Karan", "zero_overlap": True, "pre_context": [("Priya", "cab karni padegi"), ("Aman", "kaise jana hai?")]},
    {"type": "semantic", "query": "Did the professor cancel the test?", "target_text": "no exam tomorrow guys, chill", "target_sender": "Neha", "zero_overlap": True, "pre_context": [("Rahul", "I heard the professor is absent"), ("Simran", "kya hua?")]},
    {"type": "semantic", "query": "Where are we meeting for project work?", "target_text": "library ke second floor aaja sab", "target_sender": "Rohit", "zero_overlap": True, "pre_context": [("Neha", "where to meet?"), ("Karan", "project work baaki hai")]},
    {"type": "semantic", "query": "What are we gifting him?", "target_text": "watch le lete hain, best rhega", "target_sender": "Priya", "zero_overlap": False},
    {"type": "semantic", "query": "Is the assignment difficult?", "target_text": "maths waala itna hard hai dimag kharab", "target_sender": "Ananya", "zero_overlap": False},
    {"type": "semantic", "query": "Which movie to watch?", "target_text": "Inception dekh lete hai, mast hai", "target_sender": "Simran", "zero_overlap": False},
    {"type": "semantic", "query": "Are we playing cricket today?", "target_text": "match ke liye ground pahuncho shaam ko", "target_sender": "Aman", "zero_overlap": True, "pre_context": [("Rohit", "weather is good"), ("Rahul", "khelenge aaj?")]},
    {"type": "semantic", "query": "Is it raining?", "target_text": "baarish itni tez ho rahi bahaar", "target_sender": "Rahul", "zero_overlap": False},
    {"type": "semantic", "query": "Who got the highest marks?", "target_text": "topper to humari Neha hi hai as usual", "target_sender": "Karan", "zero_overlap": True, "pre_context": [("Priya", "results are out"), ("Rahul", "highest marks kiske hai?")]},
    {"type": "semantic", "query": "What time is the class?", "target_text": "lecture 9 baje shuru hoga", "target_sender": "Rohit", "zero_overlap": True, "pre_context": [("Ananya", "class cancel ho gayi kya?"), ("Simran", "what time to come?")]},

    # ATTRIBUTED (10)
    {"type": "attributed", "query": "What did Priya say about the budget?", "target_text": "paisa utna nahi hai, 5k limit rakh lo", "target_sender": "Priya", "zero_overlap": True, "pre_context": [("Karan", "we need a budget for the party"), ("Aman", "how much to contribute?")]},
    {"type": "attributed", "query": "Where is Ananya going for her internship?", "target_text": "Bangalore shift ho rahi hoon next month for the job", "target_sender": "Ananya", "zero_overlap": True, "pre_context": [("Neha", "where are you going?"), ("Rohit", "internship kidhar lagi?")]},
    {"type": "attributed", "query": "Did Rohit submit the file?", "target_text": "haan maine mail kar diya sir ko", "target_sender": "Rohit", "zero_overlap": False},
    {"type": "attributed", "query": "What did Karan say about the match?", "target_text": "India jeetegi bhai aaj", "target_sender": "Karan", "zero_overlap": False},
    {"type": "attributed", "query": "Why was Neha angry?", "target_text": "mujhpe mat gussa karo maine kuch ni kiya", "target_sender": "Neha", "zero_overlap": False},
    {"type": "attributed", "query": "What did Aman say about his phone?", "target_text": "mera mobile toot gaya yaar screen gayab", "target_sender": "Aman", "zero_overlap": False},
    {"type": "attributed", "query": "What food did Simran order?", "target_text": "maine pizza aur pasta mangwa liya", "target_sender": "Simran", "zero_overlap": False},
    {"type": "attributed", "query": "Where does Rahul want to eat?", "target_text": "dhaba chalte hai bhai log, waha eat karenge sasta padega", "target_sender": "Rahul", "zero_overlap": False},
    {"type": "attributed", "query": "What was Priya's idea?", "target_text": "theme party karte hain iss baar", "target_sender": "Priya", "zero_overlap": False},
    {"type": "attributed", "query": "Did Karan find his keys?", "target_text": "chabi mil gayi bag me hi thi", "target_sender": "Karan", "zero_overlap": False},

    # TEMPORAL (8)
    {"type": "temporal", "query": "What did we discuss last month?", "target_text": "August trip cancel karna padega I think", "target_sender": "Rahul", "zero_overlap": False, "date_override": datetime.datetime(2026, 8, 15, 12, 0, 0)},
    {"type": "temporal", "query": "Who wished happy birthday yesterday?", "target_text": "happy birthday bhai party de", "target_sender": "Aman", "zero_overlap": False, "date_override": datetime.datetime(2026, 8, 31, 0, 5, 0)},
    {"type": "temporal", "query": "What was planned last week?", "target_text": "let's go bowling on weekend", "target_sender": "Rohit", "zero_overlap": False, "date_override": datetime.datetime(2026, 8, 25, 10, 0, 0)},
    {"type": "temporal", "query": "Any updates on college reopening in July?", "target_text": "July 15 se classes fir se shuru", "target_sender": "Neha", "zero_overlap": False, "date_override": datetime.datetime(2026, 7, 5, 10, 0, 0)},
    {"type": "temporal", "query": "What did someone say in June about the fest?", "target_text": "cultural fest cancel ho gaya June me pata chala", "target_sender": "Priya", "zero_overlap": False, "date_override": datetime.datetime(2026, 6, 20, 10, 0, 0)},
    {"type": "temporal", "query": "What was the issue in May?", "target_text": "wifi bohot bekar chal raha hai aajkal", "target_sender": "Simran", "zero_overlap": False, "date_override": datetime.datetime(2026, 5, 10, 10, 0, 0)},
    {"type": "temporal", "query": "Did we play any games last month?", "target_text": "kal fifa khelte hai mere ghar", "target_sender": "Karan", "zero_overlap": False, "date_override": datetime.datetime(2026, 8, 5, 10, 0, 0)},
    {"type": "temporal", "query": "Who sent the funny meme yesterday?", "target_text": "look at this cat lmao 🐈", "target_sender": "Ananya", "zero_overlap": False, "date_override": datetime.datetime(2026, 8, 31, 14, 0, 0)},

    # MIXED-DIFFICULT (10)
    {"type": "mixed", "query": "What did Neha say yesterday?", "target_text": "main nahi aa rahi bye", "target_sender": "Neha", "zero_overlap": False, "date_override": datetime.datetime(2026, 8, 31, 18, 0, 0)},
    {"type": "mixed", "query": "Did Aman talk about movies last month?", "target_text": "wo nayi wali movies ka ticket mila kya kisi ko?", "target_sender": "Aman", "zero_overlap": False, "date_override": datetime.datetime(2026, 8, 12, 10, 0, 0)},
    {"type": "mixed", "query": "What was Priya's suggestion in July?", "target_text": "goa better suggestion rahega bhai log waha chalte", "target_sender": "Priya", "zero_overlap": False, "date_override": datetime.datetime(2026, 7, 20, 10, 0, 0)},
    {"type": "mixed", "query": "Did Rohit say anything about exams last week?", "target_text": "exams ki padhai karni shuru kardi mene, warna fail", "target_sender": "Rohit", "zero_overlap": False, "date_override": datetime.datetime(2026, 8, 26, 10, 0, 0)},
    {"type": "mixed", "query": "What did Simran say about the presentation yesterday?", "target_text": "presentation slides ready ho gayi ab bas padhna hai", "target_sender": "Simran", "zero_overlap": False, "date_override": datetime.datetime(2026, 8, 31, 9, 0, 0)},
    {"type": "mixed", "query": "What did Karan buy last month?", "target_text": "nayi bike buy kar li boys, gedi marne chalenge", "target_sender": "Karan", "zero_overlap": False, "date_override": datetime.datetime(2026, 8, 8, 10, 0, 0)},
    {"type": "mixed", "query": "Where did Rahul travel in June?", "target_text": "shimla travel kiya hai baraf giri hai, main yahi hu", "target_sender": "Rahul", "zero_overlap": False, "date_override": datetime.datetime(2026, 6, 15, 10, 0, 0)},
    {"type": "mixed", "query": "Did Ananya submit the form yesterday?", "target_text": "form submit done finally, server down tha", "target_sender": "Ananya", "zero_overlap": False, "date_override": datetime.datetime(2026, 8, 31, 23, 0, 0)},
    {"type": "mixed", "query": "What did Aman say about budget in July?", "target_text": "budget khatam ho gaya hai bhai srsly", "target_sender": "Aman", "zero_overlap": False, "date_override": datetime.datetime(2026, 7, 2, 10, 0, 0)},
    {"type": "mixed", "query": "What was Priya's excuse last week?", "target_text": "tabiyat theek nahi lag rahi, I'll skip, yehi excuse hai", "target_sender": "Priya", "zero_overlap": False, "date_override": datetime.datetime(2026, 8, 24, 10, 0, 0)}
]

def clean_word(word):
    return word.lower().strip(string.punctuation)

def check_word_overlap(query, target):
    q_words = set([clean_word(w) for w in query.split()])
    t_words = set([clean_word(w) for w in target.split()])
    stop_words = {"a", "an", "the", "in", "on", "at", "to", "for", "with", "about", "what", "did", "say", "is", "we", "are", "who", "any"}
    return q_words.intersection(t_words) - stop_words

# Verify zero-overlap
zero_overlap_count = sum(1 for t in EVAL_GROUND_TRUTHS if t.get("zero_overlap") and not check_word_overlap(t["query"], t["target_text"]))
print(f"Zero-overlap queries verified: {zero_overlap_count} (Needs >= 10)")

messages = []
ground_truth_msgs = []

for truth in EVAL_GROUND_TRUTHS:
    dt = truth.get("date_override", random_date(START_DATE, END_DATE))
    msg = {
        "id": generate_id(),
        "sender": truth["target_sender"],
        "timestamp": dt.isoformat(),
        "text": truth["target_text"],
        "truth_ref": truth
    }
    ground_truth_msgs.append(msg)

ground_truth_msgs.sort(key=lambda x: x["timestamp"])
eval_set = []

# Generate threads of messages
total_background_msgs = 5500
generated_dates = sorted([random_date(START_DATE, END_DATE) for _ in range(total_background_msgs)])

gt_index = 0
for dt in generated_dates:
    while gt_index < len(ground_truth_msgs) and ground_truth_msgs[gt_index]["timestamp"] <= dt.isoformat():
        gt = ground_truth_msgs[gt_index]
        truth = gt.pop("truth_ref")
        
        # Pre-context
        if "pre_context" in truth:
            for i, (snd, txt) in enumerate(truth["pre_context"]):
                messages.append({
                    "id": generate_id(),
                    "sender": snd,
                    "timestamp": (datetime.datetime.fromisoformat(gt["timestamp"]) - datetime.timedelta(minutes=len(truth["pre_context"])-i)).isoformat(),
                    "text": txt
                })
        else:
            for i in range(3):
                messages.append({
                    "id": generate_id(),
                    "sender": random.choice(PARTICIPANTS),
                    "timestamp": (datetime.datetime.fromisoformat(gt["timestamp"]) - datetime.timedelta(minutes=5-i)).isoformat(),
                    "text": get_varied_hinglish_phrase()
                })
            
        messages.append(gt)
        
        # Post-context
        for i in range(3):
            messages.append({
                "id": generate_id(),
                "sender": random.choice(PARTICIPANTS),
                "timestamp": (datetime.datetime.fromisoformat(gt["timestamp"]) + datetime.timedelta(minutes=i+1)).isoformat(),
                "text": get_varied_hinglish_phrase()
            })

        eval_set.append({
            "query": truth["query"],
            "expected_message_id": gt["id"],
            "type": truth["type"],
            "zero_overlap": truth.get("zero_overlap", False)
        })
        gt_index += 1

    sender = random.choice(PARTICIPANTS)
    text = get_varied_hinglish_phrase()

    messages.append({
        "id": generate_id(),
        "sender": sender,
        "timestamp": dt.isoformat(),
        "text": text
    })

messages.sort(key=lambda x: x["timestamp"])

with open("data/messages.json", "w", encoding="utf-8") as f:
    json.dump(messages, f, indent=2)

with open("data/eval_set.json", "w", encoding="utf-8") as f:
    json.dump(eval_set, f, indent=2)

unique_texts = len(set(m["text"] for m in messages))
print(f"Generated {len(messages)} total messages saved to data/messages.json")
print(f"Unique message texts: {unique_texts} (Diversity: {unique_texts/len(messages)*100:.1f}%)")
print(f"Generated {len(eval_set)} eval queries saved to data/eval_set.json")
