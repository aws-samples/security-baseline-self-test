from lib import common
from lib import level_const as level
import logging

def check_root_mfa_setting(session, translator, credential_report) -> common.CheckResult:
    logging.info(translator.translate("checking"))
    
    ret = common.CheckResult()
    ret.title = translator.translate("title")
    ret.result_cols = ['MFA Setting']

    if not credential_report:
        ret.level = level.error
        ret.msg = translator.translate("credential_report_error")
        ret.result_rows.append(['ERR'])
        return ret

    try:
        root_credential_report = common.get_root_credential_report(credential_report)
        mfa_status = root_credential_report[common.CREDENTIAL_REPORT_COLS.MFA_ACTIVE.value].upper()
    except Exception as e:
        logging.error(f"Error processing root credential report: {str(e)}", exc_info=True)
        ret.level = level.error
        ret.msg = translator.translate("processing_error")
        ret.result_rows.append(['ERR'])
        ret.error_message = str(e)
        return ret

    if mfa_status == "TRUE":
        ret.level = level.success
        ret.msg = translator.translate("success")
    else:
        ret.level = level.danger
        ret.msg = translator.translate("danger")

    ret.result_rows.append([mfa_status])
    return ret