from django.db import models

class EnrolmentRatio(models.Model):
    academic_year = models.CharField(max_length=9)  # e.g. 2018-19

    sanctioned_intake = models.IntegerField()  # N
    first_year_admitted = models.IntegerField()  # N1
    lateral_entry = models.IntegerField(default=0)  # N2
    separate_division = models.IntegerField(default=0)  # N3

    total_admitted = models.IntegerField(editable=False)
    enrolment_ratio = models.FloatField(editable=False)

    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Auto calculation
        self.total_admitted = (
            self.first_year_admitted
            + self.lateral_entry
            + self.separate_division
        )

        if self.sanctioned_intake > 0:
            self.enrolment_ratio = (
                self.first_year_admitted / self.sanctioned_intake
            ) * 100
        else:
            self.enrolment_ratio = 0

        super().save(*args, **kwargs)

    def __str__(self):
        return self.academic_year
    
#4.1.1
class EnrolmentRatio4_1_1(models.Model):
    # Year label (optional)
    year_label = models.CharField(max_length=50, default="CAY (2023-24)")

    # CAY values
    N1 = models.IntegerField(default=0)
    N2 = models.IntegerField(default=0)
    N  = models.IntegerField(default=0)

    # CAY m1 values
    N1_m1 = models.IntegerField(default=0)
    N2_m1 = models.IntegerField(default=0)
    N_m1  = models.IntegerField(default=0)

    # CAY m2 values
    N1_m2 = models.IntegerField(default=0)
    N2_m2 = models.IntegerField(default=0)
    N_m2  = models.IntegerField(default=0)

    def __str__(self):
        return "Table 4.1.1 Average Enrolment Ratio"  

#4.1.2
from django.db import models

class EnrolmentRatioMarksOnly4_1_2(models.Model):
    marks_90 = models.IntegerField(default=20)   # >=90%
    marks_80 = models.IntegerField(default=18)   # >=80%
    marks_70 = models.IntegerField(default=16)   # >=70%
    marks_60 = models.IntegerField(default=12)   # >=60%
    marks_50 = models.IntegerField(default=8)    # >=50%
    marks_below_50 = models.IntegerField(default=0)  # <50%

    def __str__(self):
        return "Table 4.1.2 Marks"
  

#4.2
class SuccessRateStipulatedPeriod(models.Model):
    year_of_entry = models.CharField(max_length=20)   # Example: 2018-19
    n1_n2_n3_total = models.IntegerField()

    passed_year_1 = models.IntegerField(null=True, blank=True)
    passed_year_2 = models.IntegerField(null=True, blank=True)
    passed_year_3 = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.year_of_entry

#4.3    
class studentspassedwithbacklogs(models.Model):
    year_of_entry = models.CharField(max_length=20)   # Example: 2018-19
    n1_n2_n3_total = models.IntegerField()

    passed_year_1 = models.IntegerField(null=True, blank=True)
    passed_year_2 = models.IntegerField(null=True, blank=True)
    passed_year_3 = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.year_of_entry