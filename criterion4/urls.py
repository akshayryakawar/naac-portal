from django.urls import path
from .views import criterion4_home, enrolment_ratio_pdf
from .views import enrolment_ratio_pdf_4_1
from .views import success_rate_nobacklog_pdf
from .views import students_passed_with_backlogs_pdf

urlpatterns = [
    path("", criterion4_home, name="criterion4_home"),
    path("4-1-enrolment-ratio/", enrolment_ratio_pdf, name="enrolment_ratio_pdf"),
    path("enrolment_ratio_pdf_4_1/", enrolment_ratio_pdf_4_1, name="enrolment_ratio_pdf_4_1"),
    path("4-2-success-rate-no-backlog/", success_rate_nobacklog_pdf, name="success_rate_nobacklog_pdf"),
    path("4-3-success-rate-no-backlog/", students_passed_with_backlogs_pdf, name="students_passed_with_backlogs_pdf"),
    
]
