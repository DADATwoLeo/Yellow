#!/usr/bin/env python3
"""多Agent隐私合规审计系统（修复完整版）"""
import json
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.scanner_agent import ScannerAgent
from agents.analyzer_agent import AnalyzerAgent
from agents.auditor_agent import AuditorAgent

def load_sample_code(filepath="data/sample_code.py"):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return '''
import logging
def process(user_data):
    email = "test@example.com"
    phone = "13812345678"
    print(f"用户信息: {email}, {phone}")
    logging.info(f"身份证: 110101199001011234")
    masked_phone = phone[:3] + "****" + phone[7:]
    print(masked_phone)
'''

def print_sep(title=""):
    print("\n" + "="*60)
    if title:
        print(f"  {title}")
        print("="*60)

def main():
    print_sep("🔍 隐私合规代码审计系统（修复版）")
    code = load_sample_code()
    scanner = ScannerAgent()
    scan_r = scanner.scan(code)

    analyzer = AnalyzerAgent()
    analyze_r = analyzer.analyze(scan_r, code)

    auditor = AuditorAgent()
    report = auditor.audit(scan_r, analyze_r)

    print_sep("📋 最终审计报告")
    print(json.dumps(report, ensure_ascii=False, indent=2))

    print_sep("📊 审计结果")
    print(f"风险评分: {report['risk_assessment']['score']}/100")
    print(f"风险等级: {report['risk_assessment']['level']}")
    print(f"合规状态: {report['compliance_status']}")
    print("\n修复建议:")
    for i, r in enumerate(report["recommendations"], 1):
        print(f"{i}. {r}")
    print_sep("✅ 审计完成")
    input("\n按回车键退出...")

if __name__ == "__main__":
    main()
