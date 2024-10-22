from lib import common
from lib import level_const as level
import botocore.exceptions
import logging

def check_alternate_contact_filling(session, translator) -> common.CheckResult:
    logging.info(translator.translate("checking"))
    
    ret = common.CheckResult()
    ret.title = translator.translate("title")
    ret.result_cols = ['Contact Type', 'Name', 'E-Mail', 'Contacts']
    
    contact_type_list = ['BILLING', 'SECURITY', 'OPERATIONS']
    client = session.client('account')
    ret.level = level.success

    for contact_type in contact_type_list:
        try:
            contact = client.get_alternate_contact(AlternateContactType=contact_type)["AlternateContact"]
        except client.exceptions.ResourceNotFoundException:
            ret.level = level.warning
            contact = {"Name": "-", "EmailAddress": "-", "PhoneNumber": "-"}
        except client.exceptions.ValidationException as e:
            ret.level = level.error
            contact = {"Name": "ERR", "EmailAddress": "ERR", "PhoneNumber": "ERR"}
            ret.error_message = f"Validation Exception: {str(e)}"
            logging.error(ret.error_message, exc_info=True)
        except client.exceptions.AccessDeniedException as e:
            ret.level = level.error
            contact = {"Name": "ERR", "EmailAddress": "ERR", "PhoneNumber": "ERR"}
            ret.error_message = f"Access Denied: {str(e)}"
            logging.error(ret.error_message, exc_info=True)
        except client.exceptions.TooManyRequestsException:
            ret.level = level.error
            contact = {"Name": "ERR", "EmailAddress": "ERR", "PhoneNumber": "ERR"}
            ret.error_message = "Too Many Request Exception. Please Try Again Later."
            logging.error(ret.error_message, exc_info=True)
        except client.exceptions.InternalServerException:
            ret.level = level.error
            contact = {"Name": "ERR", "EmailAddress": "ERR", "PhoneNumber": "ERR"}
            ret.error_message = "Internal Server Exception"
            logging.error(ret.error_message, exc_info=True)
        except botocore.exceptions.ClientError as e:
            ret.level = level.error
            contact = {"Name": "ERR", "EmailAddress": "ERR", "PhoneNumber": "ERR"}
            ret.error_message = f"Unexpected ClientError: {str(e)}"
            logging.error(ret.error_message, exc_info=True)
        except Exception as e:
            ret.level = level.error
            contact = {"Name": "ERR", "EmailAddress": "ERR", "PhoneNumber": "ERR"}
            ret.error_message = f"Unexpected Exception: {str(e)}"
            logging.error(ret.error_message, exc_info=True)
        finally:
            ret.result_rows.append([contact_type, contact["Name"], contact["EmailAddress"], contact["PhoneNumber"]])

    if ret.level == level.success:
        ret.msg = translator.translate("success")
    elif ret.level == level.warning:
        ret.msg = translator.translate("warning")
    else:
        ret.msg = translator.translate("error")

    return ret