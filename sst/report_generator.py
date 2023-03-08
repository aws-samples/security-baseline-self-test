from checklist import *
from lib import level_const, language
import datetime

def initialize_html():
    return '''<!DOCTYPE html>
                    <html lang="en">'''

def write_header():
    return '''<head>
    <meta charset="UTF-8">
    </meta>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    </meta>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet">
    </link>
    <title>Report</title>
    </head>'''

def initialize_body():
    return '''<body>
    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
        <symbol id="check-circle-fill" fill="currentColor" viewBox="0 0 16 16">
            <path
                d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z">
            </path>
        </symbol>
        <symbol id="info-fill" fill="currentColor" viewBox="0 0 16 16">
            <path
                d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z">
            </path>
        </symbol>
        <symbol id="exclamation-triangle-fill" fill="currentColor" viewBox="0 0 16 16">
            <path
                d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z">
            </path>
        </symbol>
        <symbol id="bi-x-circle-fill" fill="currentColor" viewBox="0 0 16 16">
            <path 
                d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293 5.354 4.646z">
            </path>
        </symbol>
        <symbol id="bi-dash-circle" fill="currentColor" viewBox="0 0 16 16">
            <path 
                d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z">
            </path>
            <path 
                d="M4 8a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7A.5.5 0 0 1 4 8z">
            </path>
        </symbol>
    </svg> 
    '''

def write_report_base_info(account_id, datetime):
    html = '''
        <div class="container">
        <div class="row">
            <div class="col"></div>
            <div class="col-9">
                <br>
                <h1 class="text-center">Security Baseline Self-Test Report</h1>
                <br>
                <div class="row">
                    <div class="col"></div>
                    <div class="col">
                        <table class="table"><tr><td>Account</td><td>{account_id}</td></tr><tr><td>Generated At</td><td>{datetime}</td></tr></table>
                    </div>
                </div>'''.format(account_id=account_id, datetime=str(datetime))

    return html

def write_overview(result):

    danger_count = str(len(result[level_const.danger]))
    warning_count = str(len(result[level_const.warning]))
    success_count = str(len(result[level_const.success]))
    error_count = str(len(result[level_const.error]))
    info_count = str(len(result[level_const.info]))

    html = '''
                    <div class="row">
                    <div class="card">
                        <div class="card-body">
                            <div class="card-title">
                                <b>Overview</b>
                            </div>
                            <div class="row">
                                <div class="col">
                                    <div class="alert alert-danger">
                                        <div class="d-flex align-items-center justify-content-around">
                                            <h1><a href="#danger-list" class="link-danger">{number_of_danger}</a></h1>
                                        </div> 
                                        <div class="row align-items-center justify-content-center h6">DANGER</div>
                                    </div>
                                </div>
                                <div class="col">
                                    <div class="alert alert-warning">
                                        <div class=" d-flex align-items-center justify-content-around">
                                            <h1><a href="#warning-list" class="link-warning">{number_of_warning}</a></h1>
                                        </div>
                                        <div class="row align-items-center justify-content-center h6">WARNING</div>
                                    </div>
                                </div>
                                <div class="col">
                                    <div class="alert alert-success">
                                        <div class="d-flex align-items-center justify-content-around">
                                            <h1><a href="#success-list" class="link-success">{number_of_success}</a></h1>
                                        </div> 
                                        <div class="row align-items-center justify-content-center h6">SUCCESS</div>
                                    </div>
                                </div>
                                <div class="col">
                                    <div class="alert alert-primary">
                                        <div class="d-flex align-items-center justify-content-around">
                                            <h1><a href="#info-list" class="link-primary">{number_of_info}</a></h1>
                                        </div> 
                                        <div class="row align-items-center justify-content-center h6">INFO</div>
                                    </div>
                                </div>
                                <div class="col">
                                    <div class="alert alert-dark">
                                        <div class="d-flex align-items-center justify-content-around">
                                        <h1><a href="#failed-list" class="link-secondary">{number_of_error}</a></h1>
                                        </div>
                                        <div class="row align-items-center justify-content-center h6">FAILED</div>
                                    </div>
                                </div>
                            </div>  
                        </div>
                    </div>
                </div><br>'''.format(number_of_danger=danger_count, number_of_warning=warning_count, number_of_success=success_count, number_of_info=info_count, number_of_error=error_count)

    return html


def write_danger_result(result, item_number) -> tuple:
    if len(result[level_const.danger]) == 0:
        return item_number, ''
    else:
        html = '''
                    <div class="row">
                        <div class="card">
                            <div class="card-body" id="danger-list">
                                <div class="accordion" id="accordionPanelsStayOpenExample">
                '''

        items = ''

        for result_detail in result[level_const.danger]:

            item_number += 1
            title = result_detail.title
            msg = result_detail.msg

            cols = result_detail.result_cols
            rows = result_detail.result_rows

            table_html = ''

            if len(rows) == 0:
                pass
            else:
                table_html = '''<table class="table">'''
                for col in cols:
                    table_html+='''<th scope="col">{col}</th>'''.format(col=str(col))
                for row in rows:
                    table_html+='''<tr>'''
                    for data in row:
                        table_html+='''<td>{data}</td>'''.format(data=str(data))
                    table_html+='''</tr>'''
                table_html+='''</table>'''

            items += '''

                                        <div class="accordion-item">
                                        <h2 class="accordion-header" id="panelsStayOpen-heading{item_number}">
                                            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#panelsStayOpen-collapse{item_number}" aria-expanded="true" aria-controls="panelsStayOpen-collapse{item_number}">
                                                <span class="badge text-bg-danger rounded-pill">Danger</span>
                                                <div class="ms-2 me-auto">{title}</div>
                                            </button>
                                        </h2>
                                        <div id="panelsStayOpen-collapse{item_number}" class="accordion-collapse collapse" aria-labelledby="panelsStayOpen-heading{item_number}">
                                            <div class="accordion-body">
                                    
                                                <div class="alert alert-danger d-flex align-items-center" role="alert">
                                                    <svg aria-label="Danger:" class="bi flex-shrink-0 me-2" width="24" height="24" role="img">
                                                        <use xlink:href="#exclamation-triangle-fill"></use>
                                                    </svg>
                                                    <span>{msg}</span>
                                                </div>
                                                {table_html}
                                            </div>
                                        </div>
                                    </div>'''.format(item_number=str(item_number).zfill(2), title=title, msg=msg, table_html=table_html)
        html += items
        html += '''</div>
                </div>
            </div>
            </div>
            <br>'''

        return item_number, html

def write_warning_result(result, item_number) -> tuple:
    if len(result[level_const.warning]) == 0:
        return item_number, ''
    else:
        html = '''
                    <div class="row">
                        <div class="card">
                            <div class="card-body" id="warning-list">
                                <div class="accordion" id="accordionPanelsStayOpenExample">
                '''

        items = ''

        for result_detail in result[level_const.warning]:

            item_number += 1
            title = result_detail.title
            msg = result_detail.msg

            cols = result_detail.result_cols
            rows = result_detail.result_rows

            table_html = ''

            if len(rows) == 0:
                pass
            else:
                table_html = '''<table class="table">'''
                for col in cols:
                    table_html+='''<th scope="col">{col}</th>'''.format(col=str(col))
                for row in rows:
                    table_html+='''<tr>'''
                    for data in row:
                        table_html+='''<td>{data}</td>'''.format(data=str(data))
                    table_html+='''</tr>'''
                table_html+='''</table>'''

            items += '''

                                        <div class="accordion-item">
                                        <h2 class="accordion-header" id="panelsStayOpen-heading{item_number}">
                                            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#panelsStayOpen-collapse{item_number}" aria-expanded="true" aria-controls="panelsStayOpen-collapse{item_number}">
                                                <span class="badge text-bg-warning rounded-pill">Warning</span>
                                                <div class="ms-2 me-auto">{title}</div>
                                            </button>
                                        </h2>
                                        <div id="panelsStayOpen-collapse{item_number}" class="accordion-collapse collapse" aria-labelledby="panelsStayOpen-heading{item_number}">
                                            <div class="accordion-body">
                                    
                                                <div class="alert alert-warning d-flex align-items-center" role="alert">
                                                    <svg aria-label="Warning:" class="bi flex-shrink-0 me-2" width="24" height="24" role="img">
                                                        <use xlink:href="#exclamation-triangle-fill"></use>
                                                    </svg>
                                                    <span>{msg}</span>
                                                </div>
                                                {table_html}
                                            </div>
                                        </div>
                                    </div>'''.format(item_number=str(item_number).zfill(2), title=title, msg=msg, table_html=table_html)
        html += items
        html += '''</div>
                </div>
            </div>
            </div>
            <br>'''

        return item_number, html

def write_success_result(result, item_number) -> tuple:

    if len(result[level_const.success]) == 0:
        return item_number, ''
    else:
        html = '''
                    <div class="row">
                        <div class="card">
                            <div class="card-body" id="success-list">
                                <div class="accordion" id="accordionPanelsStayOpenExample">
                '''

        items = ''

        for result_detail in result[level_const.success]:

            item_number += 1
            title = result_detail.title
            msg = result_detail.msg

            cols = result_detail.result_cols
            rows = result_detail.result_rows

            table_html = ''

            if len(rows) == 0:
                pass
            else:
                table_html = '''<table class="table">'''
                for col in cols:
                    table_html+='''<th scope="col">{col}</th>'''.format(col=str(col))
                for row in rows:
                    table_html+='''<tr>'''
                    for data in row:
                        table_html+='''<td>{data}</td>'''.format(data=str(data))
                    table_html+='''</tr>'''
                table_html+='''</table>'''

            items += '''

                                        <div class="accordion-item">
                                        <h2 class="accordion-header" id="panelsStayOpen-heading{item_number}">
                                            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#panelsStayOpen-collapse{item_number}" aria-expanded="true" aria-controls="panelsStayOpen-collapse{item_number}">
                                                <span class="badge text-bg-success rounded-pill">Success</span>
                                                <div class="ms-2 me-auto">{title}</div>
                                            </button>
                                        </h2>
                                        <div id="panelsStayOpen-collapse{item_number}" class="accordion-collapse collapse" aria-labelledby="panelsStayOpen-heading{item_number}">
                                            <div class="accordion-body">
                                    
                                                <div class="alert alert-success d-flex align-items-center" role="alert">
                                                    <svg aria-label="Success:" class="bi flex-shrink-0 me-2" width="24" height="24" role="img">
                                                        <use xlink:href="#check-circle-fill"></use>
                                                    </svg>
                                                    <span>{msg}</span>
                                                </div>
                                                {table_html}
                                            </div>
                                        </div>
                                    </div>'''.format(item_number=str(item_number).zfill(2), title=title, msg=msg, table_html=table_html)
        html += items
        html += '''</div>
                </div>
            </div>
            </div>
            <br>'''

        return item_number, html

def write_info_result(result, item_number) -> tuple:

    if len(result[level_const.info]) == 0:
        return item_number, ''
    else:
        html = '''
                    <div class="row">
                        <div class="card">
                            <div class="card-body" id="info-list">
                                <div class="accordion" id="accordionPanelsStayOpenExample">
                '''

        items = ''

        for result_detail in result[level_const.info]:

            item_number += 1
            title = result_detail.title
            msg = result_detail.msg

            cols = result_detail.result_cols
            rows = result_detail.result_rows

            table_html = ''

            if len(rows) == 0:
                pass
            else:
                table_html = '''<table class="table">'''
                for col in cols:
                    table_html+='''<th scope="col">{col}</th>'''.format(col=str(col))
                for row in rows:
                    table_html+='''<tr>'''
                    for data in row:
                        table_html+='''<td>{data}</td>'''.format(data=str(data))
                    table_html+='''</tr>'''
                table_html+='''</table>'''

            items += '''

                                        <div class="accordion-item">
                                        <h2 class="accordion-header" id="panelsStayOpen-heading{item_number}">
                                            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#panelsStayOpen-collapse{item_number}" aria-expanded="true" aria-controls="panelsStayOpen-collapse{item_number}">
                                                <span class="badge text-bg-primary rounded-pill">Info</span>
                                                <div class="ms-2 me-auto">{title}</div>
                                            </button>
                                        </h2>
                                        <div id="panelsStayOpen-collapse{item_number}" class="accordion-collapse collapse" aria-labelledby="panelsStayOpen-heading{item_number}">
                                            <div class="accordion-body">
                                    
                                                <div class="alert alert-primary d-flex align-items-center" role="alert">
                                                    <svg aria-label="Info:" class="bi flex-shrink-0 me-2" width="24" height="24" role="img">
                                                        <use xlink:href="#info-fill"></use>
                                                    </svg>
                                                    <span>{msg}</span>
                                                </div>
                                                {table_html}
                                            </div>
                                        </div>
                                    </div>'''.format(item_number=str(item_number).zfill(2), title=title, msg=msg, table_html=table_html)
        html += items
        html += '''</div>
                </div>
            </div>
            </div>
            <br>'''

    return item_number, html

def write_error_result(result, item_number) -> tuple:
    html = '''
                <div class="row">
                    <div class="card">
                        <div class="card-body" id="failed-list">
                            <div class="accordion" id="accordionPanelsStayOpenExample">
            '''

    items = ''

    if len(result[level_const.error]) == 0:
        items = '''
                    <div class="accordion-item">
                <h2 class="accordion-header" id="panelsStayOpen-heading{item_number}">
                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#panelsStayOpen-collapse{item_number}" aria-expanded="true" aria-controls="panelsStayOpen-collapse{item_number}">
                    <span class="badge text-bg-dark rounded-pill">Failed</span>
                    <div class="ms-2 me-auto">Test Failed Items</div>
                </button>
                </h2>
                <div id="panelsStayOpen-collapse{item_number}" class="accordion-collapse collapse" aria-labelledby="panelsStayOpen-heading{item_number}">
                <div class="accordion-body">
        
                    <div class="alert alert-primary d-flex align-items-center" role="alert">
                        <svg aria-label="Failed:" class="bi flex-shrink-0 me-2" width="24" height="24" role="img">
                            <use xlink:href="#info-fill"></use>
                        </svg>
                        <span>No Item<span>
                    </div>
                </div>
            </div>
        </div>'''.format(item_number=str(item_number+1).zfill(2))
    else:
        for result_detail in result[level_const.error]:

            item_number += 1
            title = result_detail.title
            msg = result_detail.msg

            cols = result_detail.result_cols
            rows = result_detail.result_rows

            table_html = ''

            if len(rows) == 0:
                pass
            else:
                table_html = '''<table class="table">'''
                for col in cols:
                    table_html+='''<th scope="col">{col}</th>'''.format(col=str(col))
                for row in rows:
                    table_html+='''<tr>'''
                    for data in row:
                        table_html+='''<td>{data}</td>'''.format(data=str(data))
                    table_html+='''</tr>'''
                table_html+='''</table>'''

            items += '''
                        <div class="accordion-item">
                        <h2 class="accordion-header" id="panelsStayOpen-heading{item_number}">
                            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#panelsStayOpen-collapse{item_number}" aria-expanded="true" aria-controls="panelsStayOpen-collapse{item_number}">
                                <span class="badge text-bg-dark rounded-pill">Failed</span>
                                <div class="ms-2 me-auto">{title}</div>
                            </button>
                        </h2>
                        <div id="panelsStayOpen-collapse{item_number}" class="accordion-collapse collapse" aria-labelledby="panelsStayOpen-heading{item_number}">
                            <div class="accordion-body">
                    
                                <div class="alert alert-dark d-flex align-items-center" role="alert">
                                    <svg aria-label="Failed:" class="bi flex-shrink-0 me-2" width="24" height="24" role="img">
                                        <use xlink:href="#bi-x-circle-fill"></use>
                                    </svg>
                                    <span>{msg}</span>
                                </div>
                                {table_html}
                            </div>
                        </div>
                    </div>'''.format(item_number=str(item_number).zfill(2), title=title, msg=msg, table_html=table_html)
    html += items
    html += '''</div>
            </div>
        </div>
        </div>
        <br>'''

    return item_number, html

def finalize_html_korean():
    return '''
                <div class="row">
                <div class="alert alert-primary d-flex align-items-center" role="alert"><svg aria-label="Info:"
                        class="bi flex-shrink-0 me-2" width="24" height="24" role="img">
                        <use xlink:href="#info-fill"></use>
                    </svg>
                    <span>계정 보안을 위한 추가적인 사항은&nbsp[<a href="https://www.awsstartup.io/security/network-security/aws-tip" target="_blank" style="overflow:hidden;word-break:break-all;">계정 안전하게 지키기 Tip</a>]&nbsp을 참고해주세요.</span>
                </div>
                </div>
                <div class="row">
                <div class="alert alert-primary d-flex align-items-center" role="alert"><svg aria-label="Info:"
                        class="bi flex-shrink-0 me-2" width="24" height="24" role="img">
                        <use xlink:href="#info-fill"></use>
                    </svg>
                    <span><a href="https://aws.amazon.com/ko/blogs/korea/aws-trusted-advisor-new-priority-capability/" target="_blank" style="overflow:hidden;word-break:break-all;">AWS Trusted Advisor</a>는 지속적으로 AWS 계정에 대한 비용 절감, 가용성 및 성능 향상, 보안 개선을 위한 정보를 고객에게 제공합니다.</span>
                </div>
                </div>
                <div class="row">
                <div class="alert alert-primary d-flex align-items-center" role="alert"><svg aria-label="Info:"
                        class="bi flex-shrink-0 me-2" width="24" height="24" role="img">
                        <use xlink:href="#info-fill"></use>
                    </svg>
                    <span>AWS Trusted Advisor 사용 방법에 대한 자세한 내용은 <a href="https://aws.amazon.com/ko/premiumsupport/knowledge-center/trusted-advisor-intro/" target="_blank" style="overflow:hidden;word-break:break-all;">여기</a>를 눌러 확인해주세요.</span>
                </div>
                </div>
            </div>
            <div class="col"></div>
        </div>
        </div>
        <script>
            function click_summary(x){
                if(x.className === "accordion-button collapsed"){
                    x.click()
                }
            }
        
        </script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/js/bootstrap.bundle.min.js"></script>
    </body>

    </html>'''

def finalize_html_english():
    return '''
                <div class="row">
                <div class="alert alert-primary d-flex align-items-center" role="alert"><svg aria-label="Info:"
                        class="bi flex-shrink-0 me-2" width="24" height="24" role="img">
                        <use xlink:href="#info-fill"></use>
                    </svg>
                    <span><a href="https://aws.amazon.com/blogs/aws/aws-trusted-advisor-new-priority-capability/" target="_blank" style="overflow:hidden;word-break:break-all;">AWS Trusted Advisor</a> is a service that continuously analyzes your AWS accounts and provides recommendations to help you to follow AWS best practices and AWS Well-Architected guidelines.</span>
                </div>
                </div>
                <div class="row">
                <div class="alert alert-primary d-flex align-items-center" role="alert"><svg aria-label="Info:"
                        class="bi flex-shrink-0 me-2" width="24" height="24" role="img">
                        <use xlink:href="#info-fill"></use>
                    </svg>
                    <span>Please <a href="https://aws.amazon.com/premiumsupport/knowledge-center/trusted-advisor-intro/?nc1=h_ls" target="_blank" style="overflow:hidden;word-break:break-all;">click</a> this link whether you want to know more details about AWS Trusted Advisor.</span>
                </div>
                </div>
            </div>
            <div class="col"></div>
        </div>
        </div>
        <script>
            function click_summary(x){
                if(x.className === "accordion-button collapsed"){
                    x.click()
                }
            }
        
        </script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/js/bootstrap.bundle.min.js"></script>
    </body>

    </html>'''

def generate_html_report(account_id_str, result_sort_by_level, selected_language):
    
    generated_at = datetime.datetime.now().strftime("(UTC) %Y-%m-%d %H:%M:%S")

    html_report = initialize_html()
    html_report += write_header()
    html_report += initialize_body()
    html_report += write_report_base_info(account_id_str, generated_at)
    html_report += write_overview(result_sort_by_level)

    item_index = 0
    item_index, danger_html = write_danger_result(result_sort_by_level, item_index)
    item_index, warning_html = write_warning_result(result_sort_by_level, item_index)
    item_index, success_html = write_success_result(result_sort_by_level, item_index)
    item_index, info_html = write_info_result(result_sort_by_level, item_index)
    item_index, error_html = write_error_result(result_sort_by_level, item_index)

    html_report += danger_html + warning_html + success_html + info_html + error_html
    if selected_language == language.LANGUAGE_CODE.ENGLISH.value:
        html_report += finalize_html_english()
    elif selected_language == language.LANGUAGE_CODE.KOREAN.value:
        html_report += finalize_html_korean()

    return html_report