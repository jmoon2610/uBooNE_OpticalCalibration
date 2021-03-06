import numpy as np
import matplotlib.pyplot as plt
import os

def CheckOutliers(values):

    median = np.median(values)
    abs_dev = []
     
    for x in values:
        abs_dev.append(abs(x-median))
     
    MAD = np.median(abs_dev)

    for x in values:
        mod_Z = 0.6745*(x-median) / MAD
        if mod_Z > 20:
            return 1
            break

    return 0
    
def GetLinFitCoeffs(x,y):

    A = np.vstack([x,np.ones(len(x))]).T
    m,c = np.linalg.lstsq(A,y)[0]
    
    return m
    
def IsTooHighLow(values):
    
    if max(values) > 350 or min(values) < 150:
        return 1
    else:
        return 0


four_recent_gain = []
three_recent_gain = []
two_recent_gain = []
one_recent_gain = []

four_recent_sig = []
three_recent_sig = []
two_recent_sig = []
one_recent_sig = []

run_list = []
convert_to_kHz = 42.662
date_list = []

with open("/uboone/app/users/moon/OpticalStudies/v05_01_01/workdir/SPEmonitor/RunsList.txt") as infile:
    for line in infile:
        run_list.append(line.rstrip('\n'))


with open("/uboone/app/users/moon/OpticalStudies/v05_01_01/workdir/SPEmonitor/DateList.txt") as infile:
    for line in infile:
        date_list.append(line.rstrip('\n'))

with open("/uboone/app/users/moon/OpticalStudies/v05_01_01/workdir/SPEmonitor/CurrentSPEamps/first_recent_singles.txt") as infile1:
    for line in infile1:
        one_recent_gain.append(42.662*float(line.rstrip('\n')))

with open("/uboone/app/users/moon/OpticalStudies/v05_01_01/workdir/SPEmonitor/CurrentSPEamps/second_recent_singles.txt") as infile2:
    for line in infile2:
        two_recent_gain.append(42.662*float(line.rstrip('\n')))

with open("/uboone/app/users/moon/OpticalStudies/v05_01_01/workdir/SPEmonitor/CurrentSPEamps/third_recent_singles.txt") as infile3:
    for line in infile3:
        three_recent_gain.append(42.662*float(line.rstrip('\n')))

with open("/uboone/app/users/moon/OpticalStudies/v05_01_01/workdir/SPEmonitor/CurrentSPEamps/fourth_recent_singles.txt") as infile4:
    for line in infile4:
        four_recent_gain.append(42.662*float(line.rstrip('\n')))

with open("/uboone/app/users/moon/OpticalStudies/v05_01_01/workdir/SPEmonitor/CurrentSPEamps/first_recent_singles_sig.txt") as infile5:
    for line in infile5:
        one_recent_sig.append(42.662*float(line.rstrip('\n')))

with open("/uboone/app/users/moon/OpticalStudies/v05_01_01/workdir/SPEmonitor/CurrentSPEamps/second_recent_singles_sig.txt") as infile6:
    for line in infile6:
        two_recent_sig.append(42.662*float(line.rstrip('\n')))

with open("/uboone/app/users/moon/OpticalStudies/v05_01_01/workdir/SPEmonitor/CurrentSPEamps/third_recent_singles_sig.txt") as infile7:
    for line in infile7:
        three_recent_sig.append(42.662*float(line.rstrip('\n')))

with open("/uboone/app/users/moon/OpticalStudies/v05_01_01/workdir/SPEmonitor/CurrentSPEamps/fourth_recent_singles_sig.txt") as infile8:
    for line in infile8:
        four_recent_sig.append(42.662*float(line.rstrip('\n')))


x1 = np.asarray([1,2,3,4])

fig = plt.figure(facecolor='0.5')
fig.subplots_adjust(bottom=0.1, left=0.06, top = 0.85, right=0.975)

isAlertOutlier = 0
isAlertTrend   = 0
isAlertAbs     = 0

for x in range(0,16):

    name = "sub%i"%(x)
    name = fig.add_subplot(2,16,x+1)

    title = "Ch%i"%(x)
    name.set_title(title,fontsize = 8)
    

    name.set_xlim([0,5])
    name.set_ylim([0,400])
    name.axes.get_xaxis().set_visible(False)

    if (x > 0):
        name.axes.get_yaxis().set_visible(False)

    plt.plot([0,5],[50,50], color='0.85',linewidth=1.0,linestyle="--")
    plt.plot([0,5],[100,100], color='0.85',linewidth=1.0,linestyle="--")
    plt.plot([0,5],[150,150], color='0.85',linewidth=1.0,linestyle="--")
    plt.plot([0,5],[200,200], color='0.85',linewidth=1.0,linestyle="--")
    plt.plot([0,5],[250,250], color='0.85',linewidth=1.0,linestyle="--")
    plt.plot([0,5],[300,300], color='0.85',linewidth=1.0,linestyle="--")
    plt.plot([0,5],[350,350], color='0.85',linewidth=1.0,linestyle="--")



    y = []
    y.append(four_recent_gain[x])
    y.append(three_recent_gain[x])
    y.append(two_recent_gain[x])
    y.append(one_recent_gain[x])
    y1 = np.asarray(y)
    
    

    yerr = []
    yerr.append(four_recent_sig[x])
    yerr.append(three_recent_sig[x])
    yerr.append(two_recent_sig[x])
    yerr.append(one_recent_sig[x])
    yerr1 = np.asarray(yerr)

    name.errorbar(x1,y1,yerr=yerr1,xerr=None,ls='none',capsize=1,marker='o',markersize='2')

    if CheckOutliers(y1) == 1:
        name.set_facecolor('lightcoral')
        isAlertOutlier = 1

    if abs(GetLinFitCoeffs(x1,y1)) > 60:
        name.set_facecolor('lightcoral')
        isAlertTrend = 1

    if IsTooHighLow(y1) == 1:
        name.set_facecolor('lightcoral')
        isAlertAbs = 1
        

for x in range(16,32):

    name = "sub%i"%(x)
    name = fig.add_subplot(2,16,x+1)

    title = "Ch%i"%(x)
    name.set_title(title,fontsize=8)

    name.set_xlim([0,5])
    name.set_ylim([0,400])

    name.axes.get_xaxis().set_visible(False)

    if (x > 16):
        name.axes.get_yaxis().set_visible(False)


    plt.plot([0,5],[50,50], color='0.85',linewidth=1.0,linestyle="--")
    plt.plot([0,5],[100,100], color='0.85',linewidth=1.0,linestyle="--")
    plt.plot([0,5],[150,150], color='0.85',linewidth=1.0,linestyle="--")
    plt.plot([0,5],[200,200], color='0.85',linewidth=1.0,linestyle="--")
    plt.plot([0,5],[250,250], color='0.85',linewidth=1.0,linestyle="--")
    plt.plot([0,5],[300,300], color='0.85',linewidth=1.0,linestyle="--")
    plt.plot([0,5],[350,350], color='0.85',linewidth=1.0,linestyle="--")


    y = []
    y.append(four_recent_gain[x])
    y.append(three_recent_gain[x])
    y.append(two_recent_gain[x])
    y.append(one_recent_gain[x])
    y1 = np.asarray(y)

    yerr = []
    yerr.append(four_recent_sig[x])
    yerr.append(three_recent_sig[x])
    yerr.append(two_recent_sig[x])
    yerr.append(one_recent_sig[x])
    yerr1 = np.asarray(yerr)
    
    name.errorbar(x1,y1,yerr1,xerr=None,ls='none',capsize=1,marker='o',markersize='2')

    if CheckOutliers(y1) == 1:
        name.set_facecolor('lightcoral')
        isAlertOutlier = 1

    if abs(GetLinFitCoeffs(x1,y1)) > 60:
        name.set_facecolor('lightcoral')
        isAlertTrend = 1

    if IsTooHighLow(y1) == 1:
        name.set_facecolor('lightcoral')
        isAlertAbs = 1


fig.suptitle('Trigger Rate \n  Run Ranges %s , %s , %s , %s \n Date Ranges %s , %s , %s , %s'%(run_list[3],run_list[2],run_list[1],run_list[0],date_list[3],date_list[2],date_list[1],date_list[0]),fontsize=12,fontweight='bold',y=1.0)


plt.savefig('/web/sites/www-microboone.fnal.gov/htdocs/at_work/operations/PMTmonitor/singles.png',figsize=(8.6),dpi=300)

outstring = "Hello person who cares if uBooNEs PMTs are in trouble. The monitor has flagged one or more PMTs for the following reason(s): \n \n"

if isAlertOutlier == 1:
    outstring += "A significant outlier in the rate compared to other recent runs.\n"

if isAlertTrend == 1:
    outstring += "A significant overall linear trend.\n"

if isAlertAbs == 1:
    outstring += "A value that has gone above or below preset desirable limits.\n"

outstring += "\n The monitor is here if you dont have the link. \n \n http://www-microboone.fnal.gov/at_work/operations/PMTmonitor/MakeMonitorPage.html"

sysout = "source /uboone/app/users/moon/OpticalStudies/v05_01_01/workdir/SPEmonitor/AlertEmail.sh '%s'" %(outstring)

if isAlertOutlier == 1 or isAlertTrend == 1 or isAlertAbs == 1:
    dummy = os.system(sysout)


