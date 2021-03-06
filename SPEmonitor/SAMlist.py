import os
import datetime
import sys
import samweb_client as sw

samweb = sw.SAMWebClient(experiment='uboone')
time_delta = 15

def TimeFormat():

    now = datetime.datetime.now()
    then = datetime.datetime.now() - datetime.timedelta(days = time_delta)

    year = str(now.year)
    
    if now.month > 9: 
        month = str(now.month)
    else:
        month = '0'+str(now.month)
    
    if now.day > 9:
        day = str(now.day)
    else:
        day = '0'+str(now.day)

    if now.hour > 9:
        hour = str(now.hour)
    else:
        hour = '0'+str(now.hour)

    if now.minute > 9:
        minute = str(now.minute)
    else:
        minute = '0'+str(now.minute)

    if now.second > 9:
        second = str(now.second)
    else:
        second = '0'+str(now.second)


    Tyear = str(then.year)
    
    if then.month > 9: 
        Tmonth = str(then.month)
    else:
        Tmonth = '0'+str(then.month)
    
    if then.day > 9:
        Tday = str(then.day)
    else:
        Tday = '0'+str(then.day)

    if then.hour > 9:
        Thour = str(then.hour)
    else:
        Thour = '0'+str(then.hour)

    if then.minute > 9:
        Tminute = str(then.minute)
    else:
        Tminute = '0'+str(then.minute)

    if then.second > 9:
        Tsecond = str(then.second)
    else:
        Tsecond = '0'+str(then.second)


    formatted_current_time = year+'-'+month+'-'+day+'T'+hour+':'+minute+':'+second
    formatted_last_time     = Tyear+'-'+Tmonth+'-'+Tday+'T'+Thour+':'+Tminute+':'+Tsecond

    return formatted_current_time , formatted_last_time


def GetRecentFiles():

    now,then = TimeFormat()

    arg = "end_time < '%s' and end_time > '%s' and (ub_project.stage = mergeext_unbiased or ub_project.stage = mergebnb_unbiased or ub_project.stage = nubnb_unbiased)" %(now,then)
    return samweb.listFiles(arg)


def Get_Recent_Runs():

    files = GetRecentFiles()
    run_nums = []

    for x in files:
   
        meta_data = samweb.getMetadata(x)
        file_run = meta_data['runs'][0][0]

        if file_run not in run_nums:
            run_nums.append(file_run)

    run_nums.sort(reverse=True)

    return run_nums
#---------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

current_max_run = Get_Recent_Runs()

x = current_max_run[0]

range1=[x]
range2=[]
range3=[]
range4=[]

total=0
while x  > 0:

    sam_arg = "run_number = %i and (ub_project.stage = mergeext_unbiased or ub_project.stage = mergebnb_unbiased or ub_project.stage = nubnb_unbiased)" %(x)
    rawData = samweb.listFilesSummary(sam_arg)
    num_events = rawData['total_event_count']
 
    if type(num_events) == int:
        total += num_events

    if total >= 10000:
        if len(range1) < 2:
            range1.append(x)
            range2.append(x-1)
            total = 0

        elif len(range2) < 2:
            range2.append(x)
            range3.append(x-1)
            total = 0

        elif len(range3) < 2:
            range3.append(x)
            range4.append(x-1)
            total = 0

        else:
            range4.append(x)
            break

    x -= 1


back_range1=(range1[1],range1[0])
back_range2=(range2[1],range2[0])
back_range3=(range3[1],range3[0])
back_range4=(range4[1],range4[0])


list_file = open("/uboone/app/users/moon/OpticalStudies/v05_01_01/workdir/SPEmonitor/RunsList.txt","w")
list_file.write(str(back_range1))
list_file.write("\n")
list_file.write(str(back_range2))
list_file.write("\n")
list_file.write(str(back_range3))
list_file.write("\n")
list_file.write(str(back_range4))
list_file.close()

sys_out1 = "samweb delete-definition first_recent"
sys_out2 = "samweb delete-definition second_recent"
sys_out3 = "samweb delete-definition third_recent"
sys_out4 = "samweb delete-definition fourth_recent"

os.system(sys_out1)
os.system(sys_out2)
os.system(sys_out3)
os.system(sys_out4)

sys_out5 = "samweb create-definition first_recent 'run_number <= %i and run_number >= %i and (ub_project.stage = mergeext_unbiased or ub_project.stage = mergebnb_unbiased or ub_project.stage = nubnb_unbiased)'" %(max(range1),min(range1))
sys_out6 = "samweb create-definition second_recent 'run_number <= %i and run_number >= %i and (ub_project.stage = mergeext_unbiased or ub_project.stage = mergebnb_unbiased or ub_project.stage = nubnb_unbiased)'" %(max(range2),min(range2))
sys_out7 = "samweb create-definition third_recent 'run_number <= %i and run_number >= %i and (ub_project.stage = mergeext_unbiased or ub_project.stage = mergebnb_unbiased or ub_project.stage = nubnb_unbiased)'" %(max(range3),min(range3))
sys_out8 = "samweb create-definition fourth_recent 'run_number <= %i and run_number >= %i and (ub_project.stage = mergeext_unbiased or ub_project.stage = mergebnb_unbiased or ub_project.stage = nubnb_unbiased)'" %(max(range4),min(range4))

os.system(sys_out5)
os.system(sys_out6)
os.system(sys_out7)
os.system(sys_out8)

















