import os

LLM_CONFIG = {
    "provider": "deepseek",
    "api_key": os.getenv("DEEPSEEK_API_KEY"),
    "model": "deepseek-chat",
    "base_url": "https://api.deepseek.com/v1"
}

PII_PATTERNS = {
    "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
    "phone_cn": r'\b1[3-9]\d{9}\b',
    "id_card_cn": r'\b(\d{17}[\dXx]|\d{15})\b',
    "credit_card": r'\b(?:\d{4}[- ]?){3}\d{4}\b',
    "ip_address": r'\b((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)\b'
}

DANGEROUS_SINKS = [
    "print", "log.info", "log.debug", "log.warning", "log.error",
    "logging.info", "logging.debug", "logging.warning", "logging.error",
    "logger.info", "logger.debug", "logger.warning", "logger.error",
    "write", "send_email", "send_sms", "http_post", "file.write",
    "requests.post", "requests.get", "open"
]

PRIVACY_LAWS = {
    "GDPR-Art.32": "数据控制者必须实施安全措施，包括假名化与加密。",
    "GDPR-Art.5.1.c": "数据最小化原则。",
    "PIPL-Art.51": "防止个人信息泄露、篡改、丢失。",
    "PIPL-Art.6": "处理个人信息应采取影响最小方式。",
    "CCPA-1798.150": "企业需合理保护个人信息。"
}
