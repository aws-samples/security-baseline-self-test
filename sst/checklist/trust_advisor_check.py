from lib import common, language
from lib import level_const as level

def check_trust_advisor_configuration(selected_language) -> common.CheckResult:

    translator = language.translation("trusted_advisor", selected_language)

    print(translator.checking())

    ret = common.CheckResult()

    ret.title = translator.title()
    ret.result_cols = []
    
    ret.level = level.info
    ret.msg = translator.info()
    ret.result_rows.append([])

    return ret