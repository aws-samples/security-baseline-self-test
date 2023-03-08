from enum import Enum

class LANGUAGE_CODE(Enum):
    ENGLISH = "ENG"
    KOREAN = "KOR"

def translation(module_name, language):
    if module_name == "main":
        return MainLan(language=language)
    elif module_name == "account_level_bucket_public_access":
        return AccountLevelBucketPUblicAccess(language=language)
    elif module_name == "alternate_contacts":
        return AlternateContact(language=language)
    elif module_name == "bucket_public_access":
        return BucketPublicAccess(language=language)
    elif module_name == "cloudwatch_alarm_configuation":
        return CloudWatchAlarmConfiguration(language=language)
    elif module_name == "direct_attached_policy":
        return IAMDirectedAttachedPolicy(language=language)
    elif module_name == "guardduty_enabled":
        return GuardDutyEnabled(language=language)
    elif module_name == "iam_password_policy":
        return IAMPasswordPolicy(language=language)
    elif module_name == "iam_user_mfa":
        return IAMUserMFASetting(language=language)
    elif module_name == "multi_region_instance_usage":
        return MultiRegionInstanceUsage(language=language)
    elif module_name == "multi_region_trail":
        return MultiRegionTrail(language=language)
    elif module_name == "root_mfa":
        return RootMFASetting(language=language)
    elif module_name == "root_usage_check":
        return RootUsage(language=language)
    elif module_name == "root_access_key":
        return RootAccessKey(language=language)
    elif module_name == "trail_enabled":
        return TrailEnabled(language=language)
    elif module_name == "trusted_advisor":
        return TrustedAdvisor(language=language)

class MainLan():
    def __init__(self, language):
        self.language = language

    def invalid_iam_entity(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "This IAM Entity is not supported. Please use IAM user profile."
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "지원하지 않는 IAM Entity입니다. IAM 사용자 Profile을 사용해 주세요."    

    def start_test(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return ">>> Execute the Test"
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return ">>> 점검을 시작합니다"

    def generate_result_report(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "\n >>> Report Generating..."
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "\n >>> 결과 리포트 생성 중..."

    def request_credential_report(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return ">> Getting Credential Report"
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return ">> Credential Report를 가져오는 중"

class AccountLevelBucketPUblicAccess():
    def __init__(self, language):
        self.language = language
    
    def checking(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return ">>> Checking Account-Level S3 Bucket Public Access"
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return ">>> 계정 수준의 S3 Bucket Public Access 확인 중"

    def title(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "Account-Level S3 Bucket Public Access Settings"
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "계정 수준 S3 Bucket Public Access 설정"

    def no_such_public_access_block_config(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "No Such Public Access Block Configuration"
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "계정의 기본 S3 Bucket Public Access Block 정책이 설정되어 있지 않습니다."

    def success(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "Account-Level S3 Bucket Public Access is All Blocked"
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "계정의 기본 S3 Bucket Public Access 정책이 모두 차단되어 있습니다."
    
    def warning(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "Some Account-Level S3 Bucket Public Access are Allowed."
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "계정의 기본 S3 Bucket Public Access 정책이 일부 허용되어 있습니다."

    def danger(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "Account-Level S3 Bucket Public Access are all Allowed."
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "계정의 기본 S3 Bucket Public Access 정책이 모두 허용되어 있습니다."

class AlternateContact():
    def __init__(self, language):
        self.language = language

    def checking(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return ">>> Checking Alternate Contacts"
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return ">>> 대체 연락처 등록을 확인하는 중"

    def title(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "Alternate Contacts are Registered"
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "대체 연락처 등록 확인"
    
    def success(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "All types of alternate contacts have been registered. Please check if those are correct information."
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "모든 유형의 대체 연락처가 등록되어 있습니다. 정확한 정보인지 확인해주세요."
    
    def warning(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "Some alternate contacts have not been registered."
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "연락처가 등록되지 않은 대체 연락처 유형이 있습니다."

class BucketPublicAccess():
    def __init__(self, language):
        self.language = language

    def checking(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return ">>> Checking Bucket Public Access"
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return ">>> 개별 S3 Bucket의 Public Access 설정 확인 중"
    
    def title(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "Bucket-Level S3 Bucket Public Access Settings"
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "Bucket-Level의 S3 Bucket Public Access 설정 확인"

    def success(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "S3 Bucket has blocked all public access."
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "S3 Bucket의 모든 public access 정책이 차단되어 있습니다."

    def warning(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "S3 Bucket has allowed some public access policy."
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "S3 Bucket의 public access 정책이 일부 허용되어 있습니다."

    def danger(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "S3 Bucket has allowed all public access policy."
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "S3 Bucket의 모든 public access 정책이 모두 허용되어 있습니다."

    def bucket_limit_warning(self, maximum_number_of_bucket_limit) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "Maximum testable bucket count({MAXIMUM_NUMBER_OF_BUCKET_LIMIT}) exceeded. Please check manual or use AWS Trusted Advisor".format(MAXIMUM_NUMBER_OF_BUCKET_LIMIT=maximum_number_of_bucket_limit)
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "점검 가능한 최대 버킷 수({MAXIMUM_NUMBER_OF_BUCKET_LIMIT}) 초과. 수동으로 점검을 진행하거나 AWS Trusted Advisor를 이용해주세요.".format(MAXIMUM_NUMBER_OF_BUCKET_LIMIT=maximum_number_of_bucket_limit)

class CloudWatchAlarmConfiguration():
    def __init__(self, language):
        self.language = language

    def checking(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return ">>> Checking CloudWatch Alarm"
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return ">>> CloudWatch 알람 설정 확인"

    def title(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "Cloudwatch Alarm Configuration for Significant Event."
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "중요 이벤트에 대한 Cloudwatch 알람 설정"

    def alarm_exist(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "Cloudwatch Alarm has been configured. Please check there are significant alarm configurations such as billing, root activities about those alarms by manual."
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "Cloudwatch 알림이 구성되어 있습니다. 비용 알림, 루트 계정 활동 알림과 같은 중요 알림 구성 여부를 수동으로 확인해주세요."

    def alarm_not_exist(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return '''Cloudwatch Alarm has not been configured. Please try this &nbsp<a href="https://catalog.workshops.aws/startup-security-baseline/en-US/b-securing-your-account/7-configurealarms" target="_blank" style="overflow:hidden;word-break:break-all;">workshop</a> to know how to set alarm for significant events such as billing, root activities.'''
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return '''CloudWatch 알림이 구성되어 있지 않습니다. &nbsp<a href="https://catalog.workshops.aws/startup-security-baseline/en-US/b-securing-your-account/7-configurealarms" target="_blank" style="overflow:hidden;word-break:break-all;">워크샵</a>을 통해 비용 알림, 루트 계정 활동 알림을 설정방법을 확인해보세요.'''

class IAMDirectedAttachedPolicy():
    def __init__(self, language):
        self.language = language

    def checking(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return ">>> Checking Directly Attached Policy for IAM User"
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return ">>> IAM 사용자에게 직접 연결된 Policy 확인 중"

    def title(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "Directly Attached Policy to IAM User"
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "IAM 사용자에게 직접 연결된 정책 확인"
    
    def no_user(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "There is no IAM User"
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "IAM 사용자가 없습니다."

    def success(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "Policies for all IAM users are being managed efficiently without direct-attached policies."
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "IAM 사용자에게 직접 연결된 IAM 정책이 없습니다. 모든 IAM 사용자의 권한이 효율적으로 관리되고 있습니다."

    def warning(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "A policy exists that is directly attached to the IAM user."
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "IAM 사용자에게 직접 연결된 정책이 존재합니다."

class GuardDutyEnabled():
    def __init__(self, language):
        self.language = language

    def checking(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return ">>> Checking GuardDuty Setting"
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return ">>> GuardDuty 설정 확인 중"

    def title(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "GuardDuty Setting"
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "GuardDuty 설정"
    
    def is_activated(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "GuardDuty has been activated in more than one region"
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "GuardDuty가 한개 이상의 리전에서 활성화 되어 있습니다."

    def is_not_activated(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "GuardDuty has not been activated any region."
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "GuardDuty가 활성화 되어있는 리전이 없습니다."

class IAMPasswordPolicy():
    def __init__(self, language):
        self.language = language
    
    def checking(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return ">>> Checking IAM Password Policy"
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return ">>> IAM 비밀번호 정책 설정을 확인하는 중"

    def title(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "IAM Password Policy Setting"
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "IAM 비밀번호 정책 설정"
    
    def warning(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "IAM Password Policy has not been set. If you use any other credential such as IAM Role rather than root, you could ignore this warning."
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "IAM 비밀번호 정책이 설정되어 있지 않습니다. 만약 root 대신 IAM Role과 같은 다른 자격증명을 사용하는 경우 이 경고를 무시해도 됩니다."
    
    def success(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "IAM Password Policy has been set."
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "IAM 비밀번호 정책이 설정되어 있습니다."

class IAMUserMFASetting():
    def __init__(self, language):
        self.language = language

    def checking(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return ">>> Checking MFA Setting for IAM User"
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return ">>> IAM 사용자의 MFA 설정을 확인하는 중"

    def title(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "MFA Setting for IAM User"
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "IAM 사용자의 MFA 설정"

    def no_iam_user(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "IAM user is not existed. If you use any other credential such as IAM Role rather than root, you could ignore this warning."
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "IAM 사용자가 없습니다. 만약 root 대신 IAM Role과 같은 다른 자격증명을 사용하는 경우 이 경고를 무시해도 됩니다."

    def success(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "All IAM User are using MFA."
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "모든 IAM 사용자가 MFA를 사용중입니다."

    def danger(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "There are IAM users who have not set up MFA."
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "MFA를 설정하지 않은 IAM 사용자가 있습니다."

class MultiRegionInstanceUsage():
    def __init__(self, language):
        self.language = language
    
    def checking(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return ">>> Checking EC2 instance usage in multi-region"
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return ">>> 여러 리전에서의 EC2 인스턴스 사용 여부 확인 중"
    def title(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "Number of instance usages by region"
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "리전 별 사용중인 EC2 인스턴스 수"

    def info_msg(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return '''Please check your instance usage by region. You can also use &nbsp<a href="https://us-east-1.console.aws.amazon.com/ec2globalview/home" target="_blank" style="overflow:hidden;word-break:break-all;">EC2 Global View</a> to check more details.'''
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return '''리전 별 인스턴스 사용량을 확인해주세요. &nbsp<a href="https://us-east-1.console.aws.amazon.com/ec2globalview/home" target="_blank" style="overflow:hidden;word-break:break-all;">EC2 Global View</a> 를 이용하여 자세한 내용을 확인할 수 있습니다.'''

class MultiRegionTrail():
    def __init__(self, language):
        self.language = language

    def checking(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return ">>> Checking Multi-Region Logging Setting"
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return ">>> Multi-Region Logging 설정 확인 중"

    def title(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "Multi-Region Logging for CloudTrail Event Log"
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "CloudTrail 이벤트 로그의 Multi-Region Logging"

    def no_trail(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return '''There is no trail created. Please create trail.&nbsp(<a href="https://docs.aws.amazon.com/prescriptive-guidance/latest/aws-startup-security-baseline/acct-07.html" target="_blank" style="overflow:hidden;word-break:break-all;">How to create trail</a>)'''
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return '''생성된 trail이 없습니다. Trail을 생성해 주세요.&nbsp(<a href="https://docs.aws.amazon.com/ko_kr/prescriptive-guidance/latest/aws-startup-security-baseline/acct-07.html" target="_blank" style="overflow:hidden;word-break:break-all;">Trail 생성방법</a>)'''

    def danger(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "The multi-region logging has been disabled for all trail."
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "모든 Trail의 multi-region logging이 비활성화 되어 있습니다."

    def warning(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "Some trails have been disabled multi-region logging."
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "일부 trail에서 multi-region logging이 비활성화 되어있습니다."

    def success(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "The multi-region logging has been enabled for all trail."

class RootMFASetting():
    def __init__(self, language):
        self.language = language

    def checking(self):
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return ">>> Checking MFA for Root"
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return ">>> 루트 계정에 대한 MFA 설정 확인 중"

    def title(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "MFA for Root Account"
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "루트 계정에 대한 MFA 설정"
    
    def success(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "Root account enabled MFA"
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "루트 계정에 대한 MFA가 설정되어 있습니다."
    
    def danger(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return '''Root account disabled MFA.&nbsp Please check how to set MFA to root account via this <a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa_enable_virtual.html" target="_blank" style="overflow:hidden;word-break:break-all;">link</a>'''
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return '''루트 계정에 설정된 MFA가 없습니다.&nbsp<a href="https://docs.aws.amazon.com/ko_kr/IAM/latest/UserGuide/id_credentials_mfa_enable_virtual.html" target="_blank" style="overflow:hidden;word-break:break-all;">링크</a>를 눌러 설정방법을 확인해주세요.'''

class RootUsage():
    def __init__(self, language):
        self.language = language
    
    def checking(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return ">>> Checking root usage for recent 7 days."
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return ">>> 최근 7일동안의 루트 계정 사용여부를 확인하는 중"

    def title(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "Root Access"
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "루트 계정 Access"
    
    def success(self, root_access_days_standard) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "No root access history for last {standard_root_access_date} days.".format(standard_root_access_date=str(root_access_days_standard))
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "최근 {standard_root_access_date} 일 간 루트 계정 접속 기록이 없습니다.".format(standard_root_access_date=str(root_access_days_standard))

    def access_today(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "Root usage history exists for today. Please use AWS service with another credentials."
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "오늘 날짜의 루트 계정 사용이력이 존재합니다. 다른 자격증명으로 AWS 서비스를 이용해주세요."

    def danger(self, last_access_days) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "Root usage history exists for last {last_access_days}. Please use AWS service with another credentials.".format(last_access_days=str(last_access_days))
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "최근 {last_access_days} 이내에 루트 계정 사용이력이 존재합니다. 다른 자격증명으로 AWS 서비스를 이용해주세요.".format(last_access_days=str(last_access_days))

class RootAccessKey():
    def __init__(self, language):
        self.language = language

    def checking(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return ">>> Checking Generated Access Key for Root"
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return ">>> 루트 계정의 Access Key 생성 여부를 확인하는 중"

    def title(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "Generated Access Key for Root"
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "루트 계정의 Access Key 생성 여부를 확인하는 중"

    def success(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "No Access Key for Root"
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "루트 계정의 Access Key가 없습니다."
    
    def danger(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return '''The root access key is in use. It is safe not to use the root access key.&nbsp(<a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-user.html#id_root-user_manage_delete-key" target="_blank" style="overflow:hidden;word-break:break-all;">How to delete access key</a>)'''
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return '''루트계정에서 Access Key를 사용중입니다. 루트 계정의 Access Key는 사용하지 않는 것이 안전합니다.&nbsp(<a href="https://docs.aws.amazon.com/ko_kr/IAM/latest/UserGuide/id_root-user.html#id_root-user_manage_delete-key" target="_blank" style="overflow:hidden;word-break:break-all;">Access Key 삭제방법</a>)'''

class TrailEnabled():
    def __init__(self, language):
        self.language = language

    def checking(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return ">>> Checking Trail setting on CloudTrail"
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return ">>> CloudTrail의 추적 설정 확인 중"

    def title(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "Enable Trail on CloudTrail"
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "CloudTrail의 Trail 설정 확인"

    def no_trail(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return '''There is no Trail on CloudTrail. Please create Trail.&nbsp(<a href="https://docs.aws.amazon.com/prescriptive-guidance/latest/aws-startup-security-baseline/acct-07.html" target="_blank" style="overflow:hidden;word-break:break-all;">How to create Trail</a>)'''
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return '''생성된 Trail이 없습니다. Trail을 생성 해주세요.&nbsp(<a href="https://docs.aws.amazon.com/ko_kr/prescriptive-guidance/latest/aws-startup-security-baseline/acct-07.html" target="_blank" style="overflow:hidden;word-break:break-all;">Trail 생성방법</a>)'''

    def danger(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "Logging is disabled for all Trails. Please enable logging."
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "모든 Trail의 Logging 설정이 비활성화 되어있습니다. Logging을 활성화 해주세요."

    def warning(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "Logging is disabled for some Trails. Please enable logging."
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "일부 Trail의 Logging 설정이 비활성화 되어있습니다. Logging을 활성화 해주세요."

    def success(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "Logging is enabled for all Trails."
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "모든 Trail의 Logging 설정이 활성화 되어있습니다."

class TrustedAdvisor():
    def __init__(self, language):
        self.language = language

    def checking(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return ">>> Checking TrustedAdvisor Setting"
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return ">>> TrustedAdvisor 설정 확인 중"

    def title(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return "Enable Trusted Advisor"
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return "Trusted Advisor를 사용하도록 설정했는지 확인"

    def info(self) -> str:
        if self.language == LANGUAGE_CODE.ENGLISH.value:
            return '''Please&nbsp<a href="https://us-east-1.console.aws.amazon.com/trustedadvisor/home?region=ap-northeast-2#/preferences/manage-trusted-advisor" target="_blank" style="overflow:hidden;word-break:break-all;">check</a> the Trusted Advisor is enabled in your AWS account.'''
        elif self.language == LANGUAGE_CODE.KOREAN.value:
            return '''현재 계정의 Trusted Advisor 설정을&nbsp<a href="https://us-east-1.console.aws.amazon.com/trustedadvisor/home?region=ap-northeast-2#/preferences/manage-trusted-advisor" target="_blank" style="overflow:hidden;word-break:break-all;">확인</a>하세요.'''