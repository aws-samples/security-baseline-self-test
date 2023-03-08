from lib import common, language
from lib import level_const as level
from datetime import datetime, timedelta

def get_last_used_days(date) -> timedelta:
    if date == "N/A" or date=="no_information":
        return timedelta(9999)
    else :
        return datetime.utcnow() - datetime.fromisoformat(date[:-6])

def check_root_accesskey_usage(credential_report, selected_language) -> common.CheckResult:

    translator = language.translation("root_access_key", selected_language)

    print(translator.checking())

    ret = common.CheckResult()

    ret.title = translator.title()
    ret.result_cols = ['Access Key', 'Status', 'Last Used Date']

    if len(credential_report) == 0:
        ret.level = level.error
        ret.msg = "Failed to generate credential report"
        ret.result_rows.append(['ERR'])
        return ret

    root_credential_report = common.get_root_credential_report(credential_report)

    access_key_1_status = root_credential_report[common.CREDENTIAL_REPORT_COLS.ACCESS_KEY_1_ACTIVE.value].upper()
    access_key_2_status = root_credential_report[common.CREDENTIAL_REPORT_COLS.ACCESS_KEY_2_ACTIVE.value].upper()

    ret.level = level.success

    if access_key_1_status == "TRUE" :
        ret.level = level.danger
        last_used_days = get_last_used_days(root_credential_report[common.CREDENTIAL_REPORT_COLS.ACCESS_KEY_1_LAST_USED_DATE.value])
        if last_used_days < timedelta(9999):
            if last_used_days.days == 0:
                ret.result_rows.append(["AccessKey1", "In Use", "Today"])
            else:
                ret.result_rows.append(["AccessKey1", "In Use", "{days}days before".format(days=str(last_used_days.days))])
        else :
            ret.result_rows.append(["AccessKey1", "In Use", "N/A"])    
    else :
        ret.result_rows.append(["AccessKey1", "Not In Use", "N/A"])
        pass

    if access_key_2_status == "TRUE" :
        ret.level = level.danger
        last_used_days = get_last_used_days(root_credential_report[common.CREDENTIAL_REPORT_COLS.ACCESS_KEY_2_LAST_USED_DATE.value])
        if last_used_days < timedelta(9999):
            if last_used_days.days == 0:
                ret.result_rows.append(["AccessKey2", "In Use", "Today"])
            else:
                ret.result_rows.append(["AccessKey2", "In Use", "{days}days before".format(days=str(last_used_days.days))])
        else:
            ret.result_rows.append(["AccessKey2", "In Use", "N/A"])    
    else :
        ret.result_rows.append(["AccessKey2", "Not In Use", "N/A"])
        pass

    if ret.level == level.success:
        ret.msg = translator.success()
    else :
        ret.msg = translator.danger()

    return ret