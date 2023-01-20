from lib import common
from lib import level_const as level
from datetime import datetime, timedelta

def get_last_used_days(date) -> timedelta:
    if date == "N/A" or date=="no_information":
        return timedelta(9999)
    else :
        return datetime.utcnow() - datetime.fromisoformat(date[:-6])

def check_root_accesskey_usage(credential_report) -> common.CheckResult:

    ret = common.CheckResult()

    ret.title = "루트 계정의 AccessKey 생성 여부 확인"
    ret.result_cols = ['Access Key', 'Status', 'Last Used Date']

    if len(credential_report) == 0:
        ret.level = level.error
        ret.msg = "Credential Report 생성이 실패했습니다."
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
                ret.result_rows.append(["AccessKey1", "사용 중", "오늘"])
            else:
                ret.result_rows.append(["AccessKey1", "사용 중", "{days}일 전".format(days=str(last_used_days.days))])
        else :
            ret.result_rows.append(["AccessKey1", "사용 중", "N/A"])    
    else :
        ret.result_rows.append(["AccessKey1", "사용 안 함", "N/A"])
        pass

    if access_key_2_status == "TRUE" :
        ret.level = level.danger
        last_used_days = get_last_used_days(root_credential_report[common.CREDENTIAL_REPORT_COLS.ACCESS_KEY_2_LAST_USED_DATE.value])
        if last_used_days < timedelta(9999):
            if last_used_days.days == 0:
                ret.result_rows.append(["AccessKey2", "사용 중", "오늘"])
            else:
                ret.result_rows.append(["AccessKey2", "사용 중", "{days}일 전".format(days=str(last_used_days.days))])
        else:
            ret.result_rows.append(["AccessKey2", "사용 중", "N/A"])    
    else :
        ret.result_rows.append(["AccessKey2", "사용 안 함", "N/A"])
        pass

    if ret.level == level.success:
        ret.msg = "루트계정에서 사용중인 Access Key가 없습니다."
    else :
        ret.msg = '''루트계정에서 Access Key 를 사용중입니다. 루트 계정의 Access Key 는 사용하지 않는 것이 보다 안전합니다.&nbsp(<a href="https://docs.aws.amazon.com/ko_kr/IAM/latest/UserGuide/id_root-user.html#id_root-user_manage_delete-key" target="_blank" style="overflow:hidden;word-break:break-all;">Access Key 삭제방법</a>)'''

    return ret