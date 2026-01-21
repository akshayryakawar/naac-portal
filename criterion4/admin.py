from django.contrib import admin
from .models import EnrolmentRatio
from django.contrib import admin


@admin.register(EnrolmentRatio)
class EnrolmentRatioAdmin(admin.ModelAdmin):
    list_display = (
        'academic_year',
        'sanctioned_intake',
        'first_year_admitted',
        'lateral_entry',
        'separate_division',
        'total_admitted',
        'enrolment_ratio',
    )

#4.1.1
from .models import EnrolmentRatio4_1_1
@admin.register(EnrolmentRatio4_1_1)
class EnrolmentRatioAdmin1(admin.ModelAdmin):
    list_display = (
        "id",
        "total_cay", "ratio_cay",
        "total_m1", "ratio_m1",
        "total_m2", "ratio_m2",
        "average_enrolment",
    )

    # ---------- TOTALS ----------
    def total_cay(self, obj):
        return obj.N1 + obj.N2
    total_cay.short_description = "Total (CAY)"

    def total_m1(self, obj):
        return obj.N1_m1 + obj.N2_m1
    total_m1.short_description = "Total (CAY m1)"

    def total_m2(self, obj):
        return obj.N1_m2 + obj.N2_m2
    total_m2.short_description = "Total (CAY m2)"


    # ---------- RATIOS ----------
    def ratio_cay(self, obj):
        if obj.N == 0:
            return 0
        return round(((obj.N1 + obj.N2) / obj.N) * 100, 2)
    ratio_cay.short_description = "Enrolment Ratio (CAY %)"

    def ratio_m1(self, obj):
        if obj.N_m1 == 0:
            return 0
        return round(((obj.N1_m1 + obj.N2_m1) / obj.N_m1) * 100, 2)
    ratio_m1.short_description = "Enrolment Ratio (m1 %)"

    def ratio_m2(self, obj):
        if obj.N_m2 == 0:
            return 0
        return round(((obj.N1_m2 + obj.N2_m2) / obj.N_m2) * 100, 2)
    ratio_m2.short_description = "Enrolment Ratio (m2 %)"


    # ---------- AVERAGE ----------
    def average_enrolment(self, obj):
        r1 = self.ratio_cay(obj)
        r2 = self.ratio_m1(obj)
        r3 = self.ratio_m2(obj)
        return round((r1 + r2 + r3) / 3, 2)
    average_enrolment.short_description = "Average Enrolment"

#4.1.1
from .models import EnrolmentRatioMarksOnly4_1_2

@admin.register(EnrolmentRatioMarksOnly4_1_2)
class EnrolmentRatioMarksOnlyAdmin(admin.ModelAdmin):
    list_display = (
        "marks_90", "marks_80", "marks_70",
        "marks_60", "marks_50", "marks_below_50"
    )

from .models import SuccessRateStipulatedPeriod
@admin.register(SuccessRateStipulatedPeriod)
class SuccessRateStipulatedPeriodAdmin(admin.ModelAdmin):
    list_display = (
        "year_of_entry", 
        "n1_n2_n3_total",
        "passed_year_1", 
        "passed_year_2", 
        "passed_year_3"
                    )
    
from .models import studentspassedwithbacklogs
@admin.register(studentspassedwithbacklogs)
class studentspassedwithbacklogsAdmin(admin.ModelAdmin):
    list_display = (
        "year_of_entry", 
        "n1_n2_n3_total",
        "passed_year_1", 
        "passed_year_2", 
        "passed_year_3"
                    )