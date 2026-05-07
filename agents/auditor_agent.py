from tools.llm_client import LLMClient
from typing import Dict, Any

class AuditorAgent:
    def __init__(self):
        self.name = "AuditorAgent"
        self.llm = LLMClient()

    def audit(self, scanner_r, analyzer_r):
        conflicts = self._detect_conflicts(scanner_r, analyzer_r)
        assessment = self._assess(scanner_r, analyzer_r, conflicts)
        return self._gen_report(scanner_r, analyzer_r, conflicts, assessment)

    def _detect_conflicts(self, s, a):
        conflicts = []
        s_flags = s.get("risk_flags", [])
        a_list = a.get("analysis_results", [])
        for f in s_flags:
            match = next((x for x in a_list if x["risk_id"] == f["id"]), None)
            if not match: continue
            s_is_high = f["severity"] == "HIGH"
            a_is_ok = not match["synthesized_judgment"]["is_violation"]
            if s_is_high and a_is_ok:
                conflicts.append({"conflict_id": f"CONFLICT-{f['id']}"})
        return conflicts

    def _assess(self, s, a, conflicts):
        risk_count = len(s.get("risk_flags", []))
        vio_count = a.get("summary", {}).get("confirmed_violations", 0)
        score = min(risk_count * 25 + vio_count * 30 + len(conflicts)*10, 100)
        if score >= 70: level = "CRITICAL"
        elif score >= 40: level = "HIGH"
        elif score >= 20: level = "MEDIUM"
        else: level = "LOW"
        return {"risk_score": score, "risk_level": level}

    def _gen_report(self, s, a, conflicts, assess):
        recs = []
        for f in s.get("risk_flags", []):
            recs.append(f"行{f['line']}：{f['variable']}输出到{f['sink']}需脱敏")
        return {
            "report_id": "AUDIT-FIXED-001",
            "risk_assessment": assess,
            "compliance_status": "PASS" if assess["risk_level"] == "LOW" else "FAIL",
            "recommendations": recs if recs else ["代码合规"]
        }
