from lib import common
from lib import level_const as level

def check_root_mfa_setting(credential_report) -> common.CheckResult:

    ret = common.CheckResult()

    ret.title = "루트 계정 MFA 설정 여부 확인"
    ret.result_cols = ['MFA 설정']

    if len(credential_report) == 0:
        ret.level = level.error
        ret.msg = "Credential Report 생성이 실패했습니다."
        ret.result_rows.append(['ERR'])
        return ret

    root_credential_report = common.get_root_credential_report(credential_report)

    mfa_status = root_credential_report[common.CREDENTIAL_REPORT_COLS.MFA_ACTIVE.value].upper()

    if mfa_status == "TRUE":
        ret.level = level.success
        ret.msg = "루트 계정에 MFA가 설정되어 있습니다."
    else :
        ret.level = level.danger  
        ret.msg = '''루트 계정에 설정된 MFA가 없습니다.&nbsp<a href="https://docs.aws.amazon.com/ko_kr/IAM/latest/UserGuide/id_credentials_mfa_enable_virtual.html" target="_blank" style="overflow:hidden;word-break:break-all;">링크</a>를 눌러 설정방법을 확인해주세요.'''
    
    ret.result_rows.append([mfa_status])

    return ret
