from lib import common
from lib import level_const as level

def check_iam_user_mfa_setting(credential_report) -> common.CheckResult:

    ret = common.CheckResult()

    ret.title = "IAM 사용자 MFA 설정 여부 확인"
    ret.result_cols = ['사용자', 'MFA 설정']

    if len(credential_report) == 0:
        ret.level = level.error
        ret.msg = "Credential Report 생성이 실패했습니다."
        ret.result_rows.append(['ERR'])
        return ret

    user_info_list = common.get_iam_credential_report(credential_report)

    if len(user_info_list) == 0:
        ret.level = level.warning
        ret.msg = "IAM 사용자가 없습니다. 루트계정이 아닌 IAM Role 과 같은 다른 자격증명을 사용하는 경우, 경고를 무시하셔도 좋습니다."
    else :
        ret.level = level.success
        ret.msg = "모든 IAM 사용자가 MFA 를 사용중입니다."

        for user_info in user_info_list:
            user_name = user_info[common.CREDENTIAL_REPORT_COLS.USER.value]
            mfa_status = user_info[common.CREDENTIAL_REPORT_COLS.MFA_ACTIVE.value].upper()

            if mfa_status == "FALSE":
                ret.level = level.danger
                ret.msg = "MFA를 설정하지 않은 IAM 사용자가 있습니다."
            else :
                pass

            ret.result_rows.append([user_name, mfa_status])

    return ret
