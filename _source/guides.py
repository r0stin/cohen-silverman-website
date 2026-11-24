"""
Guide articles for the Cohen & Silverman website.

Each guide is general information written in plain language. Sections are
(heading, [blocks]) where a block is a paragraph (str) or a bullet list (list).
"""

UPDATED = "November 2026"

GUIDES = [
    {
        "slug": "guide-unpaid-debt",
        "photo": ("1434030216411-0b793f4b4173", "A person writing notes at a desk"),
        "area": "debt-recovery",
        "title": "Someone owes you money and won't pay: your next steps",
        "short_title": "Someone owes you money and won't pay",
        "summary": "How to prove the debt, ask for payment properly, beat the deadline and actually collect once you win.",
        "meta_desc": "A practical guide to recovering money you're owed: proving the debt, sending a demand letter, limitation periods, choosing a court and enforcing a judgment.",
        "takeaways": [
            "Gather proof of the debt before you contact the person again.",
            "A formal demand letter resolves many debts without a lawsuit.",
            "Limitation periods are strict, so don't let the debt sit.",
            "Winning in court is step one. Enforcement is how you get paid.",
        ],
        "sections": [
            ("Start with the paper trail", [
                "A debt you can prove is far easier to collect. Before you send another message, gather everything that shows money changed hands and that it was meant to be repaid.",
                [
                    "Bank statements and e-transfer records showing the payment",
                    "Texts, emails or DMs that mention the money. A message like \"I'll pay you back next month\" is powerful evidence.",
                    "Any contract, IOU, invoice or receipt",
                    "Records of partial repayments, which show the debt was acknowledged",
                    "The person's full legal name and their current or last known address",
                ],
                "No written contract? That is common, and many successful claims rely on messages and transfer records alone.",
            ]),
            ("Keep communication calm and in writing", [
                "Angry or threatening messages can be used against you later. Keep any contact short, factual and in writing, so there's a clear record of what was said.",
                "If the person offers a payment plan over the phone, confirm the terms by email or text afterwards. Don't agree to anything that reduces the amount owed until you understand the consequences.",
            ]),
            ("Send a formal demand", [
                "A demand letter sets out how much is owed, why it's owed, the deadline for payment and what will happen if the deadline passes. A letter on a law firm's letterhead shows you're serious, and many people pay or propose a plan at this stage.",
                "It also creates a record that you gave the other side a fair chance to pay before going to court, which judges look on favorably.",
            ]),
            ("Know your deadline", [
                "Every debt claim has a limitation period: a deadline after which you can no longer sue. In many places it is as short as two years from the date payment was due, although it varies with the type of debt and where you live.",
                "Partial payments or written acknowledgments can sometimes restart the clock, but don't rely on that without advice. If your debt is more than a year old, speak to a lawyer soon.",
            ]),
            ("Choose the right court", [
                "Smaller amounts usually belong in small claims court, which is faster and simpler. Larger claims go to a higher court. The right choice affects how long the case takes, what it costs and whether you can recover interest and legal costs.",
            ]),
            ("Plan for enforcement before you sue", [
                "A judgment does not pay itself. If the other side still refuses to pay, the court's enforcement tools come into play:",
                [
                    "Garnishing wages, so part of each paycheck comes to you",
                    "Garnishing bank accounts",
                    "Registering a lien against property",
                    "Examining the debtor under oath about their income and assets",
                ],
                "Before suing, it's worth asking whether the person has income or assets that can be reached. We look at collectability up front so you don't spend money chasing a judgment that can't be paid.",
            ]),
            ("When to call a lawyer", [
                "Call us if the amount matters to you, the person has stopped responding, a deadline is approaching, or they've mentioned bankruptcy or moving assets. A short consultation will tell you whether a claim makes sense and what it is likely to cost.",
            ]),
        ],
    },
    {
        "slug": "guide-sextortion-first-24-hours",
        "photo": ("1563986768609-322da13575f3", "A laptop and a smartphone on a desk"),
        "area": "extortion-blackmail",
        "title": "Being blackmailed or sextorted? What to do in the first 24 hours",
        "short_title": "Blackmail and sextortion: the first 24 hours",
        "summary": "Why you shouldn't pay, how to preserve evidence, how to lock down your accounts and who to report it to.",
        "meta_desc": "Being blackmailed or threatened with private images? Steps to take in the first 24 hours: don't pay, preserve evidence, secure accounts and report it.",
        "takeaways": [
            "Don't pay, and don't send anything else.",
            "Stop responding, but keep every message.",
            "Lock down your accounts and report it to the platform and police.",
            "You are not alone, and this is not your fault.",
        ],
        "sections": [
            ("Take a breath. The pressure is deliberate.", [
                "Extortion relies on panic: short deadlines, constant messages and threats designed to stop you thinking clearly. The steps you take in the next few hours matter far more than how quickly you reply.",
            ]),
            ("Don't pay", [
                "Paying rarely ends it. It shows the person that the threat works, and it often leads to further demands. If you have already paid, you have not done anything wrong. Stop paying now and follow the steps below.",
            ]),
            ("Stop engaging, but preserve everything", [
                "Don't argue, plead or negotiate. At the same time, don't delete the conversation, because it is your evidence. Capture:",
                [
                    "Screenshots of every message and threat, with dates and times visible",
                    "The person's usernames, profile links and any other accounts they use",
                    "Any payment details they gave you, such as account numbers or wallet addresses",
                    "Records of any payments you have already made",
                ],
            ]),
            ("Secure your accounts", [
                [
                    "Change your passwords and turn on two-factor authentication",
                    "Review your privacy settings and hide your friends or followers list",
                    "Temporarily deactivate, rather than delete, accounts the person can see",
                    "Check which devices are signed in to your accounts and remove any you don't recognize",
                ],
            ]),
            ("Report it", [
                "Most major platforms have dedicated reporting for intimate image abuse and sextortion, and they can remove content and block accounts. Report it to police too, and keep the report number.",
                "If the images involve anyone under 18, contact police right away. Specialized services exist to help remove such images from the internet.",
            ]),
            ("How a lawyer can help", [
                "We can take over communication so you no longer have to deal with the person, coordinate takedown requests, and seek urgent court orders against publication. Where the person can be identified, we can bring a claim for damages, and we can ask the court to protect your identity in the proceedings.",
            ]),
            ("Look after yourself", [
                "Tell someone you trust what is happening. If you feel overwhelmed or unsafe, contact a crisis line, or call 911 or your local emergency number if you are in danger.",
            ]),
        ],
    },
    {
        "slug": "guide-restraining-orders",
        "photo": ("1501139083538-0139583c060f", "An hourglass resting on a stone surface"),
        "area": "restraining-orders",
        "title": "How restraining orders work, step by step",
        "short_title": "How restraining orders work",
        "summary": "What an order can do, who can apply, how urgent orders work, and what to expect at the hearing and afterwards.",
        "meta_desc": "A step-by-step guide to restraining and protection orders: what they can do, who can apply, emergency orders, evidence, the hearing and breaches.",
        "takeaways": [
            "Orders can limit contact, distance and specific places.",
            "Urgent temporary orders are possible when the risk is immediate.",
            "A clear, dated record of incidents makes the difference.",
            "Report any breach to police right away.",
        ],
        "sections": [
            ("What a restraining order can do", [
                "A restraining order is a court order that sets enforceable limits on another person's behavior. Depending on the type of order and where you live, it can:",
                [
                    "Prohibit contact, including through other people and online",
                    "Require the person to stay a set distance from you",
                    "Keep them away from your home, workplace or school",
                    "Extend protection to children or other members of your household",
                ],
                "Different places use different names, including protection order and peace bond, but the purpose is the same.",
            ]),
            ("Who can apply", [
                "Orders are available against partners, former partners and family members, and in many places against acquaintances, coworkers, people who live nearby and even strangers. The test varies, but you will generally need to show a reasonable fear for your safety or a pattern of harassment.",
            ]),
            ("Emergency and temporary orders", [
                "When the risk is urgent, a court can make a short-term order quickly, sometimes without notifying the other person first. A full hearing follows, where both sides can be heard and the court decides whether a longer order is needed.",
            ]),
            ("Building your evidence", [
                "Applications are won on evidence. Start with the most serious and most recent incidents, then fill in the history.",
                [
                    "A dated log of incidents: what happened, where and who saw it",
                    "Messages, voicemails and social media posts",
                    "Photos of injuries or damaged property",
                    "Police report numbers and medical records",
                    "Names and contact details of witnesses",
                ],
            ]),
            ("The hearing", [
                "Both sides may present evidence, and the judge decides whether to make the order and on what terms. We prepare you in advance, speak for you in court, and ask for safety arrangements such as separate waiting areas or remote attendance where they are available.",
            ]),
            ("After the order is made", [
                "The order must be served on the other person before it can be enforced. Keep a copy with you, consider giving copies to your workplace or your children's school, and note the expiry date so it can be extended in time if you still need it.",
            ]),
            ("If the order is breached", [
                "Call police and report the breach right away, then write down what happened while it is fresh. Breaching a court order can lead to arrest and charges, and we can return to court on your behalf.",
            ]),
        ],
    },
    {
        "slug": "guide-documenting-harassment",
        "photo": ("1455390582262-044cdead277a", "A fountain pen writing on paper"),
        "area": "harassment",
        "title": "How to document harassment so it holds up",
        "short_title": "How to document harassment",
        "summary": "Keep a log that courts, police and platforms take seriously, and capture digital evidence the right way.",
        "meta_desc": "How to document harassment properly: keeping an incident log, capturing digital and physical evidence, storing it safely and what to avoid.",
        "takeaways": [
            "A consistent, dated log is your most important tool.",
            "Capture context: dates, usernames, links and witnesses.",
            "Store evidence in more than one secure place.",
            "Don't engage, even to tell them to stop again.",
        ],
        "sections": [
            ("Why documentation matters", [
                "Courts, police and platforms act on evidence. A single incident may not be enough on its own, but a documented pattern often is. Good records also save time and cost once lawyers are involved.",
            ]),
            ("Keep an incident log", [
                "Record every incident, however small, in the same format each time:",
                [
                    "Date and time",
                    "Where it happened, or which app, number or account was used",
                    "Exactly what was said or done",
                    "Who else saw or heard it",
                    "How it affected you, such as missed work or changed routines",
                    "Any report you made, with reference numbers",
                ],
            ]),
            ("Capture digital evidence properly", [
                [
                    "Take screenshots that show the date, time, sender and link",
                    "Save original files, such as voicemails and full emails, not just screenshots",
                    "Export entire chat histories where the app allows it",
                    "Record profile links rather than display names, which can change",
                ],
            ]),
            ("Record physical incidents", [
                "Write notes as soon as possible after anything happens in person. Photograph any damage, and save doorbell or security camera footage quickly, because many systems overwrite recordings after a few days.",
            ]),
            ("Store it safely", [
                "Back up your evidence in at least two places, ideally somewhere the person harassing you cannot access. Don't share your log with them or post it publicly.",
            ]),
            ("What to avoid", [
                [
                    "Replying or retaliating, even to tell them to stop again",
                    "Posting about the situation publicly, which can complicate legal options",
                    "Editing or cropping screenshots in ways that remove context",
                ],
            ]),
            ("Bringing it to us", [
                "Bring your log and evidence to your consultation. We'll organize it into a form that courts and platforms take seriously and recommend the strongest next step, from a cease and desist letter to a protection order or a claim for damages.",
            ]),
        ],
    },
]

AREA_GUIDE = {g["area"]: g for g in GUIDES}
