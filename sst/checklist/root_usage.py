from lib import common
from lib import level_const as level
from datetime import datetime, timedelta, timezone
import logging

ROOT_ACCESS_DAYS_STANDARD = 7

def get_root_access_days(date):
    if date in ("N/A", "no_information"):
        return timedelta.max
    return datetime.now(timezone.utc) - datetime.fromisoformat(date[:-6])

def get_message(last_used_timedelta):
    if last_used_timedelta == timedelta.max:
        return "No history"
    if last_used_timedelta.days == 0:
        return "Today"
    return f"{last_used_timedelta.days} days before"

def check_root_usage(session, translator, credential_report) -> common.CheckResult:
    logging.info(translator.translate("checking"))
    
    ret = common.CheckResult()
    ret.title = translator.translate("title")
    ret.result_cols = ['Credential Type', 'Last Access Date']

    if not credential_report:
        ret.level = level.error
        ret.msg = translator.translate("credential_report_error")
        ret.result_rows.append(['ERR', 'ERR'])
        return ret

    try:
        root_credential_report = common.get_root_credential_report(credential_report)
        password_last_used = get_root_access_days(root_credential_report[common.CREDENTIAL_REPORT_COLS.PASSWORD_LAST_USED.value])
        access_key1_last_used = get_root_access_days(root_credential_report[common.CREDENTIAL_REPORT_COLS.ACCESS_KEY_1_LAST_USED_DATE.value])
        access_key2_last_used = get_root_access_days(root_credential_report[common.CREDENTIAL_REPORT_COLS.ACCESS_KEY_2_LAST_USED_DATE.value])
        
        last_access_days = min(password_last_used, access_key1_last_used, access_key2_last_used)

        if last_access_days > timedelta(ROOT_ACCESS_DAYS_STANDARD):
            ret.level = level.success
            ret.msg = translator.translate("success").format(ROOT_ACCESS_DAYS_STANDARD)
        elif last_access_days.days == 0:
            ret.level = level.danger
            ret.msg = translator.translate("access_today")
        else:
            ret.level = level.danger
            ret.msg = translator.translate("danger").format(last_access_days.days)

        ret.result_rows.extend([
            ["PASSWORD", get_message(password_last_used)],
            ["ACCESS KEY1", get_message(access_key1_last_used)],
            ["ACCESS KEY2", get_message(access_key2_last_used)]
        ])

    except Exception as e:
        logging.error(f"Error processing root usage check: {str(e)}", exc_info=True)
        ret.level = level.error
        ret.msg = translator.translate("processing_error")
        ret.result_rows.append(['ERR', 'ERR'])
        ret.error_message = str(e)

    return ret