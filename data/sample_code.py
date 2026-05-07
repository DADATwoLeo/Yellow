import logging
def process(user_data):
    email = "test@example.com"
    phone = "13812345678"
    print(f"用户信息: {email}, {phone}")
    logging.info(f"身份证: 110101199001011234")
    # 脱敏示例
    masked_phone = phone[:3] + "****" + phone[7:]
    print(masked_phone)
