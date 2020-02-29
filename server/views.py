from datetime import datetime
from django.db.models import Count
from django.shortcuts import render,redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.core.files.base import ContentFile
from .models import Patient,Appointment,Clinic
from .tests import Text_email,send_no_result,send_ok_result,send_report_upload,send_requirement
from .sql import *
import json
def redirect_to_login():
    return HttpResponseRedirect(reverse("signin"))

class SignInView(View):
    def get(self, req):
        return render(req, 'signin.html')
    def post(self, req):
        role = req.POST.get('role', None)
        email = req.POST.get('email', None)
        error = []
        password = req.POST.get('password', None)
        if role == "patient":
            if Patient.objects.filter(Email=email, Password=password):
                p = Patient.objects.filter(Email=email, Password=password)[0]
                req.session['user'] = {
                    "id":p.PatientID,
                    "email": p.Email,
                    "name": p.Last_name,
                    "role": role,
                }
                return HttpResponseRedirect(reverse("home"))
            else:
                error.append("Account or password is wrong！")
                return render(req, 'signin.html', {"error": error})
        else:
            if Clinic.objects.filter(Email=email, Password=password):
                p = Clinic.objects.filter(Email=email, Password=password)[0]
                req.session['clinic_user'] = {
                    "id":p.ClinicID,
                    "email": p.Email,
                    "name": p.ClinicName,
                    "role": role
                }
                return HttpResponseRedirect(reverse("home"))
            else:
                error.append("Account or password is wrong！")
                return render(req, 'signin.html', {"error": error})

class ClinicDashBoardView(View):
    def get(self, req):
        if req.session['clinic_user']:
            clinic_user = req.session['clinic_user']
            clinic_id=clinic_user['id']
            query_set = Appointment.objects.filter(ClinicID = clinic_id, Status = 'Approved').values()
            for query in query_set:
                print("dashboardview","query",query)
                patient_id = query['PatientID']
                patient_info = Patient.objects.filter(PatientID = patient_id).values('Email','First_name','Last_name')
                print("patient_info",patient_info)
                query.update(patient_info[0])
            pending_count = Appointment.objects.filter(ClinicID = clinic_id, Status = 'Pending').count()
            # query_set = list(query_set)
            context = {
                "query_set":query_set,
                "pending_count":pending_count,
            }
            return render(req, 'clinic/dashboard.html', context)
        else:
            return HttpResponseRedirect(reverse('signin'))


class SignUpView(View):
    role = "patient"
    req = None
    error = []
    def get_role(self):
        role = self.req.GET.get("role", None)
        if role:
            self.role = role
        return self.role
    def get_tempt(self):
        self.get_role()
        if self.role == "doc":
            tempt = "clinic/clinic_signup.html"
        else:
            tempt = 'patient/patient_signup.html'
        return tempt
    def get(self, req):
        self.req = req
        tempt = self.get_tempt()
        return render(req, tempt)
    def post(self, req):
        self.req = req
        role = self.get_role()
        tempt = self.get_tempt()
        if role == "patient":
            if self.create_user(Patient):
                return HttpResponseRedirect(reverse('signin'))
        else:
            signup_dict= {'Email':'','Password':'','ClinicName':'', 'Address':'','ZipCode':'', 'Contact':'','X_Ray':'','ChildrenImage':'','CT':'','MRI':'','WomenProcedure':''}
            examination_fields = ['X_Ray','ChildrenImage','CT','MRI','WomenProcedure']
            examinations = req.POST.getlist('examinations[]')
            for key in signup_dict:
                if key in examination_fields:
                    if key in examinations:
                        signup_dict[key] = '1'
                    else:
                        signup_dict[key] = '0'
                else:
                    signup_dict[key] = req.POST.get(key)
            
            clinic = Clinic(
                Email = signup_dict['Email'],
                Password = signup_dict['Password'],
                ClinicName = signup_dict['ClinicName'],
                Address = signup_dict['Address'],
                ZipCode = signup_dict['ZipCode'],
                Contact = signup_dict['Contact'],
                X_Ray = signup_dict['X_Ray'],
                ChildrenImage = signup_dict['ChildrenImage'],
                CT = signup_dict['CT'],
                WomenProcedure = signup_dict['WomenProcedure'],
                MRI = signup_dict['MRI'],
            )
            clinic.save()
            return HttpResponseRedirect(reverse('signin'))

    def create_user(self, model):
        data = self.req.POST
        obj = model()
        email = data.get("Email", None)
        if model.objects.filter(Email = email):
            self.error.append("Currently email has been registered！")
        else:
            for field in obj.get_fields_names()[1:]:
                value = data.get(field, None)
                if not value:
                    self.error.append("{} is invalid!".format(field))
                else:
                    setattr(obj, field, value)
        if not self.error:
            obj.save()
            return True
        else:
            return False

class LogoutView(View):
    def get(self, req):
        req.session['user'] = None
        req.session['clinic_user'] = None
        return HttpResponseRedirect(reverse('signin'))


class HomeView(View):
    def get(self, req):
        return render(req, 'home.html')

class ProfileView(View):
    error=[]
    req = None
    def get(self,req):
        if "user" in req.session.keys() and req.session['user']:
            user = req.session['user']
            user = Patient.objects.get(PatientID = user['id'])
            context = {
                "user": user,
                "error":self.error,
            }
            return render(req, 'patient/patient_profile.html', context)
        else:
            return HttpResponseRedirect(reverse('signin'))
    def post(self,req):
        self.req = req
        user = req.session['user']
        p_id = user["id"]
        patient = Patient.objects.get(PatientID = p_id)
        if self.test_verify(Patient,patient):
            for field in patient.get_fields_names()[3:]:
                value = req.POST.get(field, None)
                setattr(patient, field, value)
                patient.save()
        return HttpResponseRedirect(reverse('patient_profile'))

    def test_verify(self, model,query):
        email_field = {"old_email":"", "new_email":"","Email":""}
        for field in email_field:
            email_field[field] = self.req.POST.get(field, None)
        if "" not in email_field.values():
            if email_field["new_email"] == email_field["old_email"]:
                self.error.append("Please enter a different email")
            else:
                if email_field["Email"] != email_field["new_email"]:
                    self.error.append("Confirm email and new email does not match")
                else:
                    if model.objects.filter(Email = email_field["new_email"]):
                        self.error.append("Current email has been registered, please enter another email")
                    else:
                        query.Email = email_field["Email"]
        password_field = {"original_password":"","old_password":"", "new_password":"","Password":""}
        for field in password_field:
            password_field[field] = self.req.POST.get(field, None)
        if "" not in password_field.values():
            if password_field["old_password"] != password_field["original_password"]:
                self.error.append("Old password does not match")
            else:
                if password_field["new_password"] != password_field["Password"]:
                    self.error.append("Confirm password does not match")
                else:
                    if password_field["old_password"] == password_field["password"]:
                        self.error.append("Please enter a different new password")
                    else:
                        query.Passowrd = password_field["Password"]
        if not self.error:    
            query.save()
            self.error = []
            return True
        else:
            return False
#Patient Booking request history list
class PatientBookingView(View):
    def get(self, req):
        if "user" in req.session.keys() and req.session['user']:
            user = req.session['user']
            if user['role'] == "patient":
                patient_id = user["id"]
                user = Patient.objects.get(PatientID = patient_id)
                status = req.GET.get("status", "Any status")
                if status == "Any status":
                    bookings = Appointment.objects.filter(PatientID = patient_id).values()
                else:
                    bookings = Appointment.objects.filter(PatientID = patient_id, Status = status).values()
                count = bookings.count()
                for query in bookings:
                    clinic_id = query["ClinicID"]
                    clinic_info = Clinic.objects.filter(ClinicID = clinic_id).values("ClinicName", "Contact","Email")
                    query.update(clinic_info[0])
                context = {"user":user, "bookings":bookings, "count":count}
                return render(req, 'patient/bookings.html', context)
            else:
                return HttpResponseRedirect(reverse('signin'))
        else:
            return HttpResponseRedirect(reverse('signin'))
class ClinicProfileView(View):
    error=[]
    req = None
    def get(self,req):
        self.req = req
        if req.session['clinic_user']:
            clinic_user = req.session['clinic_user']
            clinic_id = clinic_user['id']
            result = Clinic.objects.get(ClinicID = clinic_id)
            examinations = list(Clinic.objects.filter(ClinicID = clinic_id).values('CT','MRI','X_Ray','ChildrenImage','WomenProcedure'))
            examinations = examinations[0]
            exam_dict = examinations.items()
            context = {"basic":result,
                        "exam_dict":exam_dict,
                        "error":self.error}
            return render(req, 'clinic/clinic_profile.html', context)
    def post(self,req):
        self.req = req
        clinic_user = req.session['clinic_user']
        clinic_id = clinic_user["id"]
        clinic = Clinic.objects.get(ClinicID = clinic_id)
        if self.test_verify(Clinic,clinic):
            for field in clinic.get_fields_names()[3:7]:
                value = req.POST.get(field, None)
                setattr(clinic, field, value)
                clinic.save()
            if clinic.Password == "":
                clinic.Password = self.req.POST.get("original_password")
                clinic.save()
            examinations = req.POST.getlist('examinations[]')
            for field in clinic.get_fields_names()[7:]:
                if field in examinations:
                    value = '1'
                    setattr(clinic, field, value)
                    clinic.save()
                else:
                    value = '0'
                    setattr(clinic, field, value)
                    clinic.save()
        return HttpResponseRedirect(reverse('clinic_profile'))

    def test_verify(self, model,query):
        email_field = {"old_email":"", "new_email":"","Email":""}
        for field in email_field:
            email_field[field] = self.req.POST.get(field, None)
        if "" not in email_field.values():
            if email_field["new_email"] == email_field["old_email"]:
                self.error.append("Please enter a different email")
            else:
                if email_field["Email"] != email_field["new_email"]:
                    self.error.append("Confirm email and new email does not match")
                else:
                    if model.objects.filter(Email = email_field["new_email"]):
                        self.error.append("Current email has been registered, please enter another email")
                    else:
                        query.Email = email_field["Email"]
        password_field = {"original_password":"","old_password":"", "new_password":"","Password":""}
        for field in password_field:
            password_field[field] = self.req.POST.get(field, None)
        if "" not in password_field.values():
            if password_field["old_password"] != password_field["original_password"]:
                self.error.append("Old password does not match")
            else:
                if password_field["new_password"] != password_field["Password"]:
                    self.error.append("Confirm password does not match")
                else:
                    if password_field["old_password"] == password_field["password"]:
                        self.error.append("Please enter a different new password")
                    else:
                        query.Passowrd = password_field["Password"]
        if not self.error:    
            query.save()
            self.error = []
            return True
        else:
            return False

def ChatbotView(req):
    return render(req,'chat_box.html')
#def RequestListView(req)
class RequestListView(View):
    def get(self, req):
        if req.session['clinic_user']:
            # today = datetime.today().strftime('%Y-%m-%d')
            clinic_user = req.session['clinic_user']
            clinic_id = clinic_user["id"]
            #bookings = Appointment.objects.raw("SELECT * FROM server_clinic WHERE ClinicID = %i AND Date < CURDATE()" %(clinic_id))
            status = req.GET.get("status", "Any status")
            if status == "Any status":
                bookings = Appointment.objects.filter(ClinicID = clinic_id).values()
                count = bookings.count()
            else:
                bookings = Appointment.objects.filter(ClinicID = clinic_id, Status = status).values()
                count = bookings.count() 
            for query in bookings:
                patient_id = query["PatientID"]
                patient_info = Patient.objects.filter(PatientID = patient_id).values("First_name", "Last_name", "Email")
                query.update(patient_info[0])
            context = { "bookings":bookings, "count":count, "status":status}
            return render(req, 'clinic/requestlist.html', context)
        else:
            return HttpResponseRedirect(reverse('signin'))
    def post(self,req):
        if req.session['clinic_user']:
            app_id = req.POST.get("app_id")
            ap = Appointment.objects.filter(AppointmentID=int(app_id))[0]
            file = req.FILES.get("file")
            file_content = ContentFile(file.read())
            ap.requirement.save(file.name, file_content)
            ap.Status = "Requirement Added"
            ap.save()
            p_id = ap.PatientID
            Patient_query = Patient.objects.filter(PatientID = p_id)[0]
            clinic_id = ap.ClinicID
            clinic_query = Clinic.objects.filter(ClinicID = clinic_id)[0]
            p_name = Patient_query.First_name
            p_email = Patient_query.Email
            app_exam = ap.Examination
            c_name = clinic_query.ClinicName
            c_date = ap.Date
            c_time = ap.Time
            c_contact = clinic_query.Contact
            send_requirement(p_name,p_email,app_exam,c_name,c_date,c_time,c_contact)
            return HttpResponseRedirect(reverse('requestlist'))
        else:
            return HttpResponseRedirect(reverse('signin'))


# class ClinicScheduleView(View):

#     def get(self, req):
#         schedule = Schedule.objects.all()
#         data = [
#             {
#                 "title": "12",
#                 "start": "2019-10-01"
#             }
#         ]
#         context = {

#         }
#         return render(req, 'doctor/schedule.html', context)
# class ScheduleApiView(View):
#     def serializer(self, qs):
#         re_data = []
#         for i in qs:
#             event = {
#                 "title": i.title,
#                 "start": i.start.strftime("%Y-%m-%d %H:%M"),
#                 "end": i.end.strftime("%Y-%m-%d %H:%M"),
#                 "allDay": "false"
#             }
#             re_data.append(event)
#         return re_data

#     def get(self, req):
#         schedule = Schedule.objects.all()
#         data = self.serializer(schedule)
#         return JsonResponse(data, safe=False)
class UploadReportView(View):
    def get(self, req):
        if req.session['clinic_user']:
            # today = datetime.today().strftime('%Y-%m-%d')
            clinic_user = req.session['clinic_user']
            clinic_id = clinic_user["id"]
            #bookings = Appointment.objects.raw("SELECT * FROM server_clinic WHERE ClinicID = %i AND Date < CURDATE()" %(clinic_id))
            status = req.GET.get("status", "Any status")
            if status == "Any status":
                bookings = Appointment.objects.filter(ClinicID = clinic_id).values()
                count = bookings.count()
            else:
                bookings = Appointment.objects.filter(ClinicID = clinic_id, Status = status).values()
                count = bookings.count() 
            for query in bookings:
                patient_id = query["PatientID"]
                patient_info = Patient.objects.filter(PatientID = patient_id).values("First_name", "Last_name", "Email")
                query.update(patient_info[0])
            context = { "bookings":bookings, "count":count, "status":status}
            
            return render(req, 'clinic/upload_report.html', context)
        else:
            return HttpResponseRedirect(reverse('signin'))

    def post(self, req):
        app_id = req.POST.get("app_id")
        ap = Appointment.objects.filter(AppointmentID=int(app_id))[0]
        file = req.FILES.get("file")
        file_content = ContentFile(file.read())
        ap.file.save(file.name, file_content)
        ap.Status = "Report Uploaded"
        ap.save()
        p_id = ap.PatientID
        Patient_query = Patient.objects.filter(PatientID = p_id)[0]
        clinic_id = ap.ClinicID
        clinic_query = Clinic.objects.filter(ClinicID = clinic_id)[0]
        p_name = Patient_query.First_name
        p_email = Patient_query.Email
        app_exam = ap.Examination
        c_name = clinic_query.ClinicName
        c_date = ap.Date
        c_time = ap.Time
        c_contact = clinic_query.Contact
        send_report_upload(p_name,p_email,app_exam,c_name,c_date,c_time,c_contact)
        return HttpResponseRedirect(reverse('upload_report'))

def get_statistics(req):
    if req.session['clinic_user']:
        if req.method=="GET":
            clinic_user = req.session['clinic_user']
            clinic_id = clinic_user['id']
            sure_score_list=[] #[approved.count, cancel.count]
            sure_score_list.append(Appointment.objects.filter(ClinicID=clinic_id).filter(Status='Approved').count())
            sure_score_list.append(Appointment.objects.filter(ClinicID=clinic_id).filter(Status='Cancel').count())
            #SELECT * FROM Appointment WHERE clinic=clinic_id ORFERBY date
            info = Appointment.objects.filter(ClinicID=clinic_id).order_by('Date')
            date_list = list(info.values_list('Date',flat=True))
            count_list=[]
            for date in date_list:
                count = info.filter(Date=date).count()
                count_list.append(count)
            current_time = datetime.now().strftime('%Y-%m-%d')
            context = {
                "clinic_name": clinic_user["name"],
                'result_score': count_list,
                'date_list': date_list,
                'current_time':current_time,
                'sure_score_list':sure_score_list,
            }
            return render(req,'clinic/statictics.html',context)


def monthRange(beginDate, endDate):
    monthSet = set()
    for date in dateRange(beginDate, endDate):
        monthSet.add(date[0:7])
    monthList = []
    for month in monthSet:
        monthList.append(month)
    return sorted(monthList)
def dateRange(beginDate, endDate):
    dates = []
    dt = datetime.datetime.strptime(beginDate, "%Y-%m-%d")
    date = beginDate[:]
    while date <= endDate:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y-%m-%d")
    return dates
class AppointmentView(View):
    def get(self, req):
        if req.session['user']:
            user = req.session['user']
            patient_id = user['id']
            query = Patient.objects.filter(PatientID=patient_id).values("Email", "First_name","Last_name")
            query_dict = list(query)[0]
            patient_name = query_dict["First_name"] + " " + query_dict["Last_name"]
            patient_email = query_dict["Email"]
            result = Clinic.objects.all()
            Question_dict = {"q1":"Do you have any allergies?", 
                    "q2":"Do you have asthma?",
                    "q3":"Do you have a history of kidney problems?",
                    "q4":"Do you have diabetes?",
                    "q5":"Do you have heart disease or high blood pressure for which you are taking medications?",
                    "q6":"Is there any possibility that you could be pregnant?"}
            context = {
                'nav': 'appointment',
                'info': result, # result = Clinic.objects.all()
                'patient_name': patient_name, # query_dict["First_name"] + " " + query_dict["Last_name"]
                'patient_email': patient_email, #query_dict["Email"]
                "Question_dict":Question_dict.items(),
                }
            return render(req,'patient/appointment.html', context)
        else:
            return HttpResponseRedirect(reverse('signin'))

def Step_1(req):
    import re
    examination = req.POST.get("info")
    exam_web=["Children's Imaging","CT","MRI","X-ray","Women's Procedures"]
    exam_sql=["ChildrenImage","CT","MRI","X_Ray","WomenProcedure"]
    for i in range(len(list)):
        if examination == exam_web[i]:
            keyword = exam_sql[i]
            break
    info_list=[]#returned result
    infos = Clinic.objects.raw("SELECT * FROM server_clinic WHERE %s ='1'" %(keyword))
    for i in range(0, len(infos)):
        data = {"clinic_name": re.sub("\s+","",infos[i].ClinicName),
                "clinic_email": infos[i].Email,
                "address": infos[i].Address,
                "zip_code": infos[i].ZipCode,
                "contact": infos[i].Contact,
                'clinic_id':infos[i].ClinicID,
            }
        info_list.append(data)
    count = len(infos)
    return JsonResponse({"info":info_list,'count':count, "examination": examination})
def get_clinic_info(req):
    import re
    info=req.POST.get('info')
    examination=req.POST.get('type')
    exam_web = ["Children's Imaging", "CT", "MRI", "X-ray", "Women's Procedures"]
    exam_sql = ["ChildrenImage","CT","MRI","X_Ray","WomenProcedure"]
    key = 0
    for i in range(len(list)):
        if examination == exam_web[i]:
            keyword = exam_sql[i]
            break
    info_list=[]
    infos = Clinic.objects.raw("SELECT * FROM server_clinic WHERE %s='1' and ZipCode=%s" %(keyword,info))
    for i in range(0,len(infos)):
        data = {"clinic_name": re.sub("\s+", "", infos[i].ClinicName),
                "clinic_email": infos[i].Email,
                "address": infos[i].Address,
                "zip_code": infos[i].ZipCode,
                "contact": infos[i].Contact,
                'clinic_id': infos[i].ClinicID,
                }
        info_list.append(data)
    if len(infos)!=0:
        return JsonResponse({"info":info_list,"type":keyword})
    if len(infos):
        return JsonResponse({"key":'none'})
def Step_2(req):
    info=req.POST.get("info")
    clinic_name = Clinic.objects.filter(ClinicID=int(info)).ClinicName
    return JsonResponse({"ClinicName":clinic_name})

# def Appointment_Get_Time(query_time):
#     time_dict = {"half_ba":"8:30am", "jiu":"9am", "half_jiu":"9:30am", "si":"10am", "half_sy":"10:30am",
#                 "sy":"11am", "half_sy":"11:30am", 'lunch':"12.00pm-1.00pm","half_san":"13:30pm", "ssi":"14pm", "half_ssi":"14:30pm",
#                 "siwu":"15pm", "half_siwu":"15:30pm","sl":"16pm", "half_sl":"16:30pm", "sq":"17pm"}
#     count = 0
#     if len(query_time) == 0:
        
#         return(time_dict, count)
#     else:
#         for key in time_dict:
#             if time_dict[key] in query_time:
#                 count+=1
#                 time_dict[key]='Unavailable'
        
#         return(time_dict,count)

#def Appointment_Step_4
def Step_3(req):
    clinic_id = req.POST.get("clinic_id")
    date = req.POST.get("date")
    query_time = Appointment.objects.filter(Date=date,ClinicID=clinic_id).values_list('Time',flat=True)
    query_time = list(query_time)
    time_list = ["8:30am", "9am", "9:30am", "10am", "10:30am", "11am", "11:30am", "12.00pm-1.00pm","13:30pm", "14pm", "14:30pm",
                "15pm", "15:30pm","16pm", "16:30pm", "17pm"]
    count = 0
    for i in range(0, len(time_list)):
        if time_list[i] in query_time:
            time_list[i] = "Unavailable"
            count += 1
    print("time_list",time_list)
    if count < len(time_list): 
        return JsonResponse({"info":time_list})
    else:
        #No available time for this date
        return JsonResponse({"info":["There is no available time for this date, please select anoteher date"]})
#Step5: Submit request
#def Appointment_Step_6(req):
def Step_6(req):
    quesiton = req.POST.get("quesiton")
    clinic_id = req.POST.get("clinic_id")
    patient_name = req.POST.get("patient_name")
    patient_email = req.POST.get("patient_email")
    examination = req.POST.get("examination")
    clinic_name = req.POST.get("clinic_name")
    clinic_email = req.POST.get("clinic_email")
    clinic_address = req.POST.get("address")
    clinic_contact = req.POST.get("contact")
    date = req.POST.get("date")
    time = req.POST.get("time")
    user=req.session['user']
    id=user['id']
    info=Appointment(
    PatientID=id,
    ClinicID=clinic_id,
    Date=date,
    Time=time,
    Examination=examination,
    Status='Pending',
    Questionaires=quesiton,
    )
    info.save()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    Text_email(name,email,examination,clinic_name,date,time,current_time)
    return JsonResponse({"tutes":"OK"})




def refese_reqest(req):
    app_id=req.POST.get("id")
    datet=req.POST.get("date")
    info = Appointment.objects.get(AppointmentID = app_id)
    info.Status = 'Cancel'
    info.save()
    u_id = info.PatientID
    email = Patient.objects.get(PatientID=u_id).Email
    username = Patient.objects.get(PatientID=u_id).First_name
    type = info.Examination
    clinic_id =info.ClinicID
    cur_date = info.Date
    cur_time = info.Time
    contact = Clinic.objects.get(ClinicID=clinic_id).Contact
    clinic_name = Clinic.objects.get(ClinicID=clinic_id).ClinicName
    send_no_result(username, email, type, clinic_name, datet, cur_date, cur_time, contact)
    return JsonResponse({"Cancelled": "OK"})

#def Clinic_Reqlst_Approve(req)
def approve_reqest(req):
    app_id=req.POST.get("id")
    info=Appointment.objects.get(AppointmentID=app_id)
    info.Status='Approved'
    info.save()
    u_id=info.PatientID
    email=Patient.objects.get(PatientID=u_id).Email
    username=Patient.objects.get(PatientID=u_id).First_name
    type = info.Examination
    clinic_id = info.ClinicID
    clinic_name = Clinic.object.get(ClinicID = clinic_id).ClinicName
    date = info.Date
    time = info.Time
    contact=Clinic.objects.get(ClinicID = clinic_id).Contact
    send_ok_result(username, email, type, clinic_name, date, time, contact)
    return JsonResponse({"approve":"OK"})

