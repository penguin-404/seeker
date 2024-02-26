from django.contrib import admin
from .models import User,Company,Applicant,job_post,Bid
admin.site.register(User)
admin.site.register(Company)
admin.site.register(Applicant)
admin.site.register(job_post)
admin.site.register(Bid)