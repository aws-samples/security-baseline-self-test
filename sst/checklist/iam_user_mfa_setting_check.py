from lib import common, language
from lib import level_const as level

def check_iam_user_mfa_setting(credential_report, selected_language) -> common.CheckResult:

    translator = language.translation("iam_user_mfa",selected_language)

    print(translator.checking())

    ret = common.CheckResult()

    ret.title = translator.title()
    ret.result_cols = ['IAM User', 'MFA Enabled']

    if len(credential_report) == 0:
        ret.level = level.error
        ret.msg = "Failed to generate credential report"
        ret.result_rows.append(['ERR'])
        return ret

    user_info_list = common.get_iam_credential_report(credential_report)

    if len(user_info_list) == 0:
        ret.level = level.warning
        ret.msg = translator.no_iam_user()
    else :
        ret.level = level.success
        ret.msg = translator.success()

        for user_info in user_info_list:
            user_name = user_info[common.CREDENTIAL_REPORT_COLS.USER.value]
            mfa_status = user_info[common.CREDENTIAL_REPORT_COLS.MFA_ACTIVE.value].upper()

            if mfa_status == "FALSE":
                ret.level = level.danger
                ret.msg = translator.danger()
            else :
                pass

            ret.result_rows.append([user_name, mfa_status])

    return ret
