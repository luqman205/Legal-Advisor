import re
from typing import Dict, List
from .utils import logger

class CategoryClassifier:
    def __init__(self):
        # High confidence keyword mappings grounded in real Pakistani legal terminology for the 8 target categories
        self.rules: Dict[str, List[str]] = {
            "Constitutional Laws": [
                "constitution", "constitutional", "article", "fundamental right", "supreme court", 
                "high court", "writ", "petition", "suo motu", "senate", "parliament", "national assembly", 
                "president", "prime minister", "fundamental rights", "habeas corpus", 
                "mandamus", "prohibition", "certiorari", "quo warranto", "legislation", "act of parliament",
                "amendment", "state of pakistan"
            ],
            "Family Laws": [
                "divorce", "khula", "talaq", "maintenance", "iddat", "dowry", "dower", "nikah", 
                "custody", "guardian", "marriage", "domestic violence", "court marriage", "spouse",
                "ward", "union council", "dower amount", "shariah", "dissolution of marriage", "bride",
                " bridal", "wife", "husband", "children", "minor", "visitation"
            ],
            "Property Laws": [
                "property", "possession", "illegal possession", "land", "dispute", "inheritance", 
                "registry", "patwari", "fard", "mutation", "transfer fee", "gift deed", "hiba", 
                "stamp paper", "encroachment", "title deed", "wirasat", "intiqal", "qabza", "mafia",
                "dispossess", "dispossession", "sub-registrar", "mortgage", "charge", "lease", "tenancy",
                "actionable claim", "compulsory registration", "benami", "stamp duty", "easement",
                "prescription", "partition", "co-ownership", "adverse possession", "squatter",
                "illegal dispossession act", "transfer of property act",
                "landlord", "tenant", "evict", "eviction", "rent", "rented", "house", "lease agreement",
                "malik makan", "kirayedar", "kiraya", "makan", "ghar se nikal"
            ],
            "Criminal Laws": [
                "fir", "police", "arrest", "false fir", "bail", "thana", "sho", "complaint", 
                "refusal", "remand", "custodial", "crpc", "cognizable", "pre-arrest bail", 
                "post-arrest bail", "section 22", "theft", "mischief", "murder", "assault", "conspiracy",
                "forgery", "penal code", "ppc", "criminal", "stolen", "perpetrator",
                "302", "489-f", "497", "498", "cnsa", "peca", "self-defense", "private defense", 
                "kidnapping", "abduction", "defamation", "ransom", "fraud", "trust", "trespass", 
                "narcotics", "harassment", "drugs", "rape", "cheating", "cyber"
            ],
            "Consumer Protection Laws": [
                "consumer", "refund", "faulty", "fake product", "damaged item", "warranty", 
                "consumer court", "online store scam", "expiry date", "defective goods", 
                "unfair trade", "misleading advertisement", "receipt", "deficient service", "replacement",
                "defective", "substandard", "negligence", "invoice", "overcharging", "notice", "frivolous"
            ],
            "Labour Laws": [
                "salary", "employer", "termination", "contract", "wrongful termination", 
                "overtime", "gratuity", "pension", "provident fund", "labor court", "wages", 
                "resignation", "severance", "employment agreement", "notice period", "workplace",
                "employee", "worker", "maternity", "social security", "pessi", "sessi", "eobi",
                "working hours", "weekly holiday", "paid leave", "sick leave", "workplace safety",
                "occupational health", "workmen compensation", "child labor", "trade union", "cba"
            ],
            "Tax Laws": [
                "tax", "income tax", "sales tax", "fbr", "tax return", "tax assessment", 
                "default surcharge", "filing return", "audit", "tax tribunal", "withholding",
                "invoice", "taxpayer", "revenue board", "inland revenue",
                "wht", "surcharge", "atl", "customs", "excise", "provincial", "cgt",
                "filer", "non-filer", "adrc", "pra", "srb", "kpra", "bra"
            ],
            "Civil Laws": [
                "civil", "specific relief", "specific performance", "injunction", "stay order", 
                "declaratory", "declaration", "specific performance of contract", "indemnity",
                "arbitration", "contract act", "void contract", "voidable contract", "void agreement",
                "guarantee", "surety", "principal debtor", "bailment", "pledge", "agency", "principal and agent",
                "cancellation of deed", "rectification of contract", "civil court", "pecuniary jurisdiction",
                "territorial jurisdiction", "plaint", "written statement", "summons", "execution of decree",
                "civil appeal", "revision petition", "review petition", "limitation period", "limitation act",
                "cpc", "civil procedure"
            ]
        }

    def classify(self, text: str) -> str:
        """
        Classifies the text into one of the 8 legal categories using key phrase intensity.
        Defaults to 'Constitutional Laws' or 'Civil Laws' if ambiguous.
        """
        text_lower = text.lower()
        scores = {category: 0 for category in self.rules.keys()}
        
        for category, keywords in self.rules.items():
            for kw in keywords:
                # Compile regex to match keywords as whole words or phrases
                pattern = r'\b' + re.escape(kw) + r'\b'
                matches = re.findall(pattern, text_lower)
                if matches:
                    scores[category] += len(matches) + 1

        # Get category with highest score
        max_score = max(scores.values())
        if max_score > 0:
            best_categories = [cat for cat, score in scores.items() if score == max_score]
            logger.info(f"Classified query category: {best_categories[0]} with score {max_score}")
            return best_categories[0]
        
        # Fallback keyword checks
        if any(w in text_lower for w in ["constitution", "article", "parliament", "writ"]):
            return "Constitutional Laws"
        if any(w in text_lower for w in ["divorce", "khula", "wife", "husband", "children", "custody"]):
            return "Family Laws"
        if any(w in text_lower for w in ["salary", "job", "employer", "termination", "gratuity"]):
            return "Labour Laws"
        if any(w in text_lower for w in ["land", "house", "plot", "possession", "registry"]):
            return "Property Laws"
        if any(w in text_lower for w in ["tax", "fbr", "audit"]):
            return "Tax Laws"
        if any(w in text_lower for w in ["fir", "police", "arrest", "bail", "ppc", "crpc"]):
            return "Criminal Laws"
        if any(w in text_lower for w in ["consumer", "refund", "defective", "store"]):
            return "Consumer Protection Laws"
            
        return "Constitutional Laws" # Safe default
