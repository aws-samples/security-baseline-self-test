from lib import common
from lib import level_const as level
import botocore.exceptions
import logging, traceback

def check_alternate_contact_filling(session) -> common.CheckResult:

    ret = common.CheckResult()

    ret.title = "대체 연락처 등록여부 확인"
    ret.result_cols = ['계정 타입', '이름', '이메일', '전화번호']
    contact_type_list = ['BILLING', 'SECURITY', 'OPERATIONS']

    client = session.client('account')
    
    ret.level = level.success

    for contact_type in contact_type_list:

        try:
            contact = client.get_alternate_contact(AlternateContactType=contact_type)["AlternateContact"]
        except client.exceptions.ResourceNotFoundException as e:
            ret.level = level.warning
            contact = {
                "Name" : "-",
                "EmailAddress" : "-",
                "PhoneNumber" : "-"
            }
        except client.exceptions.ValidationException as e:
            logging.error(traceback.format_exc())
            ret.level = level.error
            contact = {
                "Name" : "ERR",
                "EmailAddress" : "ERR",
                "PhoneNumber" : "ERR"
            }
            ret.msg = "유효성 검증에 실패했습니다.({error})".format(error=str(e))
        except client.exceptions.AccessDeniedException as e:
            logging.error(traceback.format_exc())
            ret.level = level.error
            contact = {
                "Name" : "ERR",
                "EmailAddress" : "ERR",
                "PhoneNumber" : "ERR"
            }
            ret.msg = "권한이 없습니다.({error})".format(error=str(e))
        except client.exceptions.TooManyRequestsException:
            logging.error(traceback.format_exc())
            ret.level = level.error
            contact = {
                "Name" : "ERR",
                "EmailAddress" : "ERR",
                "PhoneNumber" : "ERR"
            }
            ret.msg = "너무 많은 요청입니다. 잠시후 다시 시도해주세요."
        except client.exceptions.InternalServerException:
            logging.error(traceback.format_exc())
            ret.level = level.error
            contact = {
                "Name" : "ERR",
                "EmailAddress" : "ERR",
                "PhoneNumber" : "ERR"
            }
            ret.msg = "예기치 못한 서버에러가 발생했습니다."
        except botocore.exceptions.ClientError:
            logging.error(traceback.format_exc())
            ret.level = level.error
            ret.msg = "예기치 못한 에러가 발생했습니다."
            contact = {
                "Name" : "ERR",
                "EmailAddress" : "ERR",
                "PhoneNumber" : "ERR"
            }
        finally:
            ret.result_rows.append([contact_type, contact["Name"], contact["EmailAddress"], contact["PhoneNumber"]])

    if ret.level == level.success:
        ret.msg = "모든 대체 연락처 정보가 등록되어 있습니다. 정확한 정보인지 확인해주세요."
    elif ret.level == level.warning:
        ret.msg = "등록되지 않은 대체 연락처 정보가 있습니다. 대체 연락처 정보를 등록해주세요."
    else :
        pass

    return ret
