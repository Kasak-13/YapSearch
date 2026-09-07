import json
import random
import uuid
import datetime
import string

# Ensure 40 ground truth queries
# Requirements:
# 12 semantic
# 10 attributed
# 8 temporal
# 10 mixed-difficult
# >= 10 with zero word overlap

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

HINGLISH_PHRASES = [
    "haan bhai", "kya chal raha hai", "sahi hai", "lol", "lmao", "😂", "ok", "kuch nahi", 
    "batao", "kaise ho?", "chal be", "yaar", "pata nahi", "dekhte hain", "kal milte hain",
    "done", "achha", "kya baat hai", "arre yaar", "pagal hai kya", "bhai", "bro", "hn",
    "k", "hmm", "👍", "kaha ho?", "college aayega?", "kya assignment bhai?", "ded", 
    "chup kar", "tu bata", "kab jaana hai?", "kisne kaha?", "so true", "yess", "no way",
    "bhookh lag rahi hai", "kaha chale?", "kisi ne project submit kiya?", "sir ne kya bola?",
    "attendance lagwa de bhai", "canteen aaja", "kaunsi movie dekhni hai?", "trip ka plan batao",
    "budget nahi hai mera", "paisa kaun dega?", "room pe aaja", "aaj cricket khelenge",
    "baarish ho rahi hai", "so jao sab", "subah uthna hai", "late ho gaya", "bhai jaldi kar",
    "kuch samajh nahi aa raha", "notes bhej de", "wifi band hai", "net nahi chal raha",
    "kaha gum hai?", "kaisa exam gaya?", "pass ho jaunga bs", "sir gussa the", "main nahi aa raha"
]

EVAL_GROUND_TRUTHS = [
    # SEMANTIC (12) - Focus on meaning, many zero-overlap
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

    # TEMPORAL (8) - Date ranges
    {"type": "temporal", "query": "What did we discuss last month?", "target_text": "August trip cancel karna padega I think", "target_sender": "Rahul", "zero_overlap": False, "date_override": datetime.datetime(2026, 8, 15, 12, 0, 0)},
    {"type": "temporal", "query": "Who wished happy birthday yesterday?", "target_text": "happy birthday bhai party de", "target_sender": "Aman", "zero_overlap": False, "date_override": datetime.datetime(2026, 8, 31, 0, 5, 0)}, # Yesterday from Sept 1
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
    overlap = q_words.intersection(t_words)
    return overlap

# Validate overlaps
zero_overlap_count = 0
for truth in EVAL_GROUND_TRUTHS:
    if truth.get("zero_overlap"):
        overlap = check_word_overlap(truth["query"], truth["target_text"])
        stop_words = {"a", "an", "the", "in", "on", "at", "to", "for", "with", "about", "what", "did", "say", "is", "we", "are", "who", "any"}
        overlap = overlap - stop_words
        if overlap:
            print(f"WARNING: Zero-overlap query failed! Overlap '{overlap}' in query: '{truth['query']}' vs target: '{truth['target_text']}'")
        else:
            zero_overlap_count += 1

print(f"Zero-overlap queries verified: {zero_overlap_count} (Needs >= 10)")

messages = []

def add_message(dt, text, sender):
    msg = {
        "id": generate_id(),
        "sender": sender,
        "timestamp": dt.isoformat(),
        "text": text
    }
    messages.append(msg)
    return msg

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
        
        # Add pre-context
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
                    "text": random.choice(HINGLISH_PHRASES)
                })
            
        messages.append(gt)
        
        # Add post-context
        for i in range(3):
            messages.append({
                "id": generate_id(),
                "sender": random.choice(PARTICIPANTS),
                "timestamp": (datetime.datetime.fromisoformat(gt["timestamp"]) + datetime.timedelta(minutes=i+1)).isoformat(),
                "text": random.choice(HINGLISH_PHRASES)
            })

        eval_set.append({
            "query": truth["query"],
            "expected_message_id": gt["id"],
            "type": truth["type"],
            "zero_overlap": truth.get("zero_overlap", False)
        })
        gt_index += 1

    sender = random.choice(PARTICIPANTS)
    text = random.choice(HINGLISH_PHRASES)
    if random.random() < 0.2:
        text = text + " " + random.choice(HINGLISH_PHRASES)

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

print(f"Generated {len(messages)} messages and saved to data/messages.json")
print(f"Generated {len(eval_set)} eval queries and saved to data/eval_set.json")
