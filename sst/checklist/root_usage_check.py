from lib import common
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
            return "오늘"
        else:
            return "{last_used_timedelta} 일 전".format(last_used_timedelta=str(last_used_timedelta.days))
    else:
        return "사용 이력이 없습니다."

def check_root_usage(credential_report) -> common.CheckResult:

    ret = common.CheckResult()

    ret.title = "루트 계정 Access 확인"
    ret.result_cols = ['자격증명 유형','최근접속일']

    if len(credential_report) == 0:
        ret.level = level.error
        ret.msg = "Credential Report 생성이 실패했습니다."
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
        ret.msg = "최근 {standard_root_access_date} 이내에 루트 계정 사용이력이 없습니다.".format(standard_root_access_date=str(ROOT_ACCESS_DAYS_STANDARD))
    else :
        ret.level = level.danger
        if last_access_days.days == 0:
            ret.msg = "오늘 날짜의 루트 계정 사용이력이 존재합니다. 다른 자격증명으로 AWS 서비스를 이용해주세요."
        else:
            ret.msg = "최근 {last_access_days} 이내에 루트 계정 사용이력이 존재합니다. 다른 자격증명으로 AWS 서비스를 이용해주세요.".format(last_access_days=str(last_access_days.days))

    ret.result_rows.append(["PASSWORD", get_message(password_last_used_days)])
    ret.result_rows.append(["ACCESS KEY1", get_message(access_key1_last_used_days)])
    ret.result_rows.append(["ACCESS KEY2", get_message(access_key2_last_used_days)])

    return ret