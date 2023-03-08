# What is a Security Baseline Self-Test Script?
> [공동 책임 모델](https://aws.amazon.com/ko/compliance/shared-responsibility-model/?nc1=h_ls)에 따라 AWS와 고객은 클라우드 보안에 대한 공동의 책임을 지닙니다. AWS는 클라우드에서 제공되는 모든 서비스를 실행하는 소프트웨어와 하드웨어를 포함한 인프라를 보호할 책임이 있습니다. 반면 고객은 이용하는 AWS 클라우드 서비스에서의 보안을 구성하고 관리할 책임을 가집니다.<br><br>
> Security Baseline Self-Test Script은 사용중인 `AWS 계정의 가장 기본적인 보안권고 사항에 대한 설정을 점검`하고, 그 `결과를 리포트로 제공`하는 Script 입니다.
<br><br>
사용자는 Script를 실행시켜 간단하게 AWS 계정에 대한 보안 점검을 진행할 수 있으며, AWS 계정 보안과 워크로드 보안 등 15가지 항목들의 점검 결과를 확인하실 수 있습니다.

<br>

# Who needs this Script?
> 자신이 현재 사용하는 AWS 계정에 대한 보안권고 준수 상황을 간단하게 점검하고 싶은 고객이라면 누구나 사용하실 수 있습니다. 특히 AWS 를 처음 사용하는 분이나, 자신의 워크로드를 AWS 에서 구현하고 싶은 분에게 사용을 추천드립니다. 
<br><br>
또한 점검 리포트에는 적은 리소스로 AWS 보안 위협에 효과적으로 대처할 수 있는 방법들에 대해서도 안내하고 있으니, 보안에 많은 리소스를 투자하기 어려운 초기 스타트업에서도 이 Script 을 활용할 수 있습니다.

<br>

# How can I start this script?

### [ 사전 준비 ]

<br>

> - python3 설치
> - git 설치
> - [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) 설치

### [점검 권한을 가진 IAM 계정 생성]
<br>

> 먼저 점검을 하고자 하는 계정에서 [IAM 사용자를 생성](https://docs.aws.amazon.com/ko_kr/IAM/latest/UserGuide/id_users_create.html#id_users_create_console)합니다. 
>
> IAM 사용자의 권한은 [permission.json](./permission.json) 파일을 참고하여 추가해주시기 바랍니다.
>
> IAM 사용자가 생성되면 해당 IAM 사용자 상세정보 페이지에서 Security credentials 탭을 선택하고 "Create access key"를 눌러 Access key를 만들어주세요. <br>[[IAM 사용자 Access Key 생성](https://docs.aws.amazon.com/ko_kr/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)]
>
> AWS CLI가 설치된 환경에서 [AWS CLI의 자격 증명 파일을 설정](https://docs.aws.amazon.com/ko_kr/cli/latest/userguide/cli-configure-files.html)해주시기 바랍니다.

<br>

### [Python 실행환경 구성]
> 먼저 git clone 명령을 사용하여 스크립트를 다운로드 받아주세요.
```bash
git clone https://github.com/aws-samples/security-baseline-self-test.git
```

> 아래 명령어를 실행하여 스크립트를 실행할 가상 환경을 만들어주세요.<br>
```bash
python3 -m venv ssb-env
```
> 가상환경이 생성되면, 아래의 명령을 실행하여 가상환경을 활성화해주시기 바랍니다.<br>
> 
> [windows]
```bash
ssb-env\Scripts\activate.bat
```
> [Unix 또는 MacOS]
```bash
source ssb-env/bin/activate
```
> 가상환경이 활성화되면 아래의 명령을 실행하여 스크립트 실행에 필요한 패키지를 설치해주시기 바랍니다.<br>
```bash
python -m pip install -r requirements.txt
```

### [스크립트 실행]
> 다운받은 스크립트의 [sst](./sst) 디랙토리 내의 main.py 를 실행합니다.
```bash
cd sst
python3 main.py
```
> AWS CLI의 자격 증명 파일 설정시 프로파일 명을 지정했다면, 해당 프로파일명을 아래와 같이 실행인자로 넣어 스크립트를 실행할 수도 있습니다.
```bash
python3 main.py security-test
```
> 스크립트를 실행하면 언어를 선택합니다.<br>
> 현재 영어와 한국어를 지원합니다.<br>
> 점검이 끝나면 sst 디렉토리 내에 생성된 html 형식의 결과 리포트를 확인합니다.

### [ Report Sample ]

> ![report_sample](./images/report_sample.png)<br><br>

# FAQ
> *- 보안 수준을 향상시키기 위해 더 많은 항목을 점검하려면 어떻게 해야 하나요?*<br>
> 더 많은 AWS 계정의 보안 설정을 점검하시고 싶은 경우 [AWS Trusted Advisor](https://aws.amazon.com/ko/blogs/korea/aws-trusted-advisor-new-priority-capability/) 를 사용하시면 좋습니다. AWS Trusted Advisors는 AWS 계정을 지속적으로 분석하고 AWS 보안 모범 사례 및 AWS Well-Architected 가이드라인을 따르는데 도움이 되는 서비스입니다. 따라서 AWS Trusted Advisor 를 통해 Security 진단 항목을 관리하시면 AWS 계정의 보안 수준을 향상시킬 수 있습니다.
>
> <br>
>
> *- AWS 보안 수준을 향상시키기 위한 추가 정보나 가이드라인을 알고 싶은 경우 어떻게 하면 좋을까요?*<br>
> AWS 에서는 AWS 모범사례를 사용하여 아키텍처를 측정하기 위한 일관된 프로세스를 제공하는 클라우드 서비스로 [AWS Well-Architected Tool](https://docs.aws.amazon.com/ko_kr/wellarchitected/latest/userguide/intro.html) 을 제공하고 있습니다. 보안 수준을 향상시키기 위한 추가 정보나 가이드라인이 필요하신 경우 AWS Well Architected Tool 의 Security pillar 를 기반으로 보안 모범사례를 참고하여 아키텍처 설계 및 진단을 하실 수 있습니다.