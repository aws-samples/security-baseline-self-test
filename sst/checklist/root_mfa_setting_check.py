from lib import common, language
from lib import level_const as level

def check_root_mfa_setting(credential_report, selected_language) -> common.CheckResult:

    translator = language.translation("root_mfa", selected_language)
    
    print(translator.checking())

    ret = common.CheckResult()

    ret.title = translator.title()
    ret.result_cols = ['MFA Setting']

    if len(credential_report) == 0:
        ret.level = level.error
        ret.msg = "Failed to generate credential report."
        ret.result_rows.append(['ERR'])
        return ret

    root_credential_report = common.get_root_credential_report(credential_report)

    mfa_status = root_credential_report[common.CREDENTIAL_REPORT_COLS.MFA_ACTIVE.value].upper()

    if mfa_status == "TRUE":
        ret.level = level.success
        ret.msg = translator.success()
    else :
        ret.level = level.danger  
        ret.msg = translator.danger()
    
    ret.result_rows.append([mfa_status])

    return ret
