from __future__ import annotations

import json
import re
from typing import Dict, List


# ─────────────────────────────────────────────
#  FAQ KNOWLEDGE BASE
# ─────────────────────────────────────────────

FAQ_ITEMS: List[Dict[str, str]] = [
    # Rank & Eligibility
    {
        "question": "What is a cutoff rank?",
        "answer": (
            "A cutoff rank is the last rank that got a seat in a particular college, "
            "branch, category and gender in a given counselling year. For example, if the cutoff "
            "for CSE in a college is 12,000 for BC_B Boys, it means the last admitted student in that "
            "category had rank 12,000. You should target a rank better than the cutoff to have a good chance."
        ),
    },
    {
        "question": "What rank do I need for OC category in Telangana POLYCET or EAMCET?",
        "answer": (
            "For OC category in Telangana, government colleges and top JNTU-affiliated colleges usually close "
            "at ranks within the top 5,000–25,000 depending on the branch and year. Popular branches like CSE and "
            "ECE in Hyderabad often need much better ranks than colleges in smaller districts. Always compare your "
            "rank with the previous year cutoffs for your exact branch, college type and district."
        ),
    },
    {
        "question": "What rank do I need for BC_A, BC_B, BC_C, BC_D, BC_E categories?",
        "answer": (
            "BC_A to BC_E categories usually get slightly relaxed cutoffs compared to OC, but the difference depends "
            "on the branch and college. In many Telangana and AP engineering colleges, BC_B and BC_D cutoffs are very "
            "close to OC for high-demand branches like CSE. Always check category-wise cutoff ranks, not just the OC "
            "cutoff, when planning your choices."
        ),
    },
    {
        "question": "What rank is needed for SC and ST categories?",
        "answer": (
            "SC and ST categories generally have more relaxed cutoffs, so students with ranks even beyond 40,000–80,000 "
            "can get government or good private colleges depending on the branch. However, for super popular branches "
            "like CSE in top Hyderabad colleges, even SC/ST cutoffs can be within the first 30,000 ranks. Use your "
            "category-wise cutoffs to plan safe, target and dream options."
        ),
    },
    {
        "question": "How is rank calculated in Telangana POLYCET and EAMCET?",
        "answer": (
            "In Telangana POLYCET and EAMCET, your rank is calculated based on your normalized exam marks, not just "
            "raw scores. The authorities rank all qualified students and assign a unique rank from best to worst after "
            "considering tie-breaking rules. This rank, along with your category, gender and local/non-local status, "
            "is used during counselling to decide which seats you are eligible for."
        ),
    },
    {
        "question": "What is eligibility for Telangana POLYCET and EAMCET?",
        "answer": (
            "For POLYCET (Diploma), you generally need to have passed SSC/10th with at least 35% marks in maths and "
            "science, and you should meet the age and domicile conditions specified by SBTET. For EAMCET (Engineering), "
            "you must have passed or appeared for Intermediate (10+2) with MPC group or equivalent. Always read the "
            "official notification for the exact year-wise eligibility rules."
        ),
    },
    # Categories
    {
        "question": "What are OC, BC_A, BC_B, BC_C, BC_D, BC_E, SC, ST and EWS categories?",
        "answer": (
            "These are reservation categories used in Telangana and AP admissions. OC means Open Category (no reservation), "
            "BC_A to BC_E are different Backward Class groups, SC is Scheduled Caste, ST is Scheduled Tribe and EWS is "
            "Economically Weaker Section among OC. Your category decides your reserved cutoff ranks and eligibility for "
            "scholarships and fee reimbursement."
        ),
    },
    {
        "question": "How do I know my reservation category for admissions?",
        "answer": (
            "Your category is mentioned on your community or caste certificate issued by the state government, and sometimes "
            "also on your school records. For EWS, you need a valid EWS certificate issued for the current financial year. "
            "Always upload and carry the latest original certificates to counselling to avoid losing reservation benefits."
        ),
    },
    {
        "question": "What is OC or Open Category in admissions?",
        "answer": (
            "OC (Open Category) generally refers to students who do not claim any caste-based reservation. OC seats can be "
            "filled by any student purely based on merit, so cutoffs for these seats are usually the highest. If you belong "
            "to a reserved category, you can still compete for OC seats if your rank is strong enough."
        ),
    },
    {
        "question": "What is BC_A category?",
        "answer": (
            "BC_A is one of the Backward Class reservation groups in Telangana and Andhra Pradesh. Different castes are "
            "listed under BC_A as per the state government notification, and students must have a valid BC-A caste certificate "
            "to claim this quota. BC_A students get reserved seats and are eligible for scholarships and fee reimbursement "
            "if they also meet income criteria."
        ),
    },
    {
        "question": "What is EWS category in Telangana and AP admissions?",
        "answer": (
            "EWS (Economically Weaker Section) is a reservation for economically weaker students from the general/OC category, "
            "usually for families with an annual income below a limit such as ₹8 lakh. EWS seats are separate from BC/SC/ST "
            "quotas and have their own cutoffs. You must produce a valid EWS certificate for the current year to use this benefit."
        ),
    },
    # Fee Structure
    {
        "question": "What is the average fee for diploma colleges?",
        "answer": (
            "For diploma (polytechnic) colleges in Telangana and AP, government colleges usually charge around ₹5,000–₹15,000 "
            "per year, while private colleges may charge between ₹25,000 and ₹50,000 per year. Actual amounts vary by branch "
            "and college type. If you are eligible, state fee reimbursement schemes can significantly reduce what you pay."
        ),
    },
    {
        "question": "What is the average fee for engineering colleges?",
        "answer": (
            "In Telangana and AP, government and university colleges often charge around ₹15,000–₹35,000 per year for B.Tech, "
            "while private colleges typically range from ₹60,000 to ₹1,50,000 per year. Top-tier private institutes or autonomous "
            "colleges may charge more, especially for high-demand branches like CSE. Always check the latest fee structure on "
            "the official college or counselling website before locking your options."
        ),
    },
    {
        "question": "What is the average fee for medical colleges through NEET?",
        "answer": (
            "Government medical colleges in Telangana and AP usually have annual MBBS fees around ₹15,000–₹60,000, which is "
            "highly subsidised. Private medical colleges can charge anywhere between ₹8–15 lakh per year under the convenor quota, "
            "and even more under management or NRI quotas. Because fees are high, always check bond conditions and total 5-year "
            "cost before choosing a college."
        ),
    },
    {
        "question": "Are there fee reimbursement schemes available?",
        "answer": (
            "Yes, both Telangana and AP offer fee reimbursement schemes for eligible BC, SC, ST and economically weaker students. "
            "Schemes like Jagananna Vidya Deevena in AP or state post-matric scholarships in Telangana can cover a large part of "
            "your tuition fee in approved colleges. You must link your Aadhaar, bank account and income certificate and apply "
            "through the official scholarship portals on time."
        ),
    },
    {
        "question": "What is the NRI quota fee?",
        "answer": (
            "NRI quota or management quota seats in engineering and medical colleges charge much higher fees compared to convenor "
            "quota. For engineering, NRI quota may cost ₹2–5 lakh per year, while in medical it can go beyond ₹20–25 lakh per year "
            "depending on the college. Choose this route only after carefully evaluating whether the total cost fits your family's "
            "budget and long-term plans."
        ),
    },
    # Branches
    {
        "question": "Which branches have the best placements?",
        "answer": (
            "In most engineering colleges, CSE, IT, ECE and newer CS-related specialisations usually have the strongest placement "
            "numbers, especially in urban JNTU-affiliated colleges. Mechanical, Civil and EEE can also offer good careers but may "
            "require additional skills, exams or higher studies. Always look at the actual placement report of the specific college "
            "instead of assuming based only on branch name."
        ),
    },
    {
        "question": "What is the difference between CSE and IT branches?",
        "answer": (
            "CSE (Computer Science and Engineering) covers core computing concepts like algorithms, operating systems, networks and "
            "theory, while IT (Information Technology) focuses more on software systems, databases and practical applications. In many "
            "colleges in Telangana and AP, the syllabus and placements for CSE and IT are very similar. For most software jobs, both "
            "branches are treated almost equally by recruiters."
        ),
    },
    {
        "question": "What is the difference between ECE and EEE?",
        "answer": (
            "ECE (Electronics and Communication Engineering) deals with communication systems, embedded systems, VLSI and electronics, "
            "while EEE (Electrical and Electronics Engineering) focuses more on power systems, machines and electrical networks along "
            "with some electronics. ECE graduates often move into IT, telecom or chip design roles, whereas EEE graduates may work "
            "with power utilities, core electrical companies or public sector units. Choose based on whether you enjoy communication "
            "electronics or heavy electrical engineering more."
        ),
    },
    {
        "question": "Which branch should I choose based on my rank?",
        "answer": (
            "If your rank is very strong, you can prioritise high-demand branches like CSE, IT, ECE in top colleges and metro "
            "locations. With a mid-range rank, consider good colleges in slightly less demanded branches like EEE or Mechanical, "
            "or strong CSE branches in tier-2 districts. Always balance your interest, long-term career goals, college quality and "
            "fee instead of chasing only the most popular branch."
        ),
    },
    {
        "question": "Is Mechanical or Civil engineering a good choice?",
        "answer": (
            "Mechanical and Civil are core engineering branches that can lead to stable careers in manufacturing, infrastructure, "
            "construction and public sector roles. However, campus placements for these branches may be weaker in some private "
            "colleges compared to CSE or IT. If you are genuinely interested in core engineering and ready to prepare for GATE or "
            "government exams, they can still be very good options."
        ),
    },
    # Admission Process
    {
        "question": "What is POLYCET?",
        "answer": (
            "POLYCET is the Polytechnic Common Entrance Test conducted by Telangana and AP for admission into diploma engineering "
            "and non-engineering courses. Your POLYCET rank is used to allot seats in government, aided and private polytechnic "
            "colleges through web counselling. Keep an eye on the official SBTET website for application dates, hall tickets and "
            "counselling schedules."
        ),
    },
    {
        "question": "What is EAMCET?",
        "answer": (
            "EAMCET is the common entrance test conducted by Telangana (TS EAMCET) and Andhra Pradesh (AP EAPCET) for admission into "
            "engineering, agriculture and pharmacy programmes. Your rank in EAMCET, along with category and local status, decides "
            "your eligibility for B.Tech seats in JNTU-affiliated and private colleges. Always follow the official TS EAMCET or "
            "AP EAPCET portals for updated notifications and counselling instructions."
        ),
    },
    {
        "question": "What is NEET?",
        "answer": (
            "NEET (National Eligibility cum Entrance Test) is the national exam for admission to MBBS, BDS and other medical "
            "programmes across India. Your NEET score and All India Rank are used for both All India Quota and state quota counselling "
            "in Telangana and AP. Because competition is very high, even a small difference in marks can change your college options, "
            "so analyse last year's NEET cutoffs carefully."
        ),
    },
    {
        "question": "What documents are needed for counselling and admission?",
        "answer": (
            "Typically you need your hall ticket, rank card, SSC and Intermediate marks memos, transfer certificate, caste "
            "certificate, income certificate, Aadhaar card, study certificates and passport-size photos. For scholarships and "
            "fee reimbursement, bank account details and ration card or white card may also be required. Always follow the official "
            "counselling notification checklist and carry both originals and multiple photocopies."
        ),
    },
    {
        "question": "What are the important dates in the admission process?",
        "answer": (
            "Important stages include notification release, application form dates, hall ticket download, exam date, result "
            "announcement, certificate verification, option entry, seat allotment and reporting to college. For TS and AP, these "
            "events usually happen between April and September, but exact dates change every year. Bookmark the official counselling "
            "website and check it weekly during the season."
        ),
    },
    # College Types
    {
        "question": "What is the difference between government, private and aided colleges?",
        "answer": (
            "Government colleges are fully run and funded by the state, with low fees and high demand for seats. Aided colleges are "
            "private institutions that receive partial government support and often have moderate fees. Pure private colleges are "
            "self-financed, so fees can be higher but seat availability is larger; always compare faculty quality, labs and placement "
            "records across all three types."
        ),
    },
    {
        "question": "What does JNTU affiliation mean for a college?",
        "answer": (
            "If a college is JNTU-affiliated, it follows the curriculum, exam pattern and regulations set by Jawaharlal Nehru "
            "Technological University (Hyderabad, Kakinada or Anantapur). This usually ensures a standard syllabus and recognised "
            "degree for engineering programmes. When comparing colleges, check whether they are JNTU-affiliated or autonomous and "
            "look at their NAAC/NBA accreditations as well."
        ),
    },
    # Districts & Location
    {
        "question": "Which districts in Telangana and AP have more engineering colleges?",
        "answer": (
            "In Telangana, Hyderabad, Rangareddy, Medchal and nearby districts have the highest concentration of engineering colleges. "
            "In Andhra Pradesh, districts like Krishna, Guntur, Visakhapatnam and Chittoor host many institutes. Studying in such hubs "
            "can give better exposure and internships, but competition and living costs may also be higher."
        ),
    },
    {
        "question": "Is it better to study near home or in another city?",
        "answer": (
            "Studying near home can reduce hostel and travel costs and give better family support, which is helpful if your budget is "
            "tight. However, moving to a bigger city like Hyderabad or Vizag can provide stronger placements, internships and peer "
            "networks. A good balance is to prioritise college quality first and then choose the nearest strong option that fits your "
            "family's comfort level."
        ),
    },
    # Scholarships
    {
        "question": "What scholarships are available for SC and ST students?",
        "answer": (
            "SC and ST students in Telangana and AP can usually apply for post-matric scholarships and full or partial fee "
            "reimbursement in approved colleges. These schemes cover tuition and sometimes maintenance allowances if income and "
            "attendance conditions are met. Visit your state's ePASS or scholarship portal, register with Aadhaar and make sure your "
            "college is recognised under the scheme."
        ),
    },
    {
        "question": "What is Jagananna Vidya Deevena?",
        "answer": (
            "Jagananna Vidya Deevena is an AP government scheme that reimburses 100% tuition fees for eligible SC, ST, BC, minority "
            "and economically weaker OC students in approved colleges. The amount is directly credited to the mother's bank account "
            "in instalments each year. To benefit, you must ensure your college is in the approved list and keep your academic "
            "performance and attendance strong."
        ),
    },
    {
        "question": "What is a post-matric scholarship?",
        "answer": (
            "Post-matric scholarships are financial aid schemes for students studying after 10th class, including intermediate, "
            "diploma, degree and professional courses. They usually cover tuition fees, exam fees and sometimes a small stipend for "
            "maintenance. Apply online through your state's scholarship portal, submit your documents through the college and track "
            "your application status regularly."
        ),
    },
    # Score & Matching
    {
        "question": "How does College Compass score and rank colleges?",
        "answer": (
            "College Compass combines your rank, category, gender, branch preference, district choice and budget to filter out "
            "eligible colleges based on past cutoffs. It then uses a scoring logic that rewards better closing ranks, lower fees and "
            "closer locations to highlight stronger options for you. The Dream, Target and Safe tags help you quickly understand the "
            "risk level of each option instead of reading raw numbers alone."
        ),
    },
    {
        "question": "What do Dream, Target and Safe colleges mean?",
        "answer": (
            "Dream colleges are slightly above your typical cutoff range and may need some luck or a better option entry strategy. "
            "Target colleges are well-matched to your rank and profile where you have a solid chance of getting a seat. Safe colleges "
            "are options where your rank is comfortably better than the cutoff, giving a high probability of admission and peace of "
            "mind in later counselling rounds."
        ),
    },
    {
        "question": "How should I use the scores given by College Compass?",
        "answer": (
            "Use the scores as a guidance signal, not as the only decision factor. Higher scores usually indicate better alignment "
            "with your rank, budget and preferences, but you should still read about the college's placements, faculty and location. "
            "Create a mix of high-score dream options plus balanced target and safe choices across multiple districts."
        ),
    },
    # General Tips
    {
        "question": "How many counselling rounds are there for EAMCET and POLYCET?",
        "answer": (
            "Typically there are at least one main phase and one or two additional counselling rounds such as second phase or spot "
            "admissions. The exact number of rounds depends on how many seats remain vacant after each phase. Even if your first "
            "allotment is not ideal, later rounds can open up better options, so keep tracking official announcements."
        ),
    },
    {
        "question": "What happens if I miss the counselling schedule?",
        "answer": (
            "If you miss key steps like certificate verification or option entry in the main round, you may lose the chance to "
            "participate in that phase. Some later rounds or spot admissions might still be available, but your choices and seat "
            "types may become limited. Always mark counselling dates on your calendar and keep SMS and email alerts switched on."
        ),
    },
    {
        "question": "Can I change my branch after admission?",
        "answer": (
            "Branch change is sometimes allowed within the same college after the first year, based on your CGPA and seat "
            "availability in the requested branch. Policies differ by university and college, and competition for CSE or IT seats "
            "through branch change is usually very high. It's safer to join a branch you are comfortable with rather than fully "
            "depending on a future branch-change chance."
        ),
    },
    {
        "question": "Can I change my college in later rounds?",
        "answer": (
            "Yes, in most counselling systems you can revise your options in later rounds and may get a better college if your rank "
            "permits. However, once you physically report and submit original certificates to a college, you must follow the official "
            "rules to participate in further rounds or transfers. Read the 'sliding' and 'upgradation' rules on the counselling "
            "website before deciding."
        ),
    },
]


SUGGESTED_QUESTIONS: List[str] = [
    "What is a cutoff rank?",
    "Which branch has the best placements?",
    "How does College Compass score and rank colleges?",
    "What documents are needed for counselling and admission?",
    "What is BC_A category?",
    "Are there fee reimbursement schemes available?",
]


_GREETING_KEYWORDS = {"hi", "hello", "hey", "namaste", "hola"}
_THANKS_KEYWORDS = {"thank", "thanks", "thankyou", "thank you", "thx"}


def _tokenize(text: str) -> List[str]:
    """Lowercase and split into basic word tokens."""
    return re.findall(r"\w+", text.lower())


def _is_greeting(message: str) -> bool:
    tokens = _tokenize(message)
    return any(tok in _GREETING_KEYWORDS for tok in tokens)


def _is_thanks(message: str) -> bool:
    lower = message.lower()
    if any(phrase in lower for phrase in ("thank you", "thanks a lot")):
        return True
    tokens = _tokenize(message)
    return any(tok in _THANKS_KEYWORDS for tok in tokens)


def _best_faq_match(message: str) -> str | None:
    """Return the best matching FAQ answer or None if no good match."""
    user_tokens = set(_tokenize(message))
    if not user_tokens:
        return None

    best_score = 0.0
    best_answer: str | None = None

    for item in FAQ_ITEMS:
        q_tokens = set(_tokenize(item["question"]))
        # Use simple keyword overlap
        overlap = user_tokens.intersection(q_tokens)
        if not overlap:
            continue
        score = len(overlap) / max(len(user_tokens), 1)
        if score > best_score:
            best_score = score
            best_answer = item["answer"]

    # Threshold tuned to avoid random matches
    if best_score >= 0.2 and best_answer:
        return best_answer
    return None


def get_faq_response(user_message: str) -> str:
    """
    Lightweight FAQ engine:
    - Handles greetings and thanks.
    - Uses keyword overlap against FAQ questions.
    - Runs fully offline with pure Python.
    """
    text = user_message.strip()
    if not text:
        return "I did not catch that. Could you please type your question again in a simple sentence?"

    if _is_greeting(text):
        return (
            "Hello! 👋 I’m Compass AI, your admission guide for Telangana/AP diploma, engineering and medical programmes. "
            "Ask me about ranks, category cutoffs, fees, branches, counselling rounds or scholarships, and I’ll try to "
            "answer using our built‑in FAQ knowledge."
        )

    if _is_thanks(text):
        return (
            "You’re most welcome! If you have more doubts about ranks, cutoffs, fees or counselling steps, just ask another "
            "question any time. All the best for your admissions journey! 🎓"
        )

    match = _best_faq_match(text)
    if match:
        return match

    return (
        "I’m not fully sure about that specific question based on my FAQ data. "
        "Try asking about ranks, cutoffs, categories, fees, branches, counselling rounds, districts or scholarships in Telangana/AP, "
        "or rephrase your doubt in a simpler way."
    )


def export_faq_as_json() -> str:
    """Optional helper to inspect the FAQ as JSON."""
    return json.dumps(FAQ_ITEMS, ensure_ascii=False, indent=2)

