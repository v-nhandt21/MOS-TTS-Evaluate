#!/usr/bin/env python3
DEV=0
from flask import Flask, render_template, request,json
import sys
from datetime import datetime
import random
#sys.path.append('Service/')
import warnings




warnings.filterwarnings("ignore")
app = Flask(__name__, static_url_path='/static')



@app.route("/", methods=['GET', 'POST'])
def main():
    with open("static/sample.txt", "r" ,encoding="utf-8") as f:
        lines = f.readlines()
    ranlist=[]
    for f in range(len(lines)):
        ranlist.append(random.randint(3, 90)%2)
    print(ranlist)
    return render_template('index.html',lines=lines,ranlist=ranlist)


@app.route("/thank", methods=['GET', 'POST'])
def thank():
    if request.method == 'GET':
        res=dict(request.args)
        #print(res)

        name = res['lname']

        MOS_TACO=0
        MOS_TRUTH=0
        for i in range(20):
            geta='taco-'+str(i)
            MOS_TACO=MOS_TACO+int(res[geta])
            getb='truth-'+str(i)
            MOS_TRUTH=MOS_TRUTH+int(res[getb])
        MOS_TACO=MOS_TACO/float(20)
        MOS_TRUTH=MOS_TRUTH/float(20)

        now = str(datetime.now())

        print(now)
        print(MOS_TACO) 
        print(MOS_TRUTH)

        MOS_TACO=float("{:.2f}".format(MOS_TACO))
        MOS_TRUTH=float("{:.2f}".format(MOS_TRUTH))

        with open("static/result/"+name,'w+',encoding="utf-8") as fw:
            fw.write(now+"\n")
            fw.write(str(name)+"\n")
            fw.write(str(MOS_TACO)+"\n")
            fw.write(str(MOS_TRUTH)+"\n")
        with open("static/result/user",'a+',encoding="utf-8") as fw:
            fw.write(name+"\n")
        res="Taco: "+str(MOS_TACO)+"  "+"Truth: "+str(MOS_TRUTH)



        msg = Message(res, sender = 'xojziyfay@gmail.com', recipients = ['donhanbentre@gmail.com'])
        msg.body = "Hello Flask message sent from Flask-Mail"
        mail.send(msg)
    return render_template('thank.html', res=res)


@app.route("/results", methods=['GET', 'POST'])
def results():
    user=[]
    with open("static/result/user","r",encoding="utf-8") as f:
        user=f.read().splitlines()
    JS=[]
    for i in list(set(user)):
        with open("static/result/"+str(i), "r" ,encoding="utf-8") as f:
            lines = f.read()
            JS.append(lines.replace("\n","\t"))
    return render_template('results.html',JS=JS)

@app.route("/mos", methods=['GET', 'POST'])
def mos():
    user=[]
    with open("static/result/user","r",encoding="utf-8") as f:
        user=f.read().splitlines()
    JS=""
    MOS_TRUTH=0 
    MOS_TACO=0

    user_ =0
    if len(user) ==0:
        return render_template('mos.html',JS="No valid user now")
    for i in list(set(user)):
        
        if i[0]=="_":
            continue
        user_+=1    
        with open("static/result/"+str(i), "r" ,encoding="utf-8") as ff:
            lines = ff.read().splitlines()
            #print(float(lines[2]))
            MOS_TACO=MOS_TACO+float(lines[2])
            MOS_TRUTH=MOS_TRUTH+float(lines[3])
    if len(list(set(user))) > 0 :
        JS = "MOS of Tacotron is: " + str(float("{:.2f}".format(MOS_TACO/float(user_)))) + "\n"
        JS +="MOS of Ground Truth is: " + str(float("{:.2f}".format(MOS_TRUTH/float(user_)))) + "\n"
    return render_template('mos.html',JS=JS)

if __name__ == "__main__":
    app.run()


'''
IPv4 Address. . . . . . . . . . . : 192.168.100.8
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : 192.168.100.1
   '''
