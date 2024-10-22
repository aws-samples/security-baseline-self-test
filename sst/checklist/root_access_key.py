from lib import common
from lib import level_const as level
from datetime import datetime, timedelta, timezone
import logging

def get_last_used_days(date):
    if date in ("N/A", "no_information"):
        return timedelta.max
    return datetime.now(timezone.utc) - datetime.fromisoformat(date[:-6])

def format_last_used(last_used_days):
    if last_used_days == timedelta.max:
        return "N/A"
    if last_used_days.days == 0:
        return "Today"
    return f"{last_used_days.days} days before"

def check_access_key(root_credential_report, key_number):
    key_active = root_credential_report[getattr(common.CREDENTIAL_REPORT_COLS, f'ACCESS_KEY_{key_number}_ACTIVE').value].upper()
    key_last_used = root_credential_report[getattr(common.CREDENTIAL_REPORT_COLS, f'ACCESS_KEY_{key_number}_LAST_USED_DATE').value]
    
    if key_active == "TRUE":
        last_used_days = get_last_used_days(key_last_used)
        return f"AccessKey{key_number}", "In Use", format_last_used(last_used_days), True
    return f"AccessKey{key_number}", "Not In Use", "N/A", False

def check_root_accesskey_usage(session, translator, credential_report) -> common.CheckResult:
    logging.info(translator.translate("checking"))
    
    ret = common.CheckResult()
    ret.title = translator.translate("title")
    ret.result_cols = ['Access Key', 'Status', 'Last Used Date']

    if not credential_report:
        ret.level = level.error
        ret.msg = translator.translate("credential_report_error")
        ret.result_rows.append(['ERR', 'ERR', 'ERR'])
        return ret

    try:
        root_credential_report = common.get_root_credential_report(credential_report)
        
        key_in_use = False
        for key_number in [1, 2]:
            key, status, last_used, is_active = check_access_key(root_credential_report, key_number)
            ret.result_rows.append([key, status, last_used])
            key_in_use = key_in_use or is_active

        if key_in_use:
            ret.level = level.danger
            ret.msg = translator.translate("danger")
        else:
            ret.level = level.success
            ret.msg = translator.translate("success")

    except Exception as e:
        logging.error(f"Error processing root access key check: {str(e)}", exc_info=True)
        ret.level = level.error
        ret.msg = translator.translate("processing_error")
        ret.result_rows.append(['ERR', 'ERR', 'ERR'])
        ret.error_message = str(e)

    return ret