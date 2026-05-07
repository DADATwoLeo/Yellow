import json
import re
from config import LLM_CONFIG

class LLMClient:
    def __init__(self):
        self.api_key = LLM_CONFIG.get("api_key")
        self.client = None
        if self.api_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key, base_url=LLM_CONFIG["base_url"])
            except:
                self.client = None

    def chat(self, sys_prompt, user_prompt, temperature=0.1):
        if self.client:
            try:
                r = self.client.chat.completions.create(
                    model=LLM_CONFIG["model"], temperature=temperature,
                    messages=[{"role":"system","content":sys_prompt},{"role":"user","content":user_prompt}]
                )
                return r.choices[0].message.content
            except:
                return self._simulate(user_prompt)
        return self._simulate(user_prompt)

    def _simulate(self, prompt):
        has_pii = any(w in prompt.lower() for w in ["phone","email","id_card","身份证"])
        has_log = any(w in prompt.lower() for w in ["print","log"])
        has_mask = any(w in prompt.lower() for w in ["mask","脱敏","****"])
        if has_mask:
            return '{"is_violation":false,"reasoning":"已脱敏","confidence":0.92}'
        if has_pii and has_log:
            return '{"is_violation":true,"reasoning":"明文PII泄露到日志/打印","confidence":0.95}'
        return '{"is_violation":false,"reasoning":"无明显泄露","confidence":0.8}'

    def safe_parse_json(self, s):
        try: return json.loads(s)
        except:
            m = re.search(r'\{.*\}', s, re.DOTALL)
            if m:
                try: return json.loads(m.group())
                except: pass
        return {"is_violation": True, "reasoning": "解析失败", "confidence": 0.5}
