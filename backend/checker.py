import cloudscraper
import wikipediaapi
import ollama
import re
from collections import Counter

MODEL_REASONING = "llama3.1"
MODEL_FACTCHECK = "mistral"

scraper = cloudscraper.create_scraper()

wiki = wikipediaapi.Wikipedia(
    language="fr",
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent="FactCheckerBot/1.0"
)

STOPWORDS = {
    "le", "la", "les", "un", "une", "des", "est", "sont", "ne", "pas",
    "que", "qui", "dans", "sur", "avec", "pour", "par", "ce", "cela"
}

CAUSAL_WORDS = [
    "car", "parce que", "en raison", "provoque", "résulte", "cause"
]

def extract_concepts(claim):
    words = re.findall(r"\b[a-zA-Zéèêàçùîôû]+\b", claim.lower())
    return list({w for w in words if w not in STOPWORDS and len(w) > 3})[:5]

def relevance_score(text, concepts):
    counter = Counter(text.lower().split())
    score = sum(counter[c] for c in concepts)
    causal_bonus = sum(1 for w in CAUSAL_WORDS if w in text.lower())
    return score + causal_bonus * 2

def final_verdict(original, concepts, context):
    prompt = f"""
CONTEXTE :
{context}

Explique le mécanisme réel lié aux concepts : {', '.join(concepts)}
Puis indique si l'affirmation est vraie, fausse ou incertaine.

AFFIRMATION : "{original}"
"""
    res = ollama.chat(
        model=MODEL_REASONING,
        messages=[{"role": "user", "content": prompt}]
    )
    return res["message"]["content"]

def expected_result_fact_check(claim):
    prompt = f"""
AFFIRMATION :
"{claim}"

Réponds UNIQUEMENT :
RESULTAT_ATTENDU: VRAI
RESULTAT_ATTENDU: FAUX
RESULTAT_ATTENDU: INCERTAIN
"""
    res = ollama.chat(
        model=MODEL_FACTCHECK,
        messages=[{"role": "user", "content": prompt}]
    )
    return res["message"]["content"]

def check_claim(claim):
    concepts = extract_concepts(claim)

    texts = []
    sources = []

    for c in concepts:
        page = wiki.page(c)
        if page.exists():
            texts.append(page.text[:5000])
            sources.append(page.title)

    valid = [t for t in texts if relevance_score(t, concepts) >= 2]

    if not valid:
        return {
            "error": "Informations insuffisantes",
            "concepts": concepts
        }

    context = "\n\n".join(valid)

    return {
        "concepts": concepts,
        "analysis": final_verdict(claim, concepts, context),
        "expected": expected_result_fact_check(claim),
        "sources": sources
    }
