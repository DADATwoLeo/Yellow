import re
import ast
from typing import List, Dict, Any
from config import PII_PATTERNS, DANGEROUS_SINKS

class CodeParser:
    def __init__(self, code: str):
        self.code = code
        self.tree = None
        self.var_map = {}
        self.data_flows = []
        self.var_chain = {}
        try:
            self.tree = ast.parse(code)
            self._build_var_table()
            self._build_chain()
            self._trace_flow()
        except:
            pass

    def _src(self, node):
        try: return ast.get_source_segment(self.code, node) or ""
        except: return ""

    def _build_var_table(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Assign):
                src = self._src(node)
                for t in node.targets:
                    if isinstance(t, ast.Name):
                        self._detect(t.id, node.lineno, src)
            if isinstance(node, ast.FunctionDef):
                for arg in node.args.args:
                    self._detect(arg.arg, node.lineno, f"param:{arg.arg}")

    def _detect(self, name, line, src):
        types = []
        for t, p in PII_PATTERNS.items():
            if re.search(p, src):
                types.append(t)
        self.var_map[name] = {"line": line, "pii_types": types, "is_pii": len(types) > 0}

    def _build_chain(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Assign) and isinstance(node.value, ast.Name):
                src_var = node.value.id
                for t in node.targets:
                    if isinstance(t, ast.Name):
                        self.var_chain[t.id] = src_var

    def _trace_flow(self):
        for node in ast.walk(self.tree):
            if not isinstance(node, ast.Call): continue
            fname = self._fname(node.func)
            if not any(s in fname for s in DANGEROUS_SINKS): continue
            for arg in node.args + [kw.value for kw in node.keywords]:
                var = self._var(arg)
                if not var: continue
                real = self._follow(var)
                if real in self.var_map and self.var_map[real]["is_pii"]:
                    info = self.var_map[real]
                    self.data_flows.append({
                        "variable": var, "pii_categories": info["pii_types"],
                        "sink": fname, "line": node.lineno, "code": self._src(node),
                        "severity": "HIGH"
                    })

    def _fname(self, n):
        if isinstance(n, ast.Name): return n.id
        if isinstance(n, ast.Attribute):
            p = self._fname(n.value) if hasattr(n, "value") else ""
            return f"{p}.{n.attr}" if p else n.attr
        return ""

    def _var(self, a):
        if isinstance(a, ast.Name): return a.id
        return None

    def _follow(self, v):
        while v in self.var_chain:
            v = self.var_chain[v]
        return v

    def get_pii_variables(self):
        return [{"name": n, **i} for n, i in self.var_map.items() if i["is_pii"]]
    def get_data_flows(self): return self.data_flows
