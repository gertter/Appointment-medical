# #!/usr/bin/python
# # -*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText
def send_mails(to_list, sub, content):
    mail_host = "smtp.qq.com"
    mail_user = "wind_of_change_9900@foxmail.com"
    mail_pass = "inmubizwhxisbeae"
    mail_postfix = "foxmail.com"
    me = "<" + mail_user + "@" + mail_postfix + ">"  
    msg = MIMEText(content, _subtype='html', _charset='gb2312')  # html mail template
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)  # smtp connect
        s.login(mail_user, mail_pass)  # login to server
        s.sendmail(me, to_list, msg.as_string())  # send email
        s.close()
        return True
    except Exception as e:
        print("Fail to send email...",e)
        return False
def Text_email(name,email,type,clinic,date,time,current_time):
    title='[COMP_9900] Radiology Examination request submitted'
    text=''
    text+='<p style="font-size:16px;"><b>Dear Patient:</b></p>'
    text+='<p style="font-size:16px;"><b>Your Booking Request is submitted!</b></p><br/>'
    text+='Appointment Summary<br/>'
    text+='Patient name:'+name+'<br/>'
    text += 'Patient email:'+email+'<br/>'
    text += 'Examination Type: '+type+'<br/>'
    text += 'Radiology Clinic: '+clinic+'<br/>'
    text += 'Appointment Date:'+date+'<br/>'
    text += 'Appointment Time:'+time+'<br/>'
    text += '<p style="font-size:16px;"><b>Please wait for the clinic to process your request.</b></p>'
    text += 'Date:'+current_time+'<br/>'
    send_mails(email,title,text)

def send_ok_result(username,email,type,clinic,date,time,contact):
    title = '[COMP_9900] Your radiology examination request update'
    text = ''
    text+='<p>Dear '+str(username)+':</p>'
    text+='<p>Your ['+type+'] booking at ['+str(date)+'], ['+str(time)+'], ['+clinic+'] has been</p>'
    text+='<p>approved by the clinic. Please check the preparation/ chat with</p>'
    text+='<p>assistant bot at our website, you may also contact the clinic at ['+contact+']</p>'
    text+='<p>for more details.</p><br/>'
    text=''    
    text+='<p>Regards,</p>'
    text+='<p>Radiology Examination assistant</p>'
    send_mails(email, title, text)



def send_no_result(username,email,type,clinic,date,cur_date,cur_time,contact):
    title = '[COMP_9900] Your radiology examination request update'
    text=''
    text+='<p>Dear '+str(username )+':</p>'
    text+='<p>Your ['+str(type)+'] booking at ['+str(cur_date)+'], ['+str(cur_time)+'], ['+str(clinic)+'] has been</p>'
    text+='<p>schedule at ['+str(date)+'], please go and book another</p>'
    text+='<p>appointment at our website or contact the clinic at ['+str(contact)+'] for</p>'
    text+='<p>more details.</p>'
    text=''    
    text += '<p>Regards,</p>'
    text += '<p>Radiology Examination assistant</p>'
    send_mails(email, title, text)

def send_report_upload(username,email,type,clinic,date,time,contact):
    title = '[COMP_9900] Your radiology examination report uploaded'
    text=''
    text+='<p>Dear '+str(username )+':</p>'
    text+='<p>Your ['+str(type)+'] examination report at ['+str(date)+'], ['+str(time)+'], ['+str(clinic)+'] has been</p>'
    text+='<p> uploaded</p>'
    text+='<p>please visit our website to check the report or contact the clinic at ['+str(contact)+'] for</p>'
    text+='<p>further details.</p>'
    text=''    
    text += '<p>Regards,</p>'
    text += '<p>Radiology Examination assistant</p>'
    send_mails(email, title, text)

def send_requirement(username,email,type,clinic,date,time,contact):
    title = '[COMP_9900] Additional requirement from clinic added for your radiology examination'
    text=''
    text+='<p>Dear '+str(username )+':</p>'
    text+='<p>['+str(clinic)+'] has added addtional requirement document for your ['+str(type)+'] examination report at ['+str(date)+'], ['+str(time)+']</p>'
    text+='<p>Please visit our website to check the requirement document.</p>'
    text+='<p>Contact the clinic at ['+str(contact)+'] for further details</p>'
    text=''
    text += '<p>Regards,</p>'
    text += '<p>Radiology Examination assistant</p>'
    send_mails(email, title, text)