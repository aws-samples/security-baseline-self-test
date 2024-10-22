from lib import common
from lib import level_const as level
import logging

def check_trust_advisor_configuration(translator) -> common.CheckResult:
    logging.info(translator.translate("checking"))
    
    ret = common.CheckResult()
    ret.title = translator.translate("title")
    ret.result_cols = []
    
    try:
        ret.level = level.info
        ret.msg = translator.translate("info")
        ret.result_rows.append([])
    except Exception as e:
        logging.error(f"Error in Trust Advisor check: {str(e)}", exc_info=True)
        ret.level = level.error
        ret.msg = translator.translate("error")
        ret.error_message = str(e)
    
    return ret