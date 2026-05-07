from tools.code_parser import CodeParser
from typing import Dict, Any

class ScannerAgent:
    def __init__(self):
        self.name = "ScannerAgent"

    def scan(self, code: str) -> Dict[str, Any]:
        parser = CodeParser(code)
        pii_vars = parser.get_pii_variables()
        flows = parser.get_data_flows()
        return {
            "agent": self.name,
            "findings": {"pii_variables": pii_vars, "data_flows": flows},
            "risk_flags": self._gen_flags(flows),
            "confidence": 0.95 if flows else 0.9
        }

    def _gen_flags(self, flows):
        flags = []
        for f in flows:
            flags.append({
                "id": f"RISK-{f['line']}-{f['variable']}",
                "type": "DATA_LEAK",
                "severity": f["severity"],
                "variable": f["variable"],
                "sink": f["sink"],
                "line": f["line"],
                "code_snippet": f["code"],
                "description": f"PII变量{f['variable']}流向危险出口{f['sink']}"
            })
        return flags
