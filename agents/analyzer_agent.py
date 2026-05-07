from tools.rag_retriever import PrivacyLawRetriever
from tools.llm_client import LLMClient
from typing import Dict, Any

class AnalyzerAgent:
    def __init__(self):
        self.name = "AnalyzerAgent"
        self.retriever = PrivacyLawRetriever()
        self.llm = LLMClient()

    def analyze(self, scanner_result: Dict[str, Any], code: str) -> Dict[str, Any]:
        flags = scanner_result.get("risk_flags", [])
        results = []
        for flag in flags:
            laws = self.retriever.retrieve(flag["description"])
            llm_res = self._check(flag, laws)
            results.append({
                "risk_id": flag["id"],
                "synthesized_judgment": llm_res
            })
        violations = len([r for r in results if r["synthesized_judgment"]["is_violation"]])
        return {
            "agent": self.name,
            "analysis_results": results,
            "summary": {"total_risks": len(flags), "confirmed_violations": violations}
        }

    def _check(self, flag, laws):
        sys_p = """你是隐私合规专家，仅返回JSON：{"is_violation":true/false,"reasoning":"","confidence":0.8}"""
        user_p = f"代码:{flag['code_snippet']} 描述:{flag['description']}"
        res = self.llm.chat(sys_p, user_p)
        return self.llm.safe_parse_json(res)
