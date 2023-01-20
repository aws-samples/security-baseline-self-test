from lib import common
from lib import level_const as level
import botocore.exceptions
import logging, traceback

def check_iam_password_policy(session) -> common.CheckResult:
    client = session.client('iam')

    ret = common.CheckResult()

    ret.title = "IAM 비밀번호 정책 확인"
    ret.result_cols = ["비밀번호 정책 설정"]

    try:
        client.get_account_password_policy()
    except client.exceptions.NoSuchEntityException:
        ret.level = level.warning
        ret.msg = "IAM 비밀번호 정책이 설정되어 있지 않습니다. 루트계정이 아닌 IAM Role 과 같은 다른 자격증명을 사용하는 경우, 경고를 무시하셔도 좋습니다."
        ret.result_rows.append(["미설정"])
        return ret
    except client.exceptions.ServiceFailureException:
        logging.error(traceback.format_exc())
        ret.level = level.error
        ret.msg = "서비스 실패. 잠시 후 다시 시도해주세요."
        ret.result_rows.append(["ERR"])
        return ret
    except botocore.exceptions.ClientError:
        logging.error(traceback.format_exc())
        ret.level = level.error
        ret.msg = "예기치 못한 에러가 발생했습니다."
        ret.result_rows.append(["ERR"])
        return ret
    else:
        ret.level = level.success
        ret.msg = "IAM 비밀번호 정책이 설정되어 있습니다."

    return ret
