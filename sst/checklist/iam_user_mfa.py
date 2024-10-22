from lib import common
from lib import level_const as level
import logging

def check_iam_user_mfa_setting(session, translator, credential_report) -> common.CheckResult:
    logging.info(translator.translate("checking"))
    
    ret = common.CheckResult()
    ret.title = translator.translate("title")
    ret.result_cols = ['IAM User', 'MFA Enabled']

    if not credential_report:
        ret.level = level.error
        ret.msg = translator.translate("credential_report_error")
        ret.result_rows.append(['ERR', 'ERR'])
        return ret

    user_info_list = common.get_iam_credential_report(credential_report)

    if not user_info_list:
        ret.level = level.warning
        ret.msg = translator.translate("no_iam_user")
        return ret

    ret.level = level.success
    ret.msg = translator.translate("success")

    for user_info in user_info_list:
        user_name = user_info[common.CREDENTIAL_REPORT_COLS.USER.value]
        mfa_status = user_info[common.CREDENTIAL_REPORT_COLS.MFA_ACTIVE.value].upper()
        ret.result_rows.append([user_name, mfa_status])

        if mfa_status == "FALSE":
            ret.level = level.danger
            ret.msg = translator.translate("danger")

    return ret