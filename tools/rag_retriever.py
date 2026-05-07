from config import PRIVACY_LAWS

class PrivacyLawRetriever:
    def __init__(self):
        self.laws = PRIVACY_LAWS
    def retrieve(self, query, top_k=3):
        res = []
        q = query.lower()
        for lid, txt in self.laws.items():
            score = 0
            if any(w in q for w in ["log","print","输出"]): score +=1
            if any(w in q for w in ["id_card","phone","email"]): score +=1
            if score>0:
                res.append({"law_id":lid,"content":txt,"relevance_score":score})
        return sorted(res, key=lambda x:x["relevance_score"], reverse=True)[:top_k]
