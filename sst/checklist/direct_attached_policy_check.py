from lib import common
from lib import level_const as level
import botocore.exceptions
import logging, traceback

def check_iam_direct_attached_policy(session) -> common.CheckResult:
    client = session.client('iam')

    ret = common.CheckResult()

    ret.title = "IAM 사용자에게 직접 연결된 정책 확인"
    ret.result_cols = ["IAM 사용자", "직접 연결된 관리형 정책", "인라인 정책"]

    try:
        user_list = client.list_users()["Users"]
    except client.exceptions.NoSuchEntityException:
        ret.level = level.warning
        ret.msg = "IAM 사용자가 없습니다."
        ret.result_rows.append(["-", "-", "-"])
        return ret
    except client.exceptions.ServiceFailureException:
        logging.error(traceback.format_exc())
        ret.level = level.error
        ret.msg = "서비스 실패."
        ret.result_rows.append(["ERR", "ERR", "ERR"])
        return ret
    except botocore.exceptions.ClientError as e:
        logging.error(traceback.format_exc())
        ret.level = level.error
        ret.msg = "예기치 못한 에러가 발생했습니다."
        ret.result_rows.append(["ERR", "ERR", "ERR"])
        return ret
    
    if len(user_list) == 0:
        ret.level = level.warning
        ret.msg = "IAM 사용자가 없습니다."
    else:
        ret.level = level.success
        ret.msg = "직접 연결된 정책없이 모든 IAM 사용자의 정책이 효율적으로 관리되고 있습니다."

        for user in user_list:
            user_name = user["UserName"]
            
            nums_direct_attached_policies = None
            nums_inline_policies = None
            
            try:
                nums_direct_attached_policies = str(len(client.list_attached_user_policies(UserName=user_name)["AttachedPolicies"]))
            except botocore.exceptions.ClientError:
                logging.error(traceback.format_exc())
                ret.level = level.error
                ret.msg = "예기치 못한 에러가 발생했습니다."
                nums_direct_attached_policies = "ERR"

            try:
                nums_inline_policies = str(len(client.list_user_policies(UserName=user_name)["PolicyNames"]))
            except botocore.exceptions.ClientError:
                logging.error(traceback.format_exc())
                ret.level = level.error
                ret.msg = "예기치 못한 에러가 발생했습니다."
                nums_inline_policies = "ERR"

            if ret.level == level.error:
                continue
            else:
                ret.result_rows.append([user_name, nums_direct_attached_policies, nums_inline_policies])
            
                if nums_direct_attached_policies > "0" or nums_inline_policies > "0":
                    ret.level = level.warning
                    ret.msg = "IAM 사용자에게 직접 연결된 정책이 존재합니다."
                else:
                    pass

    return ret
