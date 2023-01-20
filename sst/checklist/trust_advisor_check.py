from lib import common
from lib import level_const as level

def check_trust_advisor_configuration() -> common.CheckResult:

    ret = common.CheckResult()

    ret.title = "Trusted Advisor 을 사용하도록 설정했는지 확인"
    ret.result_cols = []
    
    ret.level = level.info
    ret.msg = '''현재 계정의 Trusted Advisor 설정을&nbsp<a href="https://us-east-1.console.aws.amazon.com/trustedadvisor/home?region=ap-northeast-2#/preferences/manage-trusted-advisor" target="_blank" style="overflow:hidden;word-break:break-all;">확인</a>하세요.'''
    ret.result_rows.append([])

    return ret