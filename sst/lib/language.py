from enum import Enum
from abc import ABC, abstractmethod

class LanguageCode(Enum):
    ENGLISH = "ENG"
    KOREAN = "KOR"
    JAPANESE = "JPN"

class BaseTranslator(ABC):
    def __init__(self, language):
        self.language = language

    @abstractmethod
    def translate(self, key):
        pass

class MainTranslator(BaseTranslator):
    def translate(self, key):
        translations = {
            "invalid_iam_entity": {
                LanguageCode.ENGLISH.value: "This IAM entity is not supported. Please use an IAM user profile.",
                LanguageCode.KOREAN.value: "지원하지 않는 IAM Entity입니다. IAM 사용자 Profile을 사용해 주세요.",
                LanguageCode.JAPANESE.value: "このIAMエンティティはサポートされていません。IAMユーザープロファイルを使用してください。"
            },
            "start_test": {
                LanguageCode.ENGLISH.value: ">>> Starting the security baseline test",
                LanguageCode.KOREAN.value: ">>> 점검을 시작합니다",
                LanguageCode.JAPANESE.value: ">>> セキュリティベースラインテストを開始します"
            },
            "generate_result_report": {
                LanguageCode.ENGLISH.value: ">>> Generating the result report...",
                LanguageCode.KOREAN.value: ">>> 결과 리포트 생성 중...",
                LanguageCode.JAPANESE.value: ">>> 結果レポートを生成中..."
            },
            "request_credential_report": {
                LanguageCode.ENGLISH.value: ">>> Retrieving the credential report...",
                LanguageCode.KOREAN.value: ">>> Credential Report를 가져오는 중...",
                LanguageCode.JAPANESE.value: ">>> 認証情報レポートを取得中..."
            },
            "test_completed": {
                LanguageCode.ENGLISH.value: ">>> All inspection items were successfully checked.",
                LanguageCode.KOREAN.value: ">>> 모든 점검 항목이 성공적으로 검사되었습니다.",
                LanguageCode.JAPANESE.value: ">>> すべての検査項目が正常に確認されました。"
            },
            "results_folder_created": {
                LanguageCode.ENGLISH.value: "'results' folder has been created.",
                LanguageCode.KOREAN.value: "'results' 폴더가 생성되었습니다.",
                LanguageCode.JAPANESE.value: "'results' フォルダーが作成されました。"
            },
            "results_folder_already_exists": {
                LanguageCode.ENGLISH.value: "'results' folder already exists.",
                LanguageCode.KOREAN.value: "'results' 폴더가 이미 존재합니다.",
                LanguageCode.JAPANESE.value: "'results' フォルダーはすでに存在します。"
            }
        }
        return translations.get(key, {}).get(self.language, "Translation not available")

class AccountLevelBucketPublicAccessTranslator(BaseTranslator):
    def translate(self, key):
        translations = {
            "checking": {
                LanguageCode.ENGLISH.value: ">>> Checking account-level S3 bucket public access settings",
                LanguageCode.KOREAN.value: ">>> 계정 수준의 S3 Bucket Public Access 확인 중",
                LanguageCode.JAPANESE.value: ">>> アカウントレベルのS3バケットパブリックアクセス設定を確認中"
            },
            "title": {
                LanguageCode.ENGLISH.value: "Account-Level S3 Bucket Public Access Settings",
                LanguageCode.KOREAN.value: "계정 수준 S3 Bucket Public Access 설정",
                LanguageCode.JAPANESE.value: "アカウントレベルのS3バケットパブリックアクセス設定"
            },
            "no_such_public_access_block_config": {
                LanguageCode.ENGLISH.value: "No public access block configuration found at the account level.",
                LanguageCode.KOREAN.value: "계정의 기본 S3 Bucket Public Access Block 정책이 설정되어 있지 않습니다.",
                LanguageCode.JAPANESE.value: "アカウントレベルのパブリックアクセスブロック設定が見つかりません。"
            },
            "success": {
                LanguageCode.ENGLISH.value: "All account-level S3 bucket public access settings are blocked.",
                LanguageCode.KOREAN.value: "계정의 기본 S3 Bucket Public Access 정책이 모두 차단되어 있습니다.",
                LanguageCode.JAPANESE.value: "アカウントレベルのS3バケットパブリックアクセス設定がすべてブロックされています。"
            },
            "warning": {
                LanguageCode.ENGLISH.value: "Some account-level S3 bucket public access settings are allowed.",
                LanguageCode.KOREAN.value: "계정의 기본 S3 Bucket Public Access 정책이 일부 허용되어 있습니다.",
                LanguageCode.JAPANESE.value: "一部のアカウントレベルS3バケットパブリックアクセス設定が許可されています。"
            },
            "danger": {
                LanguageCode.ENGLISH.value: "All account-level S3 bucket public access settings are allowed.",
                LanguageCode.KOREAN.value: "계정의 기본 S3 Bucket Public Access 정책이 모두 허용되어 있습니다.",
                LanguageCode.JAPANESE.value: "すべてのアカウントレベルS3バケットパブリックアクセス設定が許可されています。"
            },
            "unexpected_error": {
                LanguageCode.ENGLISH.value: "An unexpected error occurred.",
                LanguageCode.KOREAN.value: "예기치 않은 오류가 발생했습니다.",
                LanguageCode.JAPANESE.value: "予期せぬエラーが発生しました。"
            },
            "aws_api_error": {
                LanguageCode.ENGLISH.value: "An AWS API error occurred.",
                LanguageCode.KOREAN.value: "AWS API 오류가 발생했습니다.",
                LanguageCode.JAPANESE.value: "AWS APIエラーが発生しました。"
            },
            "boto3_error": {
                LanguageCode.ENGLISH.value: "A Boto3 error occurred.",
                LanguageCode.KOREAN.value: "Boto3 오류가 발생했습니다.",
                LanguageCode.JAPANESE.value: "Boto3エラーが発生しました。"
            }
        }
        return translations.get(key, {}).get(self.language, "Translation not available")

class AlternateContactTranslator(BaseTranslator):
    def translate(self, key):
        translations = {
            "checking": {
                LanguageCode.ENGLISH.value: ">>> Checking alternate contacts",
                LanguageCode.KOREAN.value: ">>> 대체 연락처 등록을 확인하는 중",
                LanguageCode.JAPANESE.value: ">>> 代替連絡先の登録を確認中"
            },
            "title": {
                LanguageCode.ENGLISH.value: "Alternate Contacts Registration",
                LanguageCode.KOREAN.value: "대체 연락처 등록 확인",
                LanguageCode.JAPANESE.value: "代替連絡先の登録確認"
            },
            "success": {
                LanguageCode.ENGLISH.value: "All types of alternate contacts have been registered. Please verify if the information is correct.",
                LanguageCode.KOREAN.value: "모든 유형의 대체 연락처가 등록되어 있습니다. 정확한 정보인지 확인해주세요.",
                LanguageCode.JAPANESE.value: "すべてのタイプの代替連絡先が登録されています。情報が正確であるか確認してください。"
            },
            "warning": {
                LanguageCode.ENGLISH.value: "Some types of alternate contacts have not been registered.",
                LanguageCode.KOREAN.value: "연락처가 등록되지 않은 대체 연락처 유형이 있습니다.",
                LanguageCode.JAPANESE.value: "登録されていない代替連絡先のタイプがあります。"
            },
        }
        
        return translations.get(key, {}).get(self.language, "Translation not available")

class BucketPublicAccessTranslator(BaseTranslator):
    def translate(self, key):
        translations = {
            "checking": {
                LanguageCode.ENGLISH.value: ">>> Checking individual S3 bucket public access settings",
                LanguageCode.KOREAN.value: ">>> 개별 S3 Bucket의 Public Access 설정 확인 중",
                LanguageCode.JAPANESE.value: ">>> 個々のS3バケットのパブリックアクセス設定を確認中"
            },
            "title": {
                LanguageCode.ENGLISH.value: "Individual S3 Bucket Public Access Settings",
                LanguageCode.KOREAN.value: "Bucket-Level의 S3 Bucket Public Access 설정 확인",
                LanguageCode.JAPANESE.value: "個別S3バケットのパブリックアクセス設定"
            },
            "success": {
                LanguageCode.ENGLISH.value: "All S3 buckets have blocked public access.",
                LanguageCode.KOREAN.value: "S3 Bucket의 모든 public access 정책이 차단되어 있습니다.",
                LanguageCode.JAPANESE.value: "すべてのS3バケットでパブリックアクセスがブロックされています。"
            },
            "warning": {
                LanguageCode.ENGLISH.value: "Some S3 buckets have allowed public access policies.",
                LanguageCode.KOREAN.value: "S3 Bucket의 public access 정책이 일부 허용되어 있습니다.",
                LanguageCode.JAPANESE.value: "一部のS3バケットでパブリックアクセスポリシーが許可されています。"
            },
            "danger": {
                LanguageCode.ENGLISH.value: "All S3 buckets have allowed public access policies.",
                LanguageCode.KOREAN.value: "S3 Bucket의 모든 public access 정책이 모두 허용되어 있습니다.",
                LanguageCode.JAPANESE.value: "すべてのS3バケットでパブリックアクセスポリシーが許可されています。"
            },
            "bucket_limit_warning": {
                LanguageCode.ENGLISH.value: "Maximum testable bucket count ({0}) exceeded. Please check manually or use AWS Trusted Advisor.",
                LanguageCode.KOREAN.value: "점검 가능한 최대 버킷 수({0}) 초과. 수동으로 점검을 진행하거나 AWS Trusted Advisor를 이용해주세요.",
                LanguageCode.JAPANESE.value: "テスト可能な最大バケット数（{0}）を超えています。手動で確認するか、AWS Trusted Advisorを使用してください。"
            },
            "unexpected_error": {
                LanguageCode.ENGLISH.value: "An unexpected error occurred.",
                LanguageCode.KOREAN.value: "예기치 않은 오류가 발생했습니다.",
                LanguageCode.JAPANESE.value: "予期せぬエラーが発生しました。"
            }
        }
        return translations.get(key, {}).get(self.language, "Translation not available")

class CloudWatchAlarmConfigurationTranslator(BaseTranslator):
    def translate(self, key):
        translations = {
            "checking": {
                LanguageCode.ENGLISH.value: ">>> Checking CloudWatch Alarm settings",
                LanguageCode.KOREAN.value: ">>> CloudWatch 알람 설정 확인",
                LanguageCode.JAPANESE.value: ">>> CloudWatchアラーム設定を確認中"
            },
            "title": {
                LanguageCode.ENGLISH.value: "CloudWatch Alarm Configuration for Significant Events",
                LanguageCode.KOREAN.value: "중요 이벤트에 대한 CloudWatch 알람 설정",
                LanguageCode.JAPANESE.value: "重要イベントに対するCloudWatchアラーム設定"
            },
            "alarm_exist": {
                LanguageCode.ENGLISH.value: "CloudWatch Alarms have been configured. Please manually check if there are important alarm configurations such as billing and root account activity alerts.",
                LanguageCode.KOREAN.value: "CloudWatch 알림이 구성되어 있습니다. 비용 알림, 루트 계정 활동 알림과 같은 중요 알림 구성 여부를 수동으로 확인해주세요.",
                LanguageCode.JAPANESE.value: "CloudWatchアラームが設定されています。請求やルートアカウントのアクティビティなどの重要なアラーム設定があるか手動で確認してください。"
            },
            "alarm_not_exist": {
                LanguageCode.ENGLISH.value: "CloudWatch Alarms have not been configured. Please try this <a href=\"https://catalog.workshops.aws/startup-security-baseline/en-US/b-securing-your-account/7-configurealarms\" target=\"_blank\" style=\"overflow:hidden;word-break:break-all;\">workshop</a> to learn how to set alarms for significant events such as billing and root account activities.",
                LanguageCode.KOREAN.value: "CloudWatch 알림이 구성되어 있지 않습니다. <a href=\"https://catalog.workshops.aws/startup-security-baseline/en-US/b-securing-your-account/7-configurealarms\" target=\"_blank\" style=\"overflow:hidden;word-break:break-all;\">워크샵</a>을 통해 비용 알림, 루트 계정 활동 알림을 설정방법을 확인해보세요.",
                LanguageCode.JAPANESE.value: "CloudWatchアラームが設定されていません。請求やルートアカウントのアクティビティなどの重要なイベントにアラームを設定する方法については、この<a href=\"https://catalog.workshops.aws/startup-security-baseline/en-US/b-securing-your-account/7-configurealarms\" target=\"_blank\" style=\"overflow:hidden;word-break:break-all;\">ワークショップ</a>を試してください。"
            },
            "unexpected_error": {
                LanguageCode.ENGLISH.value: "An unexpected error occurred.",
                LanguageCode.KOREAN.value: "예기치 않은 오류가 발생했습니다.",
                LanguageCode.JAPANESE.value: "予期せぬエラーが発生しました。"
            },
            "retrieval_error": {
                LanguageCode.ENGLISH.value: "Failed to retrieve alarm configurations in some or all regions.",
                LanguageCode.KOREAN.value: "일부 또는 모든 리전에서 알람 구성을 가져오는 데 실패했습니다.",
                LanguageCode.JAPANESE.value: "一部または全てのリージョンでアラーム設定の取得に失敗しました。"
            }
        }
        return translations.get(key, {}).get(self.language, "Translation not available")
    
class IAMDirectAttachedPolicyTranslator(BaseTranslator):
    def translate(self, key):
        translations = {
            "checking": {
                LanguageCode.ENGLISH.value: ">>> Checking directly attached policies for IAM users",
                LanguageCode.KOREAN.value: ">>> IAM 사용자에게 직접 연결된 Policy 확인 중",
                LanguageCode.JAPANESE.value: ">>> IAMユーザーに直接アタッチされたポリシーを確認中"
            },
            "title": {
                LanguageCode.ENGLISH.value: "Directly Attached Policies to IAM Users",
                LanguageCode.KOREAN.value: "IAM 사용자에게 직접 연결된 정책 확인",
                LanguageCode.JAPANESE.value: "IAMユーザーに直接アタッチされたポリシー"
            },
            "no_user": {
                LanguageCode.ENGLISH.value: "There are no IAM users",
                LanguageCode.KOREAN.value: "IAM 사용자가 없습니다.",
                LanguageCode.JAPANESE.value: "IAMユーザーが存在しません"
            },
            "success": {
                LanguageCode.ENGLISH.value: "No IAM policies are directly attached to users. All IAM user permissions are being managed efficiently.",
                LanguageCode.KOREAN.value: "IAM 사용자에게 직접 연결된 IAM 정책이 없습니다. 모든 IAM 사용자의 권한이 효율적으로 관리되고 있습니다.",
                LanguageCode.JAPANESE.value: "IAMユーザーに直接アタッチされたIAMポリシーはありません。すべてのIAMユーザーの権限が効率的に管理されています。"
            },
            "warning": {
                LanguageCode.ENGLISH.value: "There are policies directly attached to IAM users.",
                LanguageCode.KOREAN.value: "IAM 사용자에게 직접 연결된 정책이 존재합니다.",
                LanguageCode.JAPANESE.value: "IAMユーザーに直接アタッチされたポリシーが存在します。"
            },
            "service_failure": {
                LanguageCode.ENGLISH.value: "A service failure occurred.",
                LanguageCode.KOREAN.value: "서비스 실패가 발생했습니다.",
                LanguageCode.JAPANESE.value: "サービス障害が発生しました。"
            },
            "unexpected_error": {
                LanguageCode.ENGLISH.value: "An unexpected error occurred.",
                LanguageCode.KOREAN.value: "예기치 않은 오류가 발생했습니다.",
                LanguageCode.JAPANESE.value: "予期せぬエラーが発生しました。"
            }
        }
        return translations.get(key, {}).get(self.language, "Translation not available")

class GuardDutyEnabledTranslator(BaseTranslator):
    def translate(self, key):
        translations = {
            "checking": {
                LanguageCode.ENGLISH.value: ">>> Checking GuardDuty settings",
                LanguageCode.KOREAN.value: ">>> GuardDuty 설정 확인 중",
                LanguageCode.JAPANESE.value: ">>> GuardDutyの設定を確認中"
            },
            "title": {
                LanguageCode.ENGLISH.value: "GuardDuty Settings",
                LanguageCode.KOREAN.value: "GuardDuty 설정",
                LanguageCode.JAPANESE.value: "GuardDutyの設定"
            },
            "is_activated": {
                LanguageCode.ENGLISH.value: "GuardDuty has been activated in one or more regions",
                LanguageCode.KOREAN.value: "GuardDuty가 한개 이상의 리전에서 활성화 되어 있습니다.",
                LanguageCode.JAPANESE.value: "GuardDutyが1つ以上のリージョンで有効化されています"
            },
            "is_not_activated": {
                LanguageCode.ENGLISH.value: "GuardDuty has not been activated in any region.",
                LanguageCode.KOREAN.value: "GuardDuty가 활성화 되어있는 리전이 없습니다.",
                LanguageCode.JAPANESE.value: "GuardDutyがどのリージョンでも有効化されていません"
            },
            "retrieval_error": {
                LanguageCode.ENGLISH.value: "Failed to retrieve GuardDuty status from some regions.",
                LanguageCode.KOREAN.value: "일부 리전에서 GuardDuty 상태를 가져오는 데 실패했습니다.",
                LanguageCode.JAPANESE.value: "一部のリージョンでGuardDutyの状態の取得に失敗しました。"
            }
        }
        return translations.get(key, {}).get(self.language, "Translation not available")

class IAMPasswordPolicyTranslator(BaseTranslator):
    def translate(self, key):
        translations = {
            "checking": {
                LanguageCode.ENGLISH.value: ">>> Checking IAM password policy settings",
                LanguageCode.KOREAN.value: ">>> IAM 비밀번호 정책 설정을 확인하는 중",
                LanguageCode.JAPANESE.value: ">>> IAMパスワードポリシー設定を確認中"
            },
            "title": {
                LanguageCode.ENGLISH.value: "IAM Password Policy Settings",
                LanguageCode.KOREAN.value: "IAM 비밀번호 정책 설정",
                LanguageCode.JAPANESE.value: "IAMパスワードポリシー設定"
            },
            "warning": {
                LanguageCode.ENGLISH.value: "IAM password policy has not been set. If you use other credentials such as IAM roles instead of root, you may ignore this warning.",
                LanguageCode.KOREAN.value: "IAM 비밀번호 정책이 설정되어 있지 않습니다. 만약 root 대신 IAM Role과 같은 다른 자격증명을 사용하는 경우 이 경고를 무시해도 됩니다.",
                LanguageCode.JAPANESE.value: "IAMパスワードポリシーが設定されていません。ルートの代わりにIAMロールなどの他の認証情報を使用している場合、この警告は無視しても構いません。"
            },
            "success": {
                LanguageCode.ENGLISH.value: "IAM password policy has been set.",
                LanguageCode.KOREAN.value: "IAM 비밀번호 정책이 설정되어 있습니다.",
                LanguageCode.JAPANESE.value: "IAMパスワードポリシーが設定されています。"
            },
            "service_failure": {
                LanguageCode.ENGLISH.value: "A service failure occurred.",
                LanguageCode.KOREAN.value: "서비스 실패가 발생했습니다.",
                LanguageCode.JAPANESE.value: "サービス障害が発生しました。"
            },
            "unexpected_error": {
                LanguageCode.ENGLISH.value: "An unexpected error occurred.",
                LanguageCode.KOREAN.value: "예기치 않은 오류가 발생했습니다.",
                LanguageCode.JAPANESE.value: "予期せぬエラーが発生しました。"
            }
        }
        return translations.get(key, {}).get(self.language, "Translation not available")

class IAMUserMFASettingTranslator(BaseTranslator):
    def translate(self, key):
        translations = {
            "checking": {
                LanguageCode.ENGLISH.value: ">>> Checking MFA settings for IAM users",
                LanguageCode.KOREAN.value: ">>> IAM 사용자의 MFA 설정을 확인하는 중",
                LanguageCode.JAPANESE.value: ">>> IAMユーザーのMFA設定を確認中"
            },
            "title": {
                LanguageCode.ENGLISH.value: "MFA Settings for IAM Users",
                LanguageCode.KOREAN.value: "IAM 사용자의 MFA 설정",
                LanguageCode.JAPANESE.value: "IAMユーザーのMFA設定"
            },
            "no_iam_user": {
                LanguageCode.ENGLISH.value: "No IAM users exist. If you use other credentials such as IAM roles instead of root, you may ignore this warning.",
                LanguageCode.KOREAN.value: "IAM 사용자가 없습니다. 만약 root 대신 IAM Role과 같은 다른 자격증명을 사용하는 경우 이 경고를 무시해도 됩니다.",
                LanguageCode.JAPANESE.value: "IAMユーザーが存在しません。ルートの代わりにIAMロールなどの他の認証情報を使用している場合、この警告は無視しても構いません。"
            },
            "success": {
                LanguageCode.ENGLISH.value: "All IAM users are using MFA.",
                LanguageCode.KOREAN.value: "모든 IAM 사용자가 MFA를 사용중입니다.",
                LanguageCode.JAPANESE.value: "すべてのIAMユーザーがMFAを使用しています。"
            },
            "danger": {
                LanguageCode.ENGLISH.value: "There are IAM users who have not set up MFA.",
                LanguageCode.KOREAN.value: "MFA를 설정하지 않은 IAM 사용자가 있습니다.",
                LanguageCode.JAPANESE.value: "MFAを設定していないIAMユーザーがいます。"
            },
            "credential_report_error": {
                LanguageCode.ENGLISH.value: "Failed to generate credential report",
                LanguageCode.KOREAN.value: "자격 증명 보고서 생성에 실패했습니다",
                LanguageCode.JAPANESE.value: "認証情報レポートの生成に失敗しました"
            }
        }
        return translations.get(key, {}).get(self.language, "Translation not available")

class MultiRegionInstanceUsageTranslator(BaseTranslator):
    def translate(self, key):
        translations = {
            "checking": {
                LanguageCode.ENGLISH.value: ">>> Checking EC2 instance usage across multiple regions",
                LanguageCode.KOREAN.value: ">>> 여러 리전에서의 EC2 인스턴스 사용 여부 확인 중",
                LanguageCode.JAPANESE.value: ">>> 複数のリージョンでのEC2インスタンス使用状況を確認中"
            },
            "title": {
                LanguageCode.ENGLISH.value: "Number of EC2 Instances in Use by Region",
                LanguageCode.KOREAN.value: "리전 별 사용중인 EC2 인스턴스 수",
                LanguageCode.JAPANESE.value: "リージョン別の使用中EC2インスタンス数"
            },
            "info_msg": {
                LanguageCode.ENGLISH.value: 'Please check your instance usage by region. You can also use <a href="https://us-east-1.console.aws.amazon.com/ec2globalview/home" target="_blank" style="overflow:hidden;word-break:break-all;">EC2 Global View</a> to check more details.',
                LanguageCode.KOREAN.value: '리전 별 인스턴스 사용량을 확인해주세요. <a href="https://us-east-1.console.aws.amazon.com/ec2globalview/home" target="_blank" style="overflow:hidden;word-break:break-all;">EC2 Global View</a> 를 이용하여 자세한 내용을 확인할 수 있습니다.',
                LanguageCode.JAPANESE.value: 'リージョン別のインスタンス使用状況を確認してください。詳細は<a href="https://us-east-1.console.aws.amazon.com/ec2globalview/home" target="_blank" style="overflow:hidden;word-break:break-all;">EC2 Global View</a>を使用して確認できます。'
            },
            "unexpected_error": {
                LanguageCode.ENGLISH.value: "An unexpected error occurred.",
                LanguageCode.KOREAN.value: "예기치 않은 오류가 발생했습니다.",
                LanguageCode.JAPANESE.value: "予期せぬエラーが発生しました。"
            },
            "retrieval_error": {
                LanguageCode.ENGLISH.value: "Failed to retrieve instance usage information from some regions.",
                LanguageCode.KOREAN.value: "일부 리전에서 인스턴스 사용 정보를 가져오는 데 실패했습니다.",
                LanguageCode.JAPANESE.value: "一部のリージョンでインスタンス使用情報の取得に失敗しました。"
            }
        }
        return translations.get(key, {}).get(self.language, "Translation not available")

class MultiRegionTrailTranslator(BaseTranslator):
    def translate(self, key):
        translations = {
            "checking": {
                LanguageCode.ENGLISH.value: ">>> Checking multi-region logging settings",
                LanguageCode.KOREAN.value: ">>> Multi-Region Logging 설정 확인 중",
                LanguageCode.JAPANESE.value: ">>> マルチリージョンロギング設定を確認中"
            },
            "title": {
                LanguageCode.ENGLISH.value: "Multi-Region Logging for CloudTrail Event Logs",
                LanguageCode.KOREAN.value: "CloudTrail 이벤트 로그의 Multi-Region Logging",
                LanguageCode.JAPANESE.value: "CloudTrailイベントログのマルチリージョンロギング"
            },
            "no_trail": {
                LanguageCode.ENGLISH.value: 'No trail has been created. Please create a trail. (<a href="https://docs.aws.amazon.com/prescriptive-guidance/latest/aws-startup-security-baseline/acct-07.html" target="_blank" style="overflow:hidden;word-break:break-all;">How to create a trail</a>)',
                LanguageCode.KOREAN.value: '생성된 trail이 없습니다. Trail을 생성해 주세요. (<a href="https://docs.aws.amazon.com/ko_kr/prescriptive-guidance/latest/aws-startup-security-baseline/acct-07.html" target="_blank" style="overflow:hidden;word-break:break-all;">Trail 생성방법</a>)',
                LanguageCode.JAPANESE.value: 'トレイルが作成されていません。トレイルを作成してください。(<a href="https://docs.aws.amazon.com/ja_jp/prescriptive-guidance/latest/aws-startup-security-baseline/acct-07.html" target="_blank" style="overflow:hidden;word-break:break-all;">トレイルの作成方法</a>)'
            },
            "danger": {
                LanguageCode.ENGLISH.value: "Multi-region logging has been disabled for all trails.",
                LanguageCode.KOREAN.value: "모든 Trail의 multi-region logging이 비활성화 되어 있습니다.",
                LanguageCode.JAPANESE.value: "すべてのトレイルでマルチリージョンロギングが無効になっています。"
            },
            "warning": {
                LanguageCode.ENGLISH.value: "Multi-region logging has been disabled for some trails.",
                LanguageCode.KOREAN.value: "일부 trail에서 multi-region logging이 비활성화 되어있습니다.",
                LanguageCode.JAPANESE.value: "一部のトレイルでマルチリージョンロギングが無効になっています。"
            },
            "success": {
                LanguageCode.ENGLISH.value: "Multi-region logging has been enabled for all trails.",
                LanguageCode.KOREAN.value: "모든 Trail의 multi-region logging이 활성화 되어 있습니다.",
                LanguageCode.JAPANESE.value: "すべてのトレイルでマルチリージョンロギングが有効になっています。"
            },
            "describe_trails_error": {
                LanguageCode.ENGLISH.value: "Error occurred while describing trails.",
                LanguageCode.KOREAN.value: "트레일 설명을 가져오는 중 오류가 발생했습니다.",
                LanguageCode.JAPANESE.value: "トレイルの説明を取得中にエラーが発生しました。"
            },
            "get_trail_error": {
                LanguageCode.ENGLISH.value: "Error occurred while getting trail information.",
                LanguageCode.KOREAN.value: "트레일 정보를 가져오는 중 오류가 발생했습니다.",
                LanguageCode.JAPANESE.value: "トレイル情報の取得中にエラーが発生しました。"
            }
        }
        return translations.get(key, {}).get(self.language, "Translation not available")
    
class RootMFASettingTranslator(BaseTranslator):
    def translate(self, key):
        translations = {
            "checking": {
                LanguageCode.ENGLISH.value: ">>> Checking MFA settings for the root account",
                LanguageCode.KOREAN.value: ">>> 루트 계정에 대한 MFA 설정 확인 중",
                LanguageCode.JAPANESE.value: ">>> ルートアカウントのMFA設定を確認中"
            },
            "title": {
                LanguageCode.ENGLISH.value: "MFA Settings for Root Account",
                LanguageCode.KOREAN.value: "루트 계정에 대한 MFA 설정",
                LanguageCode.JAPANESE.value: "ルートアカウントのMFA設定"
            },
            "success": {
                LanguageCode.ENGLISH.value: "MFA is enabled for the root account",
                LanguageCode.KOREAN.value: "루트 계정에 대한 MFA가 설정되어 있습니다.",
                LanguageCode.JAPANESE.value: "ルートアカウントのMFAが有効になっています"
            },
            "danger": {
                LanguageCode.ENGLISH.value: 'MFA is disabled for the root account. Please check how to set up MFA for the root account via this <a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa_enable_virtual.html" target="_blank" style="overflow:hidden;word-break:break-all;">link</a>',
                LanguageCode.KOREAN.value: '루트 계정에 설정된 MFA가 없습니다. <a href="https://docs.aws.amazon.com/ko_kr/IAM/latest/UserGuide/id_credentials_mfa_enable_virtual.html" target="_blank" style="overflow:hidden;word-break:break-all;">링크</a>를 눌러 설정방법을 확인해주세요.',
                LanguageCode.JAPANESE.value: 'ルートアカウントのMFAが無効になっています。ルートアカウントのMFA設定方法については、この<a href="https://docs.aws.amazon.com/ja_jp/IAM/latest/UserGuide/id_credentials_mfa_enable_virtual.html" target="_blank" style="overflow:hidden;word-break:break-all;">リンク</a>を確認してください'
            },
            "credential_report_error": {
                LanguageCode.ENGLISH.value: "Failed to generate credential report.",
                LanguageCode.KOREAN.value: "자격 증명 보고서 생성에 실패했습니다.",
                LanguageCode.JAPANESE.value: "認証情報レポートの生成に失敗しました。"
            },
            "processing_error": {
                LanguageCode.ENGLISH.value: "Error occurred while processing root credential report.",
                LanguageCode.KOREAN.value: "루트 자격 증명 보고서 처리 중 오류가 발생했습니다.",
                LanguageCode.JAPANESE.value: "ルート認証情報レポートの処理中にエラーが発生しました。"
            }
        }
        return translations.get(key, {}).get(self.language, "Translation not available")

class RootUsageTranslator(BaseTranslator):
    def translate(self, key):
        translations = {
            "checking": {
                LanguageCode.ENGLISH.value: ">>> Checking root account usage for the last 7 days",
                LanguageCode.KOREAN.value: ">>> 최근 7일동안의 루트 계정 사용여부를 확인하는 중",
                LanguageCode.JAPANESE.value: ">>> 過去7日間のルートアカウント使用状況を確認中"
            },
            "title": {
                LanguageCode.ENGLISH.value: "Root Account Access",
                LanguageCode.KOREAN.value: "루트 계정 Access",
                LanguageCode.JAPANESE.value: "ルートアカウントのアクセス"
            },
            "success": {
                LanguageCode.ENGLISH.value: "No root access history for the last {0} days.",
                LanguageCode.KOREAN.value: "최근 {0}일 간 루트 계정 접속 기록이 없습니다.",
                LanguageCode.JAPANESE.value: "過去{0}日間のルートアカウントアクセス履歴はありません。"
            },
            "access_today": {
                LanguageCode.ENGLISH.value: "Root account usage history exists for today. Please use AWS services with another credential.",
                LanguageCode.KOREAN.value: "오늘 날짜의 루트 계정 사용이력이 존재합니다. 다른 자격증명으로 AWS 서비스를 이용해주세요.",
                LanguageCode.JAPANESE.value: "本日のルートアカウント使用履歴が存在します。他の認証情報でAWSサービスを利用してください。"
            },
            "danger": {
                LanguageCode.ENGLISH.value: "Root account usage history exists within the last {0} days. Please use AWS services with another credential.",
                LanguageCode.KOREAN.value: "최근 {0} 이내에 루트 계정 사용이력이 존재합니다. 다른 자격증명으로 AWS 서비스를 이용해주세요.",
                LanguageCode.JAPANESE.value: "過去{0}日以内にルートアカウントの使用履歴があります。他の認証情報でAWSサービスを利用してください。"
            },
            "credential_report_error": {
                LanguageCode.ENGLISH.value: "Failed to generate credential report.",
                LanguageCode.KOREAN.value: "자격 증명 보고서 생성에 실패했습니다.",
                LanguageCode.JAPANESE.value: "認証情報レポートの生成に失敗しました。"
            },
            "processing_error": {
                LanguageCode.ENGLISH.value: "Error occurred while processing root usage check.",
                LanguageCode.KOREAN.value: "루트 사용 확인 처리 중 오류가 발생했습니다.",
                LanguageCode.JAPANESE.value: "ルート使用状況の確認処理中にエラーが発生しました。"
            }
        }
        return translations.get(key, {}).get(self.language, "Translation not available")

class RootAccessKeyTranslator(BaseTranslator):
    def translate(self, key):
        translations = {
            "checking": {
                LanguageCode.ENGLISH.value: ">>> Checking for generated access keys for the root account",
                LanguageCode.KOREAN.value: ">>> 루트 계정의 Access Key 생성 여부를 확인하는 중",
                LanguageCode.JAPANESE.value: ">>> ルートアカウントの生成されたアクセスキーを確認中"
            },
            "title": {
                LanguageCode.ENGLISH.value: "Generated Access Keys for Root Account",
                LanguageCode.KOREAN.value: "루트 계정의 Access Key 생성 여부를 확인하는 중",
                LanguageCode.JAPANESE.value: "ルートアカウントの生成されたアクセスキー"
            },
            "success": {
                LanguageCode.ENGLISH.value: "No access keys for the root account",
                LanguageCode.KOREAN.value: "루트 계정의 Access Key가 없습니다.",
                LanguageCode.JAPANESE.value: "ルートアカウントのアクセスキーはありません"
            },
            "danger": {
                LanguageCode.ENGLISH.value: 'The root account access key is in use. It is safer not to use the root access key. (<a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-user.html#id_root-user_manage_delete-key" target="_blank" style="overflow:hidden;word-break:break-all;">How to delete access key</a>)',
                LanguageCode.KOREAN.value: '루트계정에서 Access Key를 사용중입니다. 루트 계정의 Access Key는 사용하지 않는 것이 안전합니다. (<a href="https://docs.aws.amazon.com/ko_kr/IAM/latest/UserGuide/id_root-user.html#id_root-user_manage_delete-key" target="_blank" style="overflow:hidden;word-break:break-all;">Access Key 삭제방법</a>)',
                LanguageCode.JAPANESE.value: 'ルートアカウントのアクセスキーが使用中です。ルートアカウントのアクセスキーを使用しない方が安全です。(<a href="https://docs.aws.amazon.com/ja_jp/IAM/latest/UserGuide/id_root-user.html#id_root-user_manage_delete-key" target="_blank" style="overflow:hidden;word-break:break-all;">アクセスキーの削除方法</a>)'
            },
            "credential_report_error": {
                LanguageCode.ENGLISH.value: "Failed to generate credential report.",
                LanguageCode.KOREAN.value: "자격 증명 보고서 생성에 실패했습니다.",
                LanguageCode.JAPANESE.value: "認証情報レポートの生成に失敗しました。"
            },
            "processing_error": {
                LanguageCode.ENGLISH.value: "Error occurred while processing root access key check.",
                LanguageCode.KOREAN.value: "루트 액세스 키 확인 처리 중 오류가 발생했습니다.",
                LanguageCode.JAPANESE.value: "ルートアクセスキーの確認処理中にエラーが発生しました。"
            }
        }
        return translations.get(key, {}).get(self.language, "Translation not available")

class TrailEnabledTranslator(BaseTranslator):
    def translate(self, key):
        translations = {
            "checking": {
                LanguageCode.ENGLISH.value: ">>> Checking trail settings in CloudTrail",
                LanguageCode.KOREAN.value: ">>> CloudTrail의 추적 설정 확인 중",
                LanguageCode.JAPANESE.value: ">>> CloudTrailのトレイル設定を確認中"
            },
            "title": {
                LanguageCode.ENGLISH.value: "Enable Trail on CloudTrail",
                LanguageCode.KOREAN.value: "CloudTrail의 Trail 설정 확인",
                LanguageCode.JAPANESE.value: "CloudTrailのトレイル有効化"
            },
            "no_trail": {
                LanguageCode.ENGLISH.value: 'There is no trail on CloudTrail. Please create a trail. (<a href="https://docs.aws.amazon.com/prescriptive-guidance/latest/aws-startup-security-baseline/acct-07.html" target="_blank" style="overflow:hidden;word-break:break-all;">How to create a trail</a>)',
                LanguageCode.KOREAN.value: '생성된 Trail이 없습니다. Trail을 생성 해주세요. (<a href="https://docs.aws.amazon.com/ko_kr/prescriptive-guidance/latest/aws-startup-security-baseline/acct-07.html" target="_blank" style="overflow:hidden;word-break:break-all;">Trail 생성방법</a>)',
                LanguageCode.JAPANESE.value: 'CloudTrailにトレイルがありません。トレイルを作成してください。(<a href="https://docs.aws.amazon.com/ja_jp/prescriptive-guidance/latest/aws-startup-security-baseline/acct-07.html" target="_blank" style="overflow:hidden;word-break:break-all;">トレイルの作成方法</a>)'
            },
            "danger": {
                LanguageCode.ENGLISH.value: "Logging is disabled for all trails. Please enable logging.",
                LanguageCode.KOREAN.value: "모든 Trail의 Logging 설정이 비활성화 되어있습니다. Logging을 활성화 해주세요.",
                LanguageCode.JAPANESE.value: "すべてのトレイルでロギングが無効になっています。ロギングを有効にしてください。"
            },
            "warning": {
                LanguageCode.ENGLISH.value: "Logging is disabled for some trails. Please enable logging.",
                LanguageCode.KOREAN.value: "일부 Trail의 Logging 설정이 비활성화 되어있습니다. Logging을 활성화 해주세요.",
                LanguageCode.JAPANESE.value: "一部のトレイルでロギングが無効になっています。ロギングを有効にしてください。"
            },
            "success": {
                LanguageCode.ENGLISH.value: "Logging is enabled for all trails.",
                LanguageCode.KOREAN.value: "모든 Trail의 Logging 설정이 활성화 되어있습니다.",
                LanguageCode.JAPANESE.value: "すべてのトレイルでロギングが有効になっています。"
            },
            "describe_trails_error": {
                LanguageCode.ENGLISH.value: "Error occurred while describing trails.",
                LanguageCode.KOREAN.value: "트레일 설명을 가져오는 중 오류가 발생했습니다.",
                LanguageCode.JAPANESE.value: "トレイルの説明を取得中にエラーが発生しました。"
            },
            "get_trail_status_error": {
                LanguageCode.ENGLISH.value: "Error occurred while getting trail status.",
                LanguageCode.KOREAN.value: "트레일 상태를 가져오는 중 오류가 발생했습니다.",
                LanguageCode.JAPANESE.value: "トレイルの状態を取得中にエラーが発生しました。"
            }
        }
        return translations.get(key, {}).get(self.language, "Translation not available")

class TrustedAdvisorTranslator(BaseTranslator):
    def translate(self, key):
        translations = {
            "checking": {
                LanguageCode.ENGLISH.value: ">>> Checking Trusted Advisor settings",
                LanguageCode.KOREAN.value: ">>> TrustedAdvisor 설정 확인 중",
                LanguageCode.JAPANESE.value: ">>> Trusted Advisor設定を確認中"
            },
            "title": {
                LanguageCode.ENGLISH.value: "Enable Trusted Advisor",
                LanguageCode.KOREAN.value: "Trusted Advisor를 사용하도록 설정했는지 확인",
                LanguageCode.JAPANESE.value: "Trusted Advisorの有効化"
            },
            "info": {
                LanguageCode.ENGLISH.value: 'Please <a href="https://us-east-1.console.aws.amazon.com/trustedadvisor/home?region=ap-northeast-2#/preferences/manage-trusted-advisor" target="_blank" style="overflow:hidden;word-break:break-all;">check</a> if Trusted Advisor is enabled in your AWS account.',
                LanguageCode.KOREAN.value: '현재 계정의 Trusted Advisor 설정을 <a href="https://us-east-1.console.aws.amazon.com/trustedadvisor/home?region=ap-northeast-2#/preferences/manage-trusted-advisor" target="_blank" style="overflow:hidden;word-break:break-all;">확인</a>하세요.',
                LanguageCode.JAPANESE.value: 'AWSアカウントでTrusted Advisorが有効になっているかを<a href="https://us-east-1.console.aws.amazon.com/trustedadvisor/home?region=ap-northeast-2#/preferences/manage-trusted-advisor" target="_blank" style="overflow:hidden;word-break:break-all;">確認</a>してください。'
            },
            "error": {
                LanguageCode.ENGLISH.value: "An error occurred while checking Trust Advisor configuration.",
                LanguageCode.KOREAN.value: "Trust Advisor 구성을 확인하는 중 오류가 발생했습니다.",
                LanguageCode.JAPANESE.value: "Trust Advisor設定の確認中にエラーが発生しました。"
            }
        }
        return translations.get(key, {}).get(self.language, "Translation not available")
    
def get_translator(module_name, language):
    translators = {
        "main": MainTranslator,
        "root_mfa": RootMFASettingTranslator,
        "root_usage": RootUsageTranslator,
        "root_access_key": RootAccessKeyTranslator,
        "iam_user_mfa": IAMUserMFASettingTranslator,
        "iam_password_policy": IAMPasswordPolicyTranslator,
        "direct_attached_policy": IAMDirectAttachedPolicyTranslator,
        "alternate_contacts": AlternateContactTranslator,
        "trail_enabled": TrailEnabledTranslator,
        "multi_region_trail": MultiRegionTrailTranslator,
        "account_level_bucket_public_access": AccountLevelBucketPublicAccessTranslator,
        "bucket_public_access": BucketPublicAccessTranslator,
        "cloudwatch_alarm_configuration": CloudWatchAlarmConfigurationTranslator,
        "multi_region_instance_usage": MultiRegionInstanceUsageTranslator,
        "guardduty_enabled": GuardDutyEnabledTranslator,
        "trusted_advisor": TrustedAdvisorTranslator
    }
    translator_class = translators.get(module_name)
    if translator_class:
        return translator_class(language)
    else:
        raise ValueError(f"No translator found for module: {module_name}")