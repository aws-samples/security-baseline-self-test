from lib import common, language
from lib import level_const as level
from datetime import datetime, timedelta

def get_root_access_days(date) -> timedelta:
    if date == "N/A" or date=="no_information":
        return timedelta(9999)
    else :
        return datetime.utcnow() - datetime.fromisoformat(date[:-6])

def get_message(last_used_timedelta) -> str:
    if last_used_timedelta < timedelta(9999):
        if last_used_timedelta.days == 0:
            return "Today"
        else:
            return "{last_used_timedelta} days before".format(last_used_timedelta=str(last_used_timedelta.days))
    else:
        return "No history"

def check_root_usage(credential_report, selected_language) -> common.CheckResult:

    translator = language.translation("root_usage_check", selected_language)

    print(translator.checking())
    ret = common.CheckResult()

    ret.title = translator.title()
    ret.result_cols = ['Credential Type','Last Access Date']

    if len(credential_report) == 0:
        ret.level = level.error
        ret.msg = "Failed to generate credential report"
        ret.result_rows.append(['ERR'])
        return ret

    root_credential_report = common.get_root_credential_report(credential_report)

    password_last_used_days = get_root_access_days(root_credential_report[common.CREDENTIAL_REPORT_COLS.PASSWORD_LAST_USED.value])
    access_key1_last_used_days = get_root_access_days(root_credential_report[common.CREDENTIAL_REPORT_COLS.ACCESS_KEY_1_LAST_USED_DATE.value])
    access_key2_last_used_days = get_root_access_days(root_credential_report[common.CREDENTIAL_REPORT_COLS.ACCESS_KEY_2_LAST_USED_DATE.value])

    last_access_days = min(password_last_used_days, access_key1_last_used_days, access_key2_last_used_days)

    ROOT_ACCESS_DAYS_STANDARD = 7

    if last_access_days > timedelta(ROOT_ACCESS_DAYS_STANDARD):
        ret.level = level.success
        ret.msg = translator.success(ROOT_ACCESS_DAYS_STANDARD)
    else :
        ret.level = level.danger
        if last_access_days.days == 0:
            ret.msg = translator.access_today()
        else:
            ret.msg = translator.danger(last_access_days.days)

    ret.result_rows.append(["PASSWORD", get_message(password_last_used_days)])
    ret.result_rows.append(["ACCESS KEY1", get_message(access_key1_last_used_days)])
    ret.result_rows.append(["ACCESS KEY2", get_message(access_key2_last_used_days)])

    return ret