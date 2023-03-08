from lib import common, language
from lib import level_const as level
import botocore.exceptions
import logging, traceback

def check_alternate_contact_filling(session, selected_language) -> common.CheckResult:

    translator = language.translation("alternate_contacts", selected_language)

    print(translator.checking())

    ret = common.CheckResult()

    ret.title = translator.title()
    ret.result_cols = ['Contact Type', 'Name', 'E-Mail', 'Contacts']
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
            ret.msg = "Validation Exception({error})".format(error=str(e))
        except client.exceptions.AccessDeniedException as e:
            logging.error(traceback.format_exc())
            ret.level = level.error
            contact = {
                "Name" : "ERR",
                "EmailAddress" : "ERR",
                "PhoneNumber" : "ERR"
            }
            ret.msg = "Access Denied({error})".format(error=str(e))
        except client.exceptions.TooManyRequestsException:
            logging.error(traceback.format_exc())
            ret.level = level.error
            contact = {
                "Name" : "ERR",
                "EmailAddress" : "ERR",
                "PhoneNumber" : "ERR"
            }
            ret.msg = "Too Many Request Exception. Please Try Again Later."
        except client.exceptions.InternalServerException:
            logging.error(traceback.format_exc())
            ret.level = level.error
            contact = {
                "Name" : "ERR",
                "EmailAddress" : "ERR",
                "PhoneNumber" : "ERR"
            }
            ret.msg = "Internal Server Exception"
        except botocore.exceptions.ClientError:
            logging.error(traceback.format_exc())
            ret.level = level.error
            ret.msg = "Unexpected Exception"
            contact = {
                "Name" : "ERR",
                "EmailAddress" : "ERR",
                "PhoneNumber" : "ERR"
            }
        finally:
            ret.result_rows.append([contact_type, contact["Name"], contact["EmailAddress"], contact["PhoneNumber"]])

    if ret.level == level.success:
        ret.msg = translator.success()
    elif ret.level == level.warning:
        ret.msg = translator.warning()
    else :
        ret.msg = ""

    return ret
