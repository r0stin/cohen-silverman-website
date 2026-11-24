#!/usr/bin/env python3
"""
Build script for the Cohen & Silverman Law Firm website.

    python _source/build.py

It combines the page files in _source/pages/ with the shared header, menus,
footer and the firm data below, and writes finished, plain HTML pages into
the site folder. Edit the FIRM details, practice areas or lawyers here, then
run the script again. Nothing needs to be installed beyond Python 3.
"""
import html
import json
import re
import runpy
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

# ---------------------------------------------------------------------------
# Firm details: replace these placeholders before going live.
# ---------------------------------------------------------------------------
FIRM = {
    "name": "Cohen & Silverman Law Firm",
    "phone": "(905) 604-7662",
    "phone_href": "+19056047662",
    "email": "intake@cohensilverman.com",
    "address_1": "390 Bay St., Suite 2000",
    "address_2": "Toronto, ON M5H 1W2",
    "hours": "Monday to Friday, 8:30 am to 6:00 pm",
    "hours_short": "Mon to Fri, 8:30 am to 6:00 pm",
    "hours_note": "Evening appointments by arrangement",
    # Paste a form service URL here (for example a Formspree endpoint) to receive
    # contact form submissions directly. Left empty, the form opens the visitor's
    # email app with their message addressed to the email above.
    "form_endpoint": "",
}

# ---------------------------------------------------------------------------
# Photography (Unsplash, free to use). Shown with a navy tone via CSS.
# ---------------------------------------------------------------------------
PHOTOS = {
    "justice": ("1589829545856-d10d557cf95f", "Bronze statue of Lady Justice holding the scales"),
    "library": ("1505664194779-8beaceb93744", "Law library with leather-bound volumes and marble busts"),
    "columns": ("1453945619913-79ec89a82c51", "Classical courthouse columns under a clear sky"),
    "shelves": ("1521587760476-6c12a4b040da", "Tall shelves of law books"),
    "books": ("1479142506502-19b3a3b7ff33", "Rows of bound law reports on a shelf"),
    "office": ("1497366811353-6870744d04b2", "Bright, modern office meeting space"),
    "signing": ("1450101499163-c8848c66ca85", "Hands reviewing and signing a document"),
}

# ---------------------------------------------------------------------------
# Lawyers
# ---------------------------------------------------------------------------
ATTORNEYS = [
    {
        "slug": "benjamin-cohen",
        "name": "Benjamin Cohen",
        "initials": "BC",
        "role": "Founding Partner",
        "focus_short": "Debt recovery, fraud and judgment enforcement",
        "focus": [("Debt Recovery", "debt-recovery"), ("Fraud & Civil Theft", "fraud-civil-theft"), ("Judgment Enforcement", "debt-recovery")],
        "short": "Leads the firm's recovery practice, from unpaid personal loans to contested commercial debts, and stays on enforcement until judgments are paid.",
        "bio": [
            "Benjamin co-founded Cohen & Silverman on a simple conviction: people who are owed money deserve a lawyer who will actually collect it. He leads the firm's debt recovery and fraud practice.",
            "His approach is practical. Before you spend anything significant, Benjamin will tell you whether your claim is worth pursuing, what it is likely to cost, and what recovery realistically looks like. When a case goes ahead, he pushes it firmly, and he stays on enforcement until the judgment is paid.",
            "He handles matters ranging from unpaid loans between family members to disputed commercial invoices, and works on asset tracing and freezing orders in fraud cases where speed is everything.",
        ],
    },
    {
        "slug": "joshua-silverman",
        "name": "Joshua Silverman",
        "initials": "JS",
        "role": "Founding Partner",
        "focus_short": "Extortion, defamation and online harassment",
        "focus": [("Extortion & Blackmail", "extortion-blackmail"), ("Defamation", "defamation"), ("Online Harassment", "harassment")],
        "short": "Handles the firm's most urgent and sensitive matters: extortion, sextortion and online attacks where hours count and discretion is essential.",
        "bio": [
            "Joshua co-founded the firm and leads its work on extortion, defamation and online harassment, the matters where hours count and discretion is essential.",
            "He understands how frightening these situations are, so he focuses first on containment: stopping material from spreading, securing the evidence, and taking over communication so clients no longer have to deal with the person targeting them.",
            "From there, Joshua pursues accountability through court orders, takedowns and claims for damages, including in cases where the person responsible starts out anonymous.",
        ],
    },
    {
        "slug": "rebecca-anderson",
        "name": "Rebecca Anderson",
        "initials": "RA",
        "role": "Partner",
        "focus_short": "Restraining orders and harassment",
        "focus": [("Restraining Orders", "restraining-orders"), ("Harassment", "harassment"), ("Protection Orders", "restraining-orders")],
        "short": "Guides clients through restraining and protection orders, including urgent applications, and stands with them at every hearing.",
        "bio": [
            "Rebecca leads the firm's restraining order and harassment practice. Much of her work happens under time pressure, when a client needs protection quickly and the evidence has to come together in days, not weeks.",
            "She prepares each application with care, helping clients turn months of incidents into a clear, credible record, and she stands with them in court so they never have to face the other person alone.",
            "Rebecca also helps clients think through practical safety steps alongside the legal process, and works with their support networks where that helps.",
        ],
    },
    {
        "slug": "noah-katz",
        "name": "Noah Katz",
        "initials": "NK",
        "role": "Associate",
        "focus_short": "Demand letters, claims and enforcement",
        "focus": [("Debt Recovery", "debt-recovery"), ("Demand Letters", "debt-recovery"), ("Harassment", "harassment")],
        "short": "Keeps recovery and harassment files moving, from the first demand letter through to enforcement, and is often a client's day-to-day contact.",
        "bio": [
            "Noah works across the firm's recovery and harassment matters, with a particular focus on keeping files moving: demand letters, claims, motions and enforcement steps.",
            "He is often a client's day-to-day contact, making sure questions are answered promptly and every deadline is met. Noah believes clients should never have to wonder what is happening with their case.",
        ],
    },
]
ATT = {a["slug"]: a for a in ATTORNEYS}

# ---------------------------------------------------------------------------
# Practice areas
# ---------------------------------------------------------------------------
AREAS = [
    {
        "slug": "debt-recovery",
        "name": "Debt Recovery",
        "select_label": "Debt recovery (money owed to me)",
        "icon": "hand-coins",
        "nav_desc": "Sue for unpaid loans, invoices and debts.",
        "summary": "Unpaid loans, unpaid invoices, bounced payments and broken agreements. We demand payment, sue when needed and enforce the judgment.",
        "photo": ("1554224155-6726b3ff858f", "Invoices, a calculator and financial paperwork on a desk"),
        "meta_title": "Debt Recovery Lawyers | Sue for Money Owed | Cohen & Silverman",
        "meta_desc": "Owed money by someone who won't pay? Cohen & Silverman sends demand letters, sues for unpaid loans and invoices, and enforces judgments until you're paid.",
        "h1": "Recover the money you're <em>owed.</em>",
        "lead": "Unpaid loans, unpaid invoices, bounced payments, broken agreements. We demand payment, sue when needed and enforce the judgment until you're paid.",
        "overview": [
            "Being owed money by someone who has stopped responding is exhausting. Every week that passes makes the money harder to collect and gives the other side time to move assets or disappear.",
            "We move quickly. We start by reviewing your paper trail and telling you honestly whether a claim makes financial sense. When it does, we send a formal demand, file in the right court, and use every available enforcement tool once you have a judgment.",
        ],
        "notice": ("hourglass-medium", "Limitation periods for debt claims are strict and can be as short as two years from the date payment was due. If your debt is getting old, contact us soon."),
        "matters": [
            ("hand-coins", "Unpaid personal loans", "Money lent to friends, family, ex-partners or acquaintances, with or without a written agreement."),
            ("receipt", "Unpaid invoices", "Work completed or goods delivered for clients and customers who won't pay."),
            ("handshake", "Breach of contract", "Deals, agreements and promises that were broken and cost you money."),
            ("bank", "Bounced and reversed payments", "Bounced payments, cancelled transfers and chargebacks used to avoid paying."),
            ("house-line", "Unpaid rent and damage", "Amounts owed by former tenants, including arrears and repair costs."),
            ("gavel", "Judgment enforcement", "Garnishment, bank seizures, property liens and debtor examinations to collect what the court awarded."),
        ],
        "stages": [
            ("magnifying-glass", "Review the evidence", "We go through your messages, transfers, contracts and invoices and confirm how much is owed and what can be proven."),
            ("envelope-simple", "Demand payment", "A formal demand letter from a law firm often resolves the matter without a lawsuit."),
            ("scales", "File the claim", "If they still don't pay, we sue in the appropriate court and push the case through to judgment."),
            ("vault", "Enforce the judgment", "A judgment is only paper until it's collected. We pursue wages, bank accounts and property until you're paid."),
        ],
        "checklist_title": "What to gather before we talk",
        "checklist": [
            "Texts, emails or DMs that mention the money",
            "Bank statements and e-transfer records",
            "Any contract, IOU, invoice or receipt",
            "The other person's full name and last known address",
            "A rough timeline of what was promised and when",
            "Records of any partial repayments",
        ],
        "faqs": [
            ("Can I sue someone if we never signed a written agreement?", "Often, yes. Text messages, emails, bank transfers and witnesses can all prove a loan or agreement. We'll review what you have and tell you how strong it is."),
            ("Is my claim too small to be worth pursuing?", "Not necessarily. Smaller claims can often go through a simplified court process, and you may be able to recover interest and some legal costs. We'll give you a straight answer on cost versus likely recovery before you commit."),
            ("What happens if they still don't pay after we win?", "We move to enforcement. Depending on where you live, that can include garnishing wages, seizing funds from bank accounts, registering liens against property and examining the debtor under oath about their assets."),
            ("How long does a debt recovery case take?", "Many matters settle within weeks of a demand letter. Contested lawsuits take longer, usually months. We'll give you a realistic timeline at the start and keep you updated."),
            ("Can I recover my legal fees?", "In many cases the court can order the other side to pay part of your legal costs, along with interest on the debt. How much depends on the court and the outcome."),
        ],
        "lawyers": ["benjamin-cohen", "noah-katz"],
        "related": ["fraud-civil-theft", "defamation", "harassment"],
    },
    {
        "slug": "harassment",
        "name": "Harassment",
        "select_label": "Harassment",
        "icon": "chats-circle",
        "nav_desc": "Stop unwanted contact, online abuse and stalking.",
        "summary": "Repeated calls, messages, fake accounts and showing up uninvited. We use legal pressure, court orders and civil claims to end it.",
        "photo": ("1523966211575-eb4a01e7dd51", "A telephone receiver lying on a plain surface"),
        "meta_title": "Harassment Lawyers | Stop Unwanted Contact | Cohen & Silverman",
        "meta_desc": "Harassment, cyberstalking, fake accounts and unwanted contact. Cohen & Silverman uses cease and desist letters, court orders and civil claims to make it stop.",
        "h1": "Make the harassment <em>stop.</em>",
        "lead": "Repeated calls, messages, fake accounts, showing up uninvited. We use legal pressure, court orders and civil claims to end it and hold the person accountable.",
        "overview": [
            "Harassment wears people down. Whether it comes from an ex-partner, someone who lives nearby, a former business contact or an anonymous account, it affects your sleep, your work and your sense of safety.",
            "We act on several fronts at once: a formal cease and desist letter, applications for court orders, requests to platforms to remove content and, where the law allows, a claim for damages. When the harasser is anonymous, we can ask the court to order platforms to reveal who is behind the account.",
        ],
        "notice": ("warning-circle", "If you are in immediate danger, call 911 or your local emergency number first."),
        "matters": [
            ("device-mobile", "Persistent unwanted contact", "Calls, texts, emails and messages that continue after you've asked them to stop."),
            ("globe", "Online harassment and cyberstalking", "Abusive posts, comments, monitoring and threats across social media and messaging apps."),
            ("user-focus", "Fake and anonymous accounts", "Impersonation and anonymous accounts used to target, embarrass or intimidate you."),
            ("footprints", "Following and showing up", "Waiting outside your home or workplace, or turning up wherever you'll be."),
            ("identification-card", "Doxxing", "Publishing your address, phone number, workplace or other private information."),
            ("users", "Harassment by an ex-partner", "Ongoing contact, monitoring or intimidation after a relationship has ended."),
        ],
        "stages": [
            ("folder-open", "Document everything", "We help you build an organized record of every incident, message and account involved."),
            ("envelope-simple", "Send a cease and desist", "A firm, formal letter puts the person on notice of the legal consequences of continuing."),
            ("shield-check", "Seek court protection", "Where needed, we apply for a restraining or protection order, including on an urgent basis."),
            ("scales", "Pursue accountability", "We can bring a civil claim for damages and request removal of harmful content."),
        ],
        "checklist_title": "Do this now",
        "checklist": [
            "Don't reply or engage, even to tell them to stop again",
            "Screenshot messages and posts, including dates and usernames",
            "Save voicemails and call logs",
            "Keep a dated log of every incident",
            "Report threats of violence to police and keep the report number",
            "Tell someone you trust what is happening",
        ],
        "faqs": [
            ("What counts as harassment legally?", "It generally involves a pattern of conduct that causes someone to fear for their safety or causes serious distress. The exact test depends on where you live and the remedy you're seeking. We'll explain what applies to your situation."),
            ("What if I don't know who is harassing me?", "We can often identify anonymous harassers. Courts can order platforms, service providers and websites to disclose account information."),
            ("Should I go to the police or a lawyer?", "Often both. Police handle criminal conduct. A lawyer can pursue civil remedies the police can't, such as civil protection orders, cease and desist letters, content removal and damages. We regularly work alongside police reports."),
            ("Will the harasser find out I contacted a lawyer?", "Not unless we decide together to contact them. Your consultation is confidential, and we plan every step with your safety in mind."),
        ],
        "lawyers": ["rebecca-anderson", "joshua-silverman"],
        "related": ["restraining-orders", "extortion-blackmail", "defamation"],
    },
    {
        "slug": "extortion-blackmail",
        "name": "Extortion & Blackmail",
        "select_label": "Extortion or blackmail",
        "icon": "shield-warning",
        "nav_desc": "Act fast against threats, sextortion and demands.",
        "summary": "Sextortion, threats to expose private information and demands for money. We act immediately, contain the damage and take over communication.",
        "photo": ("1567581935884-3349723552ca", "A smartphone lying face up on a dark surface"),
        "meta_title": "Extortion & Blackmail Lawyers | Sextortion Help | Cohen & Silverman",
        "meta_desc": "Being threatened or blackmailed? Cohen & Silverman acts fast and discreetly against sextortion and extortion: containment, takedowns, urgent court orders and claims.",
        "h1": "Threatened? You don't have to face it <em>alone.</em>",
        "lead": "Sextortion, threats to expose private information, demands for money. We act immediately, contain the damage and take over communication with the person making the threats.",
        "overview": [
            "Extortion is designed to make you panic and pay quickly. Paying rarely ends it. More often, it leads to more demands.",
            "Our response is fast and discreet. We help you secure your accounts and preserve evidence, coordinate with police and platforms to stop material spreading, and seek urgent court orders when needed. Where the person can be identified, we pursue them for damages.",
        ],
        "notice": ("warning-circle", "If the images involve someone under 18, contact police right away. If you are in immediate danger, call 911 or your local emergency number."),
        "matters": [
            ("eye-slash", "Sextortion", "Threats to share intimate images or videos unless you pay or send more."),
            ("lock-key", "Threats to expose private information", "Demands tied to threats of revealing personal, medical, financial or family information."),
            ("storefront", "Business extortion", "Threats of fake reviews, data leaks or false reports unless a payment is made."),
            ("users", "Threats from an ex-partner", "Private material or information used as leverage after a relationship ends."),
            ("database", "Data theft and ransom demands", "Demands made after someone has accessed your accounts, devices or files."),
            ("detective", "Identifying the person responsible", "Court orders and investigative steps to find out who is behind the threats."),
        ],
        "stages": [
            ("lifebuoy", "Stabilize", "We advise on immediate steps: stop engaging, lock down accounts and preserve every message."),
            ("prohibit", "Contain", "We work with platforms and hosts to remove or block material and prevent it from spreading."),
            ("siren", "Escalate", "We coordinate with police and, where needed, seek urgent court orders against publication."),
            ("scales", "Hold accountable", "Once the person is identified, we can bring a civil claim for damages."),
        ],
        "checklist_title": "Do this now",
        "checklist": [
            "Do not pay or send anything else",
            "Stop replying, but do not delete the conversation",
            "Screenshot the threats, usernames and profile links",
            "Temporarily deactivate (don't delete) accounts the person can see",
            "Report it to police and keep the report number",
            "Call us before responding to any new demand",
        ],
        "faqs": [
            ("Should I just pay to make it go away?", "We strongly advise against it. Paying shows the person that the threat works, and demands often increase. Every situation is different, so speak with us before you respond."),
            ("Will this become public if I take legal action?", "We take privacy seriously at every step. In many places, courts allow sensitive cases to proceed with anonymity or sealing orders. We'll discuss these protections with you before anything is filed."),
            ("What if the person is in another country?", "Cross-border cases are harder but not hopeless. Platform reporting, takedown requests and cooperation between police agencies can still be effective, and we focus on what protects you fastest."),
            ("Can I sue the person who is blackmailing me?", "Yes, if they can be identified. A civil claim can include damages for the harm caused and court orders preventing any further publication."),
        ],
        "lawyers": ["joshua-silverman", "rebecca-anderson"],
        "related": ["harassment", "defamation", "restraining-orders"],
    },
    {
        "slug": "restraining-orders",
        "name": "Restraining Orders",
        "select_label": "Restraining or protection order",
        "icon": "shield-check",
        "nav_desc": "Court orders that keep someone away from you.",
        "summary": "When someone won't keep their distance, a restraining or protection order sets enforceable limits. We handle the application, including urgent ones.",
        "photo": ("1436450412740-6b988f486c6b", "Stone pediment and columns of a courthouse"),
        "meta_title": "Restraining Order Lawyers | Protection Orders | Cohen & Silverman",
        "meta_desc": "Need a restraining or protection order? Cohen & Silverman prepares and argues applications, including urgent ones, and acts quickly when orders are breached.",
        "h1": "Protection, backed by a <em>court order.</em>",
        "lead": "When someone won't keep their distance, a restraining or protection order sets enforceable limits. We prepare and argue your application, including urgent ones.",
        "overview": [
            "A restraining order (in some places called a protection order or peace bond) is a court order that can prohibit someone from contacting you, coming near you, or going to your home, work or school. Breaching it can carry serious consequences.",
            "Applications are won on evidence. We help you assemble a clear, credible record, prepare your sworn statement and represent you at the hearing. When the risk is urgent, we can ask the court for a temporary order straight away.",
        ],
        "notice": ("warning-circle", "If you are in immediate danger, call 911 or your local emergency number. A court order is important, but it does not replace emergency help."),
        "matters": [
            ("lightning", "Emergency and temporary orders", "Urgent short-term protection while a full hearing is scheduled."),
            ("heart-break", "Partners and former partners", "Protection from a current partner, an ex-partner or a family member."),
            ("user-minus", "Civil harassment orders", "Protection from someone who lives nearby, an acquaintance, a coworker or a stranger."),
            ("users-three", "Protecting your household", "Orders that extend to children and other household members where appropriate."),
            ("arrows-clockwise", "Extensions and changes", "Extending an order that is about to expire, or changing its terms."),
            ("prohibit", "Enforcing breaches", "Taking action quickly when the other person violates the order."),
        ],
        "stages": [
            ("lifebuoy", "Assess safety", "We start with your immediate safety and whether an urgent order is needed."),
            ("folder-open", "Build the evidence", "We organize messages, photos, police reports and witness accounts into a clear record."),
            ("file-text", "Apply to the court", "We prepare your application and sworn statement and file it in the right court."),
            ("scales", "Argue the hearing", "We represent you in court, so you don't have to face the other person alone."),
            ("shield-check", "Serve and enforce", "We make sure the order is served and act quickly if it's breached."),
        ],
        "checklist_title": "What to bring",
        "checklist": [
            "A dated list of incidents, starting with the most serious",
            "Threatening messages, voicemails and social media posts",
            "Photos of injuries or damaged property",
            "Police report numbers and officer names",
            "Names and contact details of any witnesses",
            "Copies of any previous court orders",
        ],
        "faqs": [
            ("How quickly can I get a restraining order?", "When there is an urgent risk, courts can grant a temporary order quickly, sometimes without the other person being notified first. A full hearing follows. We'll tell you what's realistic where you live."),
            ("Will I have to see the other person in court?", "Possibly, at the hearing. We'll prepare you, stand with you and speak for you. Some courts allow remote attendance or other safety arrangements, and we'll ask for them where appropriate."),
            ("How long does an order last?", "It depends on the type of order and the court. Some last a set period, others until the court changes them. We'll explain the duration and help you extend it if needed."),
            ("What happens if they violate the order?", "Document it and report it to police right away. Breaching a court order can lead to arrest and charges. We can also go back to court on your behalf."),
        ],
        "lawyers": ["rebecca-anderson", "noah-katz"],
        "related": ["harassment", "extortion-blackmail", "defamation"],
    },
    {
        "slug": "defamation",
        "name": "Defamation",
        "select_label": "Defamation or false statements",
        "icon": "newspaper",
        "nav_desc": "Fight false statements and damaging posts.",
        "summary": "False reviews, damaging posts and lies told to clients or employers. We remove the content, correct the record and seek compensation.",
        "photo": ("1504711434969-e33886168f5c", "A stack of folded newspapers"),
        "meta_title": "Defamation Lawyers | False Reviews & Online Posts | Cohen & Silverman",
        "meta_desc": "False reviews, defamatory posts or lies told to your clients? Cohen & Silverman acts quickly to remove content, demand retractions and claim damages.",
        "h1": "Your reputation took years to <em>build.</em>",
        "lead": "False reviews, damaging posts, lies told to clients or employers. We move to remove the content, correct the record and seek compensation.",
        "overview": [
            "Defamation is the publication of a false statement that harms someone's reputation. Online, it spreads quickly and stays searchable for years.",
            "We act on two tracks: getting the content taken down or corrected as quickly as possible, and holding the person responsible. Some defamation claims have very short notice deadlines, so early advice matters.",
        ],
        "notice": ("hourglass-medium", "Some defamation claims require formal notice within weeks of the publication. Get advice early."),
        "matters": [
            ("star-half", "Fake and malicious reviews", "False reviews posted by competitors, former employees or people who were never customers."),
            ("chat-centered-text", "Defamatory social media posts", "Damaging false claims on social platforms, forums and comment sections."),
            ("briefcase", "False statements to clients or employers", "Lies told to people whose opinion affects your income or career."),
            ("user-focus", "Impersonation", "Accounts or websites pretending to be you or your business."),
            ("trash", "Takedowns and de-indexing", "Requests to platforms, hosts and search engines to remove or de-list content."),
            ("note-pencil", "Retractions and apologies", "Formal demands that the person publicly correct the record."),
        ],
        "stages": [
            ("camera", "Preserve", "We capture the content properly, with dates and URLs, before it can be edited or deleted."),
            ("magnifying-glass", "Assess", "We look at whether the statement is false, harmful and actionable, and at any deadlines."),
            ("envelope-simple", "Demand", "A formal letter demanding removal, retraction and an apology often resolves it."),
            ("scales", "Litigate", "If needed, we sue for damages and seek court orders requiring removal."),
        ],
        "checklist_title": "Do this now",
        "checklist": [
            "Screenshot the content with the date, time and URL visible",
            "Don't respond publicly or argue in the comments",
            "Note who has seen it and any effect on your work or business",
            "Save evidence of lost clients, sales or opportunities",
            "Contact us quickly, because notice deadlines can be short",
        ],
        "faqs": [
            ("What's the difference between defamation and a bad review?", "Honest opinion, even harsh opinion, is generally protected. Defamation involves false statements of fact that harm your reputation. We'll help you tell the difference."),
            ("Can I find out who posted an anonymous review?", "Often, yes. Courts can order platforms and service providers to disclose identifying information when there's a valid claim."),
            ("How fast can content be taken down?", "Platform removals can happen within days when content breaks their policies. Court-ordered removal takes longer but carries more force."),
            ("Is there a deadline to sue?", "Yes, and it can be short. Some jurisdictions require notice within weeks of learning about the publication. Don't wait to get advice."),
        ],
        "lawyers": ["joshua-silverman", "benjamin-cohen"],
        "related": ["harassment", "extortion-blackmail", "debt-recovery"],
    },
    {
        "slug": "fraud-civil-theft",
        "name": "Fraud & Civil Theft",
        "select_label": "Fraud or civil theft",
        "icon": "vault",
        "nav_desc": "Trace and recover money taken by deception.",
        "summary": "Scams, misappropriated funds and contractors who vanish with deposits. We trace the money, freeze assets where possible and sue to get it back.",
        "photo": ("1563013544-824ae1b704d3", "A payment card held over a laptop keyboard"),
        "meta_title": "Fraud & Civil Theft Lawyers | Recover Stolen Money | Cohen & Silverman",
        "meta_desc": "Scammed, defrauded or left with a missing deposit? Cohen & Silverman traces funds, seeks asset freezing orders and sues to recover your money.",
        "h1": "When money is taken by <em>deception.</em>",
        "lead": "Scams, misappropriated funds, contractors who vanish with deposits. We trace the money, freeze assets where possible and sue to get it back.",
        "overview": [
            "Fraud cases are a race against time. The longer money sits with the wrong person, the more likely it is to be spent, moved or hidden.",
            "We act fast to trace where funds went and, where the evidence supports it, ask the court to freeze assets before they disappear. Then we pursue judgment and enforcement against everyone responsible.",
        ],
        "notice": ("phone", "If you've just sent money to a scammer, call your bank's fraud line immediately. Fast action can sometimes stop or reverse a transfer."),
        "matters": [
            ("hammer", "Contractors who take deposits", "Builders and tradespeople who took payment and never finished, or never started."),
            ("handshake", "Business partner misappropriation", "Partners, directors or employees who diverted company money."),
            ("heart", "Romance and investment scams", "Recovery claims where the people or receiving accounts can be identified."),
            ("arrows-left-right", "Fraudulent transfers", "Assets moved to relatives or new companies to avoid paying what's owed."),
            ("magnifying-glass", "Asset tracing", "Following the money through bank records and court-ordered disclosure."),
            ("vault", "Asset freezing orders", "Urgent court orders preventing funds and property from being moved."),
        ],
        "stages": [
            ("magnifying-glass", "Trace", "We follow the money using your records and, where needed, court-ordered disclosure from banks."),
            ("lock-key", "Freeze", "If assets are at risk, we ask the court for an urgent order to stop them being moved."),
            ("scales", "Sue", "We bring claims against everyone responsible, including those who received the money."),
            ("hand-coins", "Recover", "We enforce the judgment against accounts, property and other assets."),
        ],
        "checklist_title": "What to gather",
        "checklist": [
            "Every payment record: transfers, receipts and card statements",
            "Contracts, quotes, invoices and messages",
            "Names, company names and websites used",
            "Details of the accounts the money was sent to",
            "Any police or bank fraud report numbers",
        ],
        "faqs": [
            ("Can I get money back from a scammer?", "It depends on whether the people or accounts can be identified and whether assets can be reached. We'll assess that honestly before you spend money on litigation."),
            ("What is a freezing order?", "A court order that stops a person from moving or spending assets until the case is decided. They're powerful, so courts require strong evidence and quick action."),
            ("Should I report fraud to police too?", "Yes. A police report supports your case and may lead to criminal charges. A civil claim runs separately and focuses on getting your money back."),
            ("Can I sue people who received the stolen money?", "In many cases, yes. Claims can extend to people and companies who knowingly received or helped move the funds."),
        ],
        "lawyers": ["benjamin-cohen", "noah-katz"],
        "related": ["debt-recovery", "extortion-blackmail", "defamation"],
    },
]
AREA = {a["slug"]: a for a in AREAS}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def esc(s):
    return html.escape(s, quote=True)


def ux(photo_id, w, q=72):
    return f"https://images.unsplash.com/photo-{photo_id}?auto=format&fit=crop&w={w}&q={q}"


def photo(photo_id, alt, sizes="(max-width: 1023px) 92vw, 50vw", cls="", eager=False, widths=(480, 800, 1200, 1600)):
    srcset = ", ".join(f"{ux(photo_id, w)} {w}w" for w in widths)
    loading = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    classes = " ".join(c for c in ("photo", cls) if c)
    return (f'<div class="{classes}">'
            f'<img src="{ux(photo_id, widths[1])}" srcset="{srcset}" sizes="{sizes}" alt="{esc(alt)}" {loading} decoding="async"></div>')


def named_photo(key, **kw):
    pid, alt = PHOTOS[key]
    return photo(pid, alt, **kw)


def icon(name, light=True, cls=""):
    weight = "ph-light" if light else "ph"
    return f'<i class="{weight} ph-{name}{(" " + cls) if cls else ""}" aria-hidden="true"></i>'


def portrait(a, cls=""):
    headshot = ROOT / "assets" / "img" / "team" / f"{a['slug']}.jpg"
    if headshot.exists():
        # The lawyer's name always sits right next to the photo, so the image itself is decorative.
        inner = (f'<img class="portrait-photo" src="assets/img/team/{a["slug"]}.jpg" alt="" '
                 f'width="768" height="1024" loading="lazy" decoding="async">')
        return f'<div class="portrait has-photo {cls}" aria-hidden="true">{inner}</div>'
    return (f'<div class="portrait {cls}" aria-hidden="true">'
            f'<!-- Add a headshot at assets/img/team/{a["slug"]}.jpg and rebuild to replace this placeholder. -->'
            f'<span class="portrait-initials">{a["initials"]}</span>'
            f'<img class="portrait-mark" src="assets/img/brand/mark-scales-white.webp" alt="" loading="lazy" width="44" height="31">'
            f'</div>')


def accordion(items, prefix):
    out = []
    for i, (q, a) in enumerate(items, 1):
        qid, pid = f"{prefix}-q{i}", f"{prefix}-a{i}"
        out.append(
            f'<div class="accordion-item"><h3>'
            f'<button class="accordion-trigger" type="button" id="{qid}" aria-expanded="false" aria-controls="{pid}">'
            f'<span>{esc(q)}</span><span class="accordion-icon" aria-hidden="true"><i class="ph ph-plus"></i></span></button></h3>'
            f'<div class="accordion-panel" id="{pid}" role="region" aria-labelledby="{qid}"><div><p>{esc(a)}</p></div></div></div>'
        )
    return "\n".join(out)


def faq_jsonld(items):
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items
        ],
    }
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def tel():
    return f'tel:{FIRM["phone_href"]}'


def asset_version(rel):
    """Short content hash so browsers always load the latest CSS and JS."""
    import hashlib
    return hashlib.md5((ROOT / rel).read_bytes()).hexdigest()[:8]


# ---------------------------------------------------------------------------
# Shared layout
# ---------------------------------------------------------------------------
SITE_URL = "https://cohensilverman.com"


def page_url(name):
    return f"{SITE_URL}/" if name == "index" else f"{SITE_URL}/{name}.html"


def firm_jsonld():
    data = {
        "@context": "https://schema.org",
        "@type": "LegalService",
        "name": FIRM["name"],
        "url": f"{SITE_URL}/",
        "logo": f"{SITE_URL}/assets/img/brand/og-image.png",
        "image": f"{SITE_URL}/assets/img/brand/og-image.png",
        "description": "Debt recovery, harassment, extortion and blackmail, restraining orders, defamation, and fraud and civil theft.",
        "telephone": FIRM["phone"],
        "email": FIRM["email"],
        "address": {"@type": "PostalAddress", "streetAddress": FIRM["address_1"], "addressLocality": "Toronto", "addressRegion": "ON", "postalCode": "M5H 1W2", "addressCountry": "CA"},
        "openingHours": "Mo-Fr 08:30-18:00",
        "employee": [{"@type": "Person", "name": a["name"], "jobTitle": a["role"]} for a in ATTORNEYS],
    }
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def seo_links(meta):
    name = meta.get("_name", "")
    if name == "404":
        return '<meta name="robots" content="noindex">\n<base href="/">'
    url = page_url(name)
    return f'<link rel="canonical" href="{url}">\n<meta property="og:url" content="{url}">'


def head(meta):
    extra = meta.get("head_extra", "")
    if meta.get("schema") == "firm":
        extra += "\n" + firm_jsonld() + "\n" + faq_jsonld(HOME_FAQS)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="format-detection" content="telephone=no, address=no, email=no">
<meta name="apple-mobile-web-app-title" content="Cohen &amp; Silverman">
<title>{esc(meta['title'])}</title>
<meta name="description" content="{esc(meta['description'])}">
<meta name="theme-color" content="#042a59">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Cohen &amp; Silverman Law Firm">
<meta property="og:title" content="{esc(meta['title'])}">
<meta property="og:description" content="{esc(meta['description'])}">
<meta property="og:image" content="{SITE_URL}/assets/img/brand/og-image.png">
{seo_links(meta)}
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="32x32" href="assets/img/brand/favicon-32.png">
<link rel="icon" type="image/png" sizes="64x64" href="assets/img/brand/favicon-64.png">
<link rel="apple-touch-icon" href="assets/img/brand/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://images.unsplash.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400..700;1,8..60,400..600&display=swap">
<link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.1.1/src/regular/style.css">
<link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.1.1/src/light/style.css">
<link rel="stylesheet" href="assets/css/styles.css?v={asset_version('assets/css/styles.css')}">
<script>document.documentElement.classList.add('js')</script>
<script src="assets/js/main.js?v={asset_version('assets/js/main.js')}" defer></script>
{extra}
</head>"""


def site_header(nav):
    def cur(key):
        return ' aria-current="page"' if nav == key else ""

    mega_links = "\n".join(
        f'<a class="mega-link" href="{a["slug"]}.html">{icon(a["icon"])}'
        f'<span><strong>{esc(a["name"])}</strong><small>{esc(a["nav_desc"])}</small></span></a>'
        for a in AREAS
    )
    mobile_links = "\n".join(
        f'<a href="{a["slug"]}.html">{icon(a["icon"])}{esc(a["name"])}</a>' for a in AREAS
    )
    practice_cls = " is-current" if nav == "practice" else ""
    return f"""<body>
<div class="scroll-sentinel" aria-hidden="true"></div>
<a class="skip-link" href="#main">Skip to content</a>
<div class="topbar on-dark">
  <div class="container topbar-inner">
    <p>{icon('lock-simple')}Confidential consultations for individuals and businesses</p>
    <ul>
      <li>{icon('clock')}{FIRM['hours_short']}</li>
      <li><a href="mailto:{FIRM['email']}">{icon('envelope-simple')}{FIRM['email']}</a></li>
      <li><a href="{tel()}">{icon('phone')}{FIRM['phone']}</a></li>
    </ul>
  </div>
</div>
<header class="site-header" data-header>
  <div class="container header-inner">
    <a class="brand" href="index.html" aria-label="Cohen &amp; Silverman Law Firm, home">
      <img src="assets/img/brand/logo-horizontal-navy.webp" alt="Cohen &amp; Silverman Law Firm" width="247" height="44">
    </a>
    <nav class="primary-nav" aria-label="Main">
      <ul class="nav-list">
        <li class="has-mega" data-mega>
          <button class="nav-link nav-trigger{practice_cls}" type="button" aria-expanded="false" aria-controls="mega-practice">Practice Areas <i class="ph ph-caret-down" aria-hidden="true"></i></button>
          <div class="mega" id="mega-practice">
            <div class="mega-grid">
{mega_links}
            </div>
            <div class="mega-foot">
              <span>Not sure where your situation fits?</span>
              <a class="link-arrow" href="practice-areas.html">All practice areas <i class="ph ph-arrow-right" aria-hidden="true"></i></a>
            </div>
          </div>
        </li>
        <li><a class="nav-link" href="attorneys.html"{cur('lawyers')}>Our Lawyers</a></li>
        <li><a class="nav-link" href="guides.html"{cur('guides')}>Guides</a></li>
        <li><a class="nav-link" href="about.html"{cur('about')}>About</a></li>
        <li><a class="nav-link" href="contact.html"{cur('contact')}>Contact</a></li>
      </ul>
    </nav>
    <a class="nav-phone" href="{tel()}">{icon('phone')}<span>{FIRM['phone']}</span></a>
    <a class="btn btn--primary btn--sm header-cta" href="contact.html">Book a consultation</a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="mobile-nav" aria-label="Open menu"><i class="ph ph-list" aria-hidden="true"></i></button>
  </div>
</header>

<div class="mobile-nav on-dark" id="mobile-nav" role="dialog" aria-modal="true" aria-label="Menu" aria-hidden="true">
  <div class="mobile-nav-top">
    <a href="index.html" aria-label="Home"><img src="assets/img/brand/logo-horizontal-white.webp" alt="Cohen &amp; Silverman Law Firm" width="225" height="40"></a>
    <button class="mobile-close" type="button" aria-label="Close menu"><i class="ph ph-x" aria-hidden="true"></i></button>
  </div>
  <div class="mobile-nav-body">
    <ul class="mobile-links">
      <li>
        <details{' open' if nav == 'practice' else ''}>
          <summary>Practice Areas <i class="ph ph-plus" aria-hidden="true"></i></summary>
          <div class="mobile-sub">
{mobile_links}
            <a href="practice-areas.html">{icon('squares-four')}All practice areas</a>
          </div>
        </details>
      </li>
      <li><a href="attorneys.html">Our Lawyers <i class="ph ph-arrow-right" aria-hidden="true"></i></a></li>
      <li><a href="guides.html">Guides <i class="ph ph-arrow-right" aria-hidden="true"></i></a></li>
      <li><a href="about.html">About <i class="ph ph-arrow-right" aria-hidden="true"></i></a></li>
      <li><a href="contact.html">Contact <i class="ph ph-arrow-right" aria-hidden="true"></i></a></li>
    </ul>
    <div class="mobile-nav-foot">
      <a class="mobile-phone" href="{tel()}">{icon('phone')}{FIRM['phone']}</a>
      <a class="btn btn--light btn--block" href="contact.html">Book a consultation</a>
    </div>
  </div>
</div>
"""


def site_footer(nav=""):
    area_links = "\n".join(f'<li><a href="{a["slug"]}.html">{esc(a["name"])}</a></li>' for a in AREAS)
    return f"""
<footer class="site-footer on-dark">
  <div class="container">
    <div class="footer-top">
      <div class="footer-brand">
        <img src="assets/img/brand/logo-stacked-white.webp" alt="Cohen &amp; Silverman Law Firm" width="230" height="100" loading="lazy">
        <p>Litigation for people who are owed money, and protection for people who are being harassed, threatened or exploited.</p>
      </div>
      <div class="footer-col">
        <h2>Practice areas</h2>
        <ul>
{area_links}
        </ul>
      </div>
      <div class="footer-col">
        <h2>Firm</h2>
        <ul>
          <li><a href="attorneys.html">Our Lawyers</a></li>
          <li><a href="about.html">About the firm</a></li>
          <li><a href="practice-areas.html">All practice areas</a></li>
          <li><a href="guides.html">Guides</a></li>
          <li><a href="contact.html">Book a consultation</a></li>
        </ul>
      </div>
      <div class="footer-col footer-contact">
        <h2>Contact</h2>
        <ul>
          <li>{icon('phone')}<a href="{tel()}">{FIRM['phone']}</a></li>
          <li>{icon('envelope-simple')}<a href="mailto:{FIRM['email']}">{FIRM['email']}</a></li>
          <li>{icon('map-pin')}<span>{FIRM['address_1']}<br>{FIRM['address_2']}</span></li>
          <li>{icon('clock')}<span>{FIRM['hours']}</span></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <div class="footer-bottom-row">
        <p>&copy; <span data-year>2026</span> Cohen &amp; Silverman Law Firm. All rights reserved.</p>
        <nav class="footer-legal-links" aria-label="Legal">
          <a href="legal.html#disclaimer">Disclaimer</a>
          <a href="legal.html#privacy">Privacy</a>
          <a href="legal.html#terms">Terms of use</a>
          <a href="legal.html#accessibility">Accessibility</a>
        </nav>
      </div>
      <p class="footer-disclaimer">The information on this website is general information only and is not legal advice. Contacting us through this website does not create a lawyer-client relationship. Please do not send confidential information until we have confirmed that we can act for you.</p>
    </div>
  </div>
</footer>
{mobile_bar(nav)}
</body>
</html>
"""


def mobile_bar(nav=""):
    if nav == "contact":
        second = (f'<a class="mobile-bar-btn" href="mailto:{FIRM["email"]}">'
                  f'<i class="ph ph-envelope-simple" aria-hidden="true"></i>Email us</a>')
    else:
        second = ('<a class="mobile-bar-btn mobile-bar-btn--primary" href="contact.html">'
                  '<i class="ph ph-calendar-check" aria-hidden="true"></i><span class="mb-long">Book a consultation</span><span class="mb-short">Book now</span></a>')
    return f"""<nav class="mobile-bar" aria-label="Quick contact">
  <a class="mobile-bar-btn" href="tel:{FIRM['phone_href']}"><i class="ph ph-phone" aria-hidden="true"></i><span class="mb-long">Call {FIRM['phone']}</span><span class="mb-short">Call us</span></a>
  {second}
</nav>"""


def cta_band(title="Tell us what happened.", text="A short, confidential conversation is the quickest way to understand your options. We'll tell you plainly what we can do.", matter=None):
    href = f"contact.html?matter={matter}" if matter else "contact.html"
    return f"""
<section class="cta-band on-dark" aria-labelledby="cta-title">
  <img class="cta-mark" src="assets/img/brand/mark-scales-white.webp" alt="" aria-hidden="true" loading="lazy" width="420" height="299">
  <div class="container cta-band-inner">
    <div data-reveal>
      <h2 class="display-2" id="cta-title">{title}</h2>
      <p>{text}</p>
    </div>
    <div class="cta-actions" data-reveal>
      <a class="btn btn--light" href="{href}">Book a consultation <i class="ph ph-arrow-right" aria-hidden="true"></i></a>
      <a class="cta-phone" href="{tel()}">{icon('phone')}{FIRM['phone']}</a>
    </div>
  </div>
</section>"""


def team_grid(heading_level="h3"):
    cards = []
    for a in ATTORNEYS:
        cards.append(
            f'<a class="person-card" href="attorneys.html#{a["slug"]}" data-reveal>'
            f'{portrait(a)}'
            f'<{heading_level} class="person-name">{esc(a["name"])}</{heading_level}>'
            f'<p class="person-role">{esc(a["role"])}</p>'
            f'<p class="person-focus">{esc(a["focus_short"])}</p></a>'
        )
    return '<div class="team-grid" data-reveal-group>\n' + "\n".join(cards) + "\n</div>"


def area_options():
    opts = ['<option value="" disabled selected>Choose one</option>']
    opts += [f'<option value="{a["slug"]}">{esc(a["select_label"])}</option>' for a in AREAS]
    opts.append('<option value="other">Something else</option>')
    return "\n".join(opts)


def breadcrumbs(*trail):
    parts = ['<a href="index.html">Home</a>']
    for label, href in trail:
        parts.append('<span class="sep" aria-hidden="true">/</span>')
        parts.append(f'<a href="{href}">{esc(label)}</a>' if href else f'<span aria-current="page">{esc(label)}</span>')
    return f'<nav class="breadcrumbs" aria-label="Breadcrumb">{"".join(parts)}</nav>'


# ---------------------------------------------------------------------------
# Generated pages
# ---------------------------------------------------------------------------
def practice_page(a):
    lead = ATT[a["lawyers"][0]]
    matters = "\n".join(
        f'<div class="matter" data-reveal>{icon(ic)}<h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for ic, t, d in a["matters"]
    )
    stages = "\n".join(
        f'<li class="stage" data-reveal><span class="stage-marker">{icon(ic)}</span><div><h3>{esc(t)}</h3><p>{esc(d)}</p></div></li>'
        for ic, t, d in a["stages"]
    )
    checks = "\n".join(f'<li><i class="ph ph-check" aria-hidden="true"></i><span>{esc(c)}</span></li>' for c in a["checklist"])
    notice = ""
    if a.get("notice"):
        ic, text = a["notice"]
        notice = f'<div class="notice" role="note">{icon(ic)}<p>{esc(text)}</p></div>'
    others = "\n".join(
        f'<li><a href="{o["slug"]}.html">{esc(o["name"])} <i class="ph ph-arrow-right" aria-hidden="true"></i></a></li>'
        for o in AREAS if o["slug"] != a["slug"]
    )
    related = "\n".join(
        f'<a class="related-card" href="{r}.html" data-reveal>{icon(AREA[r]["icon"])}<h3>{esc(AREA[r]["name"])}</h3>'
        f'<p>{esc(AREA[r]["nav_desc"])}</p><span class="tile-link">Learn more <i class="ph ph-arrow-right" aria-hidden="true"></i></span></a>'
        for r in a["related"]
    )
    team = " and ".join(f'<a href="attorneys.html#{s}">{esc(ATT[s]["name"])}</a>' for s in a["lawyers"])
    pid, alt = a["photo"]

    body = f"""
<main id="main">
<section class="page-hero page-hero--split on-dark">
  <div class="container page-hero-inner">
    <div>
      {breadcrumbs(("Practice Areas", "practice-areas.html"), (a["name"], None))}
      <p class="eyebrow">{esc(a["name"])}</p>
      <h1>{a["h1"]}</h1>
      <p class="lead">{esc(a["lead"])}</p>
      <div class="page-hero-actions">
        <a class="btn btn--light" href="contact.html?matter={a['slug']}">Book a consultation <i class="ph ph-arrow-right" aria-hidden="true"></i></a>
        <a class="btn btn--outline-light" href="{tel()}"><i class="ph ph-phone" aria-hidden="true"></i><span class="mb-long">Call {FIRM['phone']}</span><span class="mb-short">Call us</span></a>
      </div>
    </div>
    <div class="page-hero-media framed">{photo(pid, alt, sizes="(max-width: 1023px) 92vw, 520px", eager=True)}</div>
  </div>
</section>

<section class="section">
  <div class="container practice-layout">
    <div class="practice-main">
      <div class="practice-intro" data-reveal>
        <p>{esc(a["overview"][0])}</p>
        <p>{esc(a["overview"][1])}</p>
        <p>Matters in this area are led by {team}.</p>
        {notice}
      </div>

      <section aria-labelledby="matters-title">
        <h2 id="matters-title" data-reveal>What we handle</h2>
        <div class="matters" data-reveal-group>
{matters}
        </div>
      </section>

      <section aria-labelledby="approach-title">
        <h2 id="approach-title" data-reveal>How we approach it</h2>
        <ol class="stages" data-reveal-group>
{stages}
        </ol>
      </section>

      <section class="checklist-panel" aria-labelledby="checklist-title" data-reveal>
        <h2 id="checklist-title">{esc(a["checklist_title"])}</h2>
        <ul class="check-list check-list--two">
{checks}
        </ul>
      </section>
      {guide_callout(a["slug"])}

      <section aria-labelledby="faq-title">
        <h2 id="faq-title" data-reveal>Common questions</h2>
        <div class="accordion" data-reveal>
{accordion(a["faqs"], a["slug"])}
        </div>
      </section>
    </div>

    <aside class="practice-aside" aria-label="Book a consultation">
      {consult_card(a["slug"])}
      <div class="aside-box">
        <h2>Other practice areas</h2>
        <ul class="aside-links">
{others}
        </ul>
      </div>
    </aside>
  </div>
</section>

<section class="section section--paper section--tight" aria-labelledby="related-title">
  <div class="container">
    <h2 class="display-2" id="related-title" data-reveal>Related practice areas</h2>
    <div class="related" data-reveal-group style="margin-top:40px">
{related}
    </div>
  </div>
</section>
{cta_band(matter=a["slug"])}
</main>"""
    meta = {
        "title": a["meta_title"],
        "description": a["meta_desc"],
        "nav": "practice",
        "head_extra": faq_jsonld(a["faqs"]),
    }
    return meta, body


def practice_index():
    rows = []
    for a in AREAS:
        tags = "".join(f'<span class="tag">{esc(t)}</span>' for _, t, _ in a["matters"][:4])
        pid, alt = a["photo"]
        rows.append(f"""
<article class="area-row" data-reveal>
  {icon(a["icon"], cls="area-row-icon")}
  <h2><a href="{a['slug']}.html">{esc(a["name"])}</a></h2>
  <div class="area-row-desc">
    <p>{esc(a["summary"])}</p>
    <div class="area-row-tags">{tags}</div>
    <a class="link-arrow" href="{a['slug']}.html">Explore {esc(a["name"])} <i class="ph ph-arrow-right" aria-hidden="true"></i></a>
  </div>
  <a class="area-row-media" href="{a['slug']}.html" tabindex="-1" aria-hidden="true">{photo(pid, alt, sizes="(max-width: 767px) 92vw, 220px", widths=(320, 480, 800))}</a>
</article>""")
    body = f"""
<main id="main">
<section class="page-hero page-hero--split on-dark">
  <div class="container page-hero-inner">
    <div>
      {breadcrumbs(("Practice Areas", None))}
      <h1>Recovery and <em>protection.</em></h1>
      <p class="lead">We focus on a small number of areas and know them well: getting back money you're owed, and protecting you from people who harass, threaten or deceive.</p>
      <div class="page-hero-actions">
        <a class="btn btn--light" href="contact.html">Book a consultation <i class="ph ph-arrow-right" aria-hidden="true"></i></a>
      </div>
    </div>
    <div class="page-hero-media framed">{named_photo("columns", sizes="(max-width: 1023px) 92vw, 520px", eager=True)}</div>
  </div>
</section>

<section class="section" aria-label="Practice areas">
  <div class="container">
    <div class="area-list">
{"".join(rows)}
    </div>
  </div>
</section>
{cta_band(title="Not sure where your situation fits?", text="Many matters touch more than one area. Tell us what happened and we'll work out the right approach together.")}
</main>"""
    meta = {
        "title": "Practice Areas | Cohen & Silverman Law Firm",
        "description": "Debt recovery, harassment, extortion and blackmail, restraining orders, defamation, and fraud and civil theft. See how Cohen & Silverman can help.",
        "nav": "practice",
    }
    return meta, body


def attorneys_page():
    cards, dialogs = [], []
    for a in ATTORNEYS:
        tags = "".join(f'<a class="tag" href="{slug}.html">{esc(label)}</a>' for label, slug in a["focus"])
        bio = "".join(f"<p>{esc(p)}</p>" for p in a["bio"])
        cards.append(f"""
<article class="attorney-card" id="{a['slug']}" data-reveal>
  {portrait(a)}
  <div class="attorney-body">
    <h2>{esc(a["name"])}</h2>
    <p class="person-role">{esc(a["role"])}</p>
    <p>{esc(a["short"])}</p>
    <div class="focus-list">{tags}</div>
    <button class="btn btn--outline" type="button" data-dialog-open="bio-{a['slug']}" aria-haspopup="dialog">Read full bio <i class="ph ph-arrow-right" aria-hidden="true"></i></button>
  </div>
</article>""")
        dialogs.append(f"""
<dialog class="bio-dialog" id="bio-{a['slug']}" aria-labelledby="bio-{a['slug']}-title">
  <div class="bio-dialog-inner">
    {portrait(a)}
    <div class="bio-dialog-body">
      <button class="dialog-close" type="button" data-dialog-close aria-label="Close biography"><i class="ph ph-x" aria-hidden="true"></i></button>
      <p class="person-role">{esc(a["role"])}</p>
      <h2 id="bio-{a['slug']}-title">{esc(a["name"])}</h2>
      <div class="prose">{bio}</div>
      <div class="focus-list">{tags}</div>
      <div class="bio-dialog-actions">
        <a class="btn btn--primary" href="contact.html">Book a consultation <i class="ph ph-arrow-right" aria-hidden="true"></i></a>
        <a class="btn btn--outline" href="{tel()}"><i class="ph ph-phone" aria-hidden="true"></i><span class="mb-long">Call {FIRM['phone']}</span><span class="mb-short">Call us</span></a>
      </div>
    </div>
  </div>
</dialog>""")

    body = f"""
<main id="main">
<section class="page-hero page-hero--split on-dark">
  <div class="container page-hero-inner">
    <div>
      {breadcrumbs(("Our Lawyers", None))}
      <h1>The lawyers who will handle <em>your matter.</em></h1>
      <p class="lead">Four lawyers focused on recovery and protection work. You'll know who is responsible for your case from the first conversation.</p>
    </div>
    <div class="page-hero-media framed">{named_photo("books", sizes="(max-width: 1023px) 92vw, 520px", eager=True)}</div>
  </div>
</section>

<section class="section" aria-label="Lawyers">
  <div class="container">
    <div class="attorney-grid" data-reveal-group>
{"".join(cards)}
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <p class="statement" data-reveal>Every matter has one lawyer who owns it, and a whole firm <em>behind it.</em></p>
    <div class="story-cols" data-reveal>
      <p>Your lead lawyer is responsible for your case from the first call to the final outcome. You'll have their direct line, and you won't be passed between people who don't know your file.</p>
      <p>Behind them, the rest of the firm is available when it helps: a second view on strategy, extra hands when a deadline is tight, and a partner's review before anything important is filed with the court.</p>
    </div>
  </div>
</section>
{cta_band()}
</main>
{"".join(dialogs)}"""
    meta = {
        "title": "Our Lawyers | Cohen & Silverman Law Firm",
        "description": "Meet Benjamin Cohen, Joshua Silverman, Rebecca Anderson and Noah Katz, the lawyers at Cohen & Silverman Law Firm.",
        "nav": "lawyers",
    }
    return meta, body


# ---------------------------------------------------------------------------
# Guides, shared consultation card and contact form
# ---------------------------------------------------------------------------
_guides = runpy.run_path(str(HERE / "guides.py"))
GUIDES, AREA_GUIDE, GUIDES_UPDATED = _guides["GUIDES"], _guides["AREA_GUIDE"], _guides["UPDATED"]


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def read_minutes(g):
    words = 0
    for _, blocks in g["sections"]:
        for b in blocks:
            words += len(b.split()) if isinstance(b, str) else sum(len(x.split()) for x in b)
    return max(2, -(-words // 200))  # whole minutes, rounded up, at about 200 words a minute


def guide_meta(g):
    return (f'<p class="guide-meta"><span>{esc(AREA[g["area"]]["name"])}</span>'
            f'<span>{read_minutes(g)} min read</span></p>')


def guide_photo(g, **kw):
    pid, alt = g.get("photo") or AREA[g["area"]]["photo"]
    return photo(pid, alt, **kw)


def consult_card(area_slug):
    a = AREA[area_slug]
    lead = ATT[a["lawyers"][0]]
    return f"""<div class="consult-card on-dark">
        <p class="label">Lead lawyer</p>
        <a class="consult-person" href="attorneys.html#{lead['slug']}">
          {portrait(lead)}
          <span><strong>{esc(lead["name"])}</strong><span>{esc(lead["role"])}</span></span>
        </a>
        <p>Tell us what happened in a confidential consultation. We'll explain your options and likely costs before you commit to anything.</p>
        <a class="btn btn--light btn--block" href="contact.html?matter={area_slug}">Book a consultation</a>
        <a class="btn btn--outline-light btn--block" href="{tel()}"><i class="ph ph-phone" aria-hidden="true"></i><span class="mb-long">Call {FIRM['phone']}</span><span class="mb-short">Call us</span></a>
      </div>"""


def guide_callout(area_slug):
    g = AREA_GUIDE.get(area_slug)
    if not g:
        return ""
    return (f'<a class="guide-callout" href="{g["slug"]}.html" data-reveal>{icon("book-open-text")}'
            f'<span><small>Read our guide</small><strong>{esc(g["title"])}</strong></span>'
            f'<i class="ph ph-arrow-right" aria-hidden="true"></i></a>')


def guides_home():
    first, rest = GUIDES[0], GUIDES[1:]
    rows = "\n".join(
        f'<a class="guide-row" href="{g["slug"]}.html" data-reveal><span>{guide_meta(g)}'
        f'<h3>{esc(g["short_title"])}</h3><p>{esc(g["summary"])}</p></span>'
        f'<i class="ph ph-arrow-right" aria-hidden="true"></i></a>'
        for g in rest
    )
    return f"""<div class="guides-feature">
      <a class="guide-card-lg" href="{first['slug']}.html" data-reveal>
        {guide_photo(first, sizes="(max-width: 1023px) 92vw, 600px")}
        <div class="guide-body">
          {guide_meta(first)}
          <h3>{esc(first["title"])}</h3>
          <p>{esc(first["summary"])}</p>
          <span class="tile-link">Read the guide <i class="ph ph-arrow-right" aria-hidden="true"></i></span>
        </div>
      </a>
      <div class="guide-list" data-reveal-group>
{rows}
      </div>
    </div>"""


def guides_index():
    cards = []
    for i, g in enumerate(GUIDES):
        featured = i == 0
        cards.append(f"""
<a class="guide-card{' guide-card--featured' if featured else ''}" href="{g['slug']}.html" data-reveal>
  {guide_photo(g, sizes="(max-width: 767px) 92vw, " + ("640px" if featured else "400px"), eager=featured)}
  <div class="guide-body">
    {guide_meta(g)}
    <h3>{esc(g["title"])}</h3>
    <p>{esc(g["summary"])}</p>
    <span class="tile-link">Read the guide <i class="ph ph-arrow-right" aria-hidden="true"></i></span>
  </div>
</a>""")
    body = f"""
<main id="main">
<section class="page-hero page-hero--split on-dark">
  <div class="container page-hero-inner">
    <div>
      {breadcrumbs(("Guides", None))}
      <h1>Practical guides for difficult <em>situations.</em></h1>
      <p class="lead">Plain-language answers to the questions people bring to us most often: what to do first, what to keep, and what the legal process looks like.</p>
    </div>
    <div class="page-hero-media framed">{named_photo("office", sizes="(max-width: 1023px) 92vw, 520px", eager=True)}</div>
  </div>
</section>

<section class="section" aria-label="All guides">
  <div class="container">
    <div class="guide-grid" data-reveal-group>
{"".join(cards)}
    </div>
    <p class="guides-note">{icon("info")}<span>These guides are general information, not legal advice. The law varies by location and every situation is different, so speak with a lawyer about your circumstances.</span></p>
  </div>
</section>
{cta_band(title="Need advice on your situation?", text="A guide can only go so far. Tell us what happened and we'll explain your options plainly, in a confidential consultation.")}
</main>"""
    meta = {
        "title": "Guides | Cohen & Silverman Law Firm",
        "description": "Practical guides on recovering money owed, documenting harassment, restraining orders and responding to blackmail or sextortion.",
        "nav": "guides",
    }
    return meta, body


def guide_page(g):
    area = AREA[g["area"]]
    toc, sections = [], []
    for heading, blocks in g["sections"]:
        sid = slugify(heading)
        toc.append(f'<a href="#{sid}">{esc(heading)}</a>')
        inner = []
        for b in blocks:
            if isinstance(b, str):
                inner.append(f"<p>{esc(b)}</p>")
            else:
                inner.append('<ul class="article-list">' + "".join(f"<li>{esc(x)}</li>" for x in b) + "</ul>")
        sections.append(f'<section id="{sid}" aria-labelledby="{sid}-h"><h2 id="{sid}-h">{esc(heading)}</h2>{"".join(inner)}</section>')
    takeaways = "".join(f'<li><i class="ph ph-check" aria-hidden="true"></i><span>{esc(t)}</span></li>' for t in g["takeaways"])
    others = [o for o in GUIDES if o["slug"] != g["slug"]]
    more = "\n".join(
        f'<a class="guide-card" href="{o["slug"]}.html" data-reveal>{guide_photo(o, sizes="(max-width: 767px) 92vw, 400px")}'
        f'<div class="guide-body">{guide_meta(o)}<h3>{esc(o["short_title"])}</h3>'
        f'<span class="tile-link">Read the guide <i class="ph ph-arrow-right" aria-hidden="true"></i></span></div></a>'
        for o in others
    )
    body = f"""
<main id="main">
<section class="page-hero on-dark">
  <div class="container page-hero-inner">
    <div class="article-hero">
      {breadcrumbs(("Guides", "guides.html"), (g["short_title"], None))}
      <p class="eyebrow">{esc(area["name"])}</p>
      <h1>{esc(g["title"])}</h1>
      <p class="lead">{esc(g["summary"])}</p>
      <div class="article-meta">
        <span>{icon("clock")}{read_minutes(g)} min read</span>
        <span>{icon("calendar-blank")}Updated {GUIDES_UPDATED}</span>
        <span>{icon("scales")}Cohen &amp; Silverman Law Firm</span>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container article-layout">
    <article class="article-body">
      <div class="takeaways" data-reveal>
        <h2>Key takeaways</h2>
        <ul class="check-list">{takeaways}</ul>
      </div>
      {"".join(sections)}
      <p class="article-disclaimer">{icon("info")}<span>This guide is general information, not legal advice. Laws and deadlines differ by location, and the right steps depend on your circumstances. <a class="link-arrow" href="contact.html?matter={g['area']}">Book a consultation</a> for advice on your situation.</span></p>
    </article>
    <aside class="article-aside" aria-label="Guide contents and consultation">
      <nav class="toc-box" aria-label="In this guide">
        <h2>In this guide</h2>
        {"".join(toc)}
      </nav>
      {consult_card(g["area"])}
    </aside>
  </div>
</section>

<section class="section section--paper section--tight" aria-labelledby="more-guides">
  <div class="container">
    <h2 class="display-2" id="more-guides" data-reveal>More guides</h2>
    <div class="guide-grid" data-reveal-group style="margin-top:40px">
{more}
    </div>
  </div>
</section>
{cta_band(matter=g["area"])}
</main>"""
    meta = {"title": f'{g["short_title"]} | Cohen & Silverman Law Firm', "description": g["meta_desc"], "nav": "guides"}
    return meta, body


def contact_form(compact=False):
    def field(name, label, kind="text", auto="", extra=""):
        return f"""<div class="field">
            <label for="{name}">{label} <span class="req" aria-hidden="true">*</span></label>
            <input id="{name}" name="{name}" type="{kind}" autocomplete="{auto}" required aria-describedby="{name}-error"{extra}>
            <p class="field-error" id="{name}-error"><i class="ph ph-warning-circle" aria-hidden="true"></i><span></span></p>
          </div>"""

    title = "Request a consultation" if compact else "Tell us about your matter"
    intro = ("It takes about two minutes. Everything you share is kept confidential." if compact
             else 'Fields marked <span class="req">*</span> are required. Everything you share with us is kept confidential.')
    prefs = "" if compact else """
          <fieldset class="field field--full">
            <legend>How should we contact you?</legend>
            <div class="choice-row">
              <label class="choice"><input type="radio" name="contact_pref" value="Phone" checked><span><i class="ph ph-phone" aria-hidden="true"></i>Phone</span></label>
              <label class="choice"><input type="radio" name="contact_pref" value="Email"><span><i class="ph ph-envelope-simple" aria-hidden="true"></i>Email</span></label>
              <label class="choice"><input type="radio" name="contact_pref" value="Either"><span>Either is fine</span></label>
            </div>
          </fieldset>"""
    urgent = "" if compact else """
          <div class="field field--full">
            <label class="check"><input type="checkbox" name="urgent" value="yes"><span>This is urgent: there's a deadline, an active threat or a safety concern.</span></label>
          </div>"""
    return f"""<div class="form-card" data-reveal>
      <form data-contact-form data-endpoint="{FIRM['form_endpoint']}" data-email="{FIRM['email']}" novalidate>
        <h2>{title}</h2>
        <p>{intro}</p>
        <div class="form-grid">
          {field("first_name", "First name", auto="given-name")}
          {field("last_name", "Last name", auto="family-name")}
          {field("email", "Email", kind="email", auto="email", extra=' inputmode="email"')}
          {field("phone", "Phone", kind="tel", auto="tel", extra=' inputmode="tel"')}
          <div class="field field--full">
            <label for="matter">What is your matter about? <span class="req" aria-hidden="true">*</span></label>
            <select id="matter" name="matter" required aria-describedby="matter-error">
{area_options()}
            </select>
            <p class="field-error" id="matter-error"><i class="ph ph-warning-circle" aria-hidden="true"></i><span></span></p>
          </div>{prefs}
          <div class="field field--full">
            <label for="message">What happened? <span class="req" aria-hidden="true">*</span></label>
            <textarea id="message" name="message" rows="{4 if compact else 6}" required aria-describedby="message-hint message-error"></textarea>
            <p class="field-hint" id="message-hint">A few sentences is enough. Please don't include passwords, account numbers or intimate images.</p>
            <p class="field-error" id="message-error"><i class="ph ph-warning-circle" aria-hidden="true"></i><span></span></p>
          </div>{urgent}
          <div class="field field--full">
            <label class="check"><input type="checkbox" name="acknowledge" value="yes" required aria-describedby="acknowledge-error"><span>I understand that sending this form does not make Cohen &amp; Silverman my lawyers until we confirm in writing. <span class="req" aria-hidden="true">*</span></span></label>
            <p class="field-error" id="acknowledge-error"><i class="ph ph-warning-circle" aria-hidden="true"></i><span></span></p>
          </div>
          <div class="hp" aria-hidden="true">
            <label for="company_website">Leave this field empty</label>
            <input id="company_website" name="company_website" type="text" tabindex="-1" autocomplete="off">
          </div>
        </div>
        <div class="form-alert form-alert--error" role="alert"><i class="ph ph-warning-circle" aria-hidden="true"></i><span></span></div>
        <div class="form-actions">
          <button class="btn btn--primary" type="submit"><span class="btn-label">Send request</span><span class="btn-spinner" aria-hidden="true"></span><i class="ph ph-paper-plane-tilt" aria-hidden="true"></i></button>
          <p class="fine">We only use your details to respond to your message. See our <a class="link-arrow" href="legal.html#privacy">privacy policy</a>.</p>
        </div>
      </form>
      <div class="form-success" aria-live="polite">
        <span class="form-success-icon"><i class="ph ph-check" aria-hidden="true"></i></span>
        <div data-success-sent hidden>
          <h2>Thank you. We have your message.</h2>
          <p>A lawyer will review it and contact you, usually within one business day. If your situation becomes urgent in the meantime, call us on <a class="link-arrow" href="{tel()}">{FIRM['phone']}</a>.</p>
        </div>
        <div data-success-email hidden>
          <h2>One more step.</h2>
          <p>Your email app should now be open with your message ready to go. Press send, and a lawyer will review it and contact you, usually within one business day.</p>
          <p>If nothing opened, email us at <a class="link-arrow" href="mailto:{FIRM['email']}">{FIRM['email']}</a> or call <a class="link-arrow" href="{tel()}">{FIRM['phone']}</a>.</p>
        </div>
        <a class="btn btn--outline" href="index.html">Back to the home page</a>
      </div>
    </div>"""


# ---------------------------------------------------------------------------
# Hand-written pages (in _source/pages) with simple {{TOKENS}}
# ---------------------------------------------------------------------------
META_RE = re.compile(r"^\s*<!--meta\s*(\{.*?\})\s*-->", re.S)


def render_tokens(text):
    simple = {
        "PHONE": FIRM["phone"],
        "TEL": tel(),
        "EMAIL": FIRM["email"],
        "ADDRESS_1": FIRM["address_1"],
        "ADDRESS_2": FIRM["address_2"],
        "HOURS": FIRM["hours"],
        "HOURS_NOTE": FIRM["hours_note"],
        "FORM_ENDPOINT": FIRM["form_endpoint"],
        "TEAM_GRID": team_grid(),
        "AREA_OPTIONS": area_options(),
        "CONTACT_FORM": contact_form(),
        "CONTACT_FORM_COMPACT": contact_form(compact=True),
        "GUIDES_HOME": guides_home(),
        "HOURS_SHORT": FIRM["hours_short"],
    }

    # Tokens: {{PHONE}}, {{PHOTO|key|eager|sizes=...|class=...}}, {{ICON|name}},
    # {{CTA_BAND}} or {{CTA_BAND|Title|Text}}, {{BREADCRUMB|Label}}, {{FAQ|prefix}}
    def repl(m):
        parts = m.group(1).split("|")
        token, args = parts[0], parts[1:]
        if token in simple:
            return simple[token]
        if token == "PHOTO":
            key, kw = args[0], {}
            for p in args[1:]:
                if p == "eager":
                    kw["eager"] = True
                elif p.startswith("sizes="):
                    kw["sizes"] = p[6:]
                elif p.startswith("class="):
                    kw["cls"] = p[6:]
            if key in PHOTOS:
                return named_photo(key, **kw)
            pid, alt = AREA[key]["photo"]
            return photo(pid, alt, **kw)
        if token == "ICON":
            return icon(args[0], cls=args[1] if len(args) > 1 else "")
        if token == "CTA_BAND":
            return cta_band(*args) if args else cta_band()
        if token == "BREADCRUMB":
            return breadcrumbs((args[0], None))
        if token == "FAQ":
            return accordion(HOME_FAQS, args[0])
        raise KeyError(f"Unknown token {{{{{m.group(1)}}}}}")

    return re.sub(r"\{\{([^{}]+)\}\}", repl, text)


HOME_FAQS = [
    ("How do I get started?", "Call us or send a short message through our contact form. We'll arrange a confidential consultation to hear what happened and explain your options."),
    ("Is my consultation confidential?", "Yes. What you tell us when seeking legal advice is kept confidential, even if you decide not to hire us."),
    ("How much will my case cost?", "It depends on the matter. Some work, such as a demand letter, can often be done for a set fee. Litigation is usually billed differently. We'll explain the fee arrangement in writing before any work begins."),
    ("How quickly can you act?", "Urgent matters such as extortion threats and restraining orders are prioritized. Tell us when you get in touch if your situation is time-sensitive."),
    ("Do I have to go to court?", "Not always. Many matters resolve through a demand letter or negotiation. If court is needed, we'll prepare you and represent you throughout."),
    ("Do you only take large cases?", "No. We take matters of all sizes, and we'll be honest about whether the cost of pursuing a claim makes sense for you."),
]


# ---------------------------------------------------------------------------
# Typography clean-up and checks
# ---------------------------------------------------------------------------
def smarten(doc):
    """Curly apostrophes in visible text only (not in tags, scripts or styles)."""
    out, in_script = [], False
    for part in re.split(r"(<[^>]+>)", doc):
        if part.startswith("<"):
            low = part.lower()
            if low.startswith("<script") or low.startswith("<style"):
                in_script = True
            elif low.startswith("</script") or low.startswith("</style"):
                in_script = False
            out.append(part)
        elif in_script or part.startswith("<!--"):
            out.append(part)
        else:
            part = re.sub(r"(?<=\w)'(?=\w)", "’", part)
            part = re.sub(r"(?<=s)'(?=[\s.,])", "’", part)
            out.append(part)
    return "".join(out)


def assemble(meta, body):
    doc = head(meta) + "\n" + site_header(meta.get("nav", "")) + body + site_footer(meta.get("nav", ""))
    doc = smarten(doc)
    for bad in ("—", "–"):
        if bad in doc:
            raise ValueError(f"Dash character {bad!r} found in output for {meta['title']}")
    return doc


def main():
    pages = {}
    for src in sorted((HERE / "pages").glob("*.html")):
        text = src.read_text(encoding="utf-8")
        m = META_RE.match(text)
        if not m:
            raise ValueError(f"{src.name} is missing its <!--meta {{...}} --> header")
        meta = json.loads(m.group(1))
        pages[src.stem] = (meta, render_tokens(text[m.end():]))

    pages["practice-areas"] = practice_index()
    pages["attorneys"] = attorneys_page()
    for a in AREAS:
        pages[a["slug"]] = practice_page(a)
    pages["guides"] = guides_index()
    for g in GUIDES:
        pages[g["slug"]] = guide_page(g)

    for name, (meta, body) in pages.items():
        meta["_name"] = name
        (ROOT / f"{name}.html").write_text(assemble(meta, body), encoding="utf-8")
        print(f"  built {name}.html")

    order = ["index"] + sorted(n for n in pages if n not in ("index", "404"))
    urls = "\n".join(f"  <url><loc>{page_url(n)}</loc></url>" for n in order)
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "\n</urlset>\n",
        encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
    (ROOT / "CNAME").write_text(SITE_URL.split("//", 1)[1] + "\n", encoding="utf-8")
    print(f"Done: {len(pages)} pages.")


if __name__ == "__main__":
    main()
