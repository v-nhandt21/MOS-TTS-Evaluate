#!/usr/bin/env python3
DEV=0
from flask import Flask, render_template, request,json
import sys
from datetime import datetime
#sys.path.append('Service/')
import warnings
warnings.filterwarnings("ignore")
if DEV:
    from inference import getAudio
app = Flask(__name__, static_url_path='/static')

@app.route("/", methods=['GET', 'POST'])
def main():
    with open("static/sample.txt", "r" ,encoding="utf-8") as f:
        lines = f.readlines()
        #print(lines)
    return render_template('index.html',lines=lines)


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
    return render_template('thank.html')


@app.route("/results", methods=['GET', 'POST'])
def results():
    user=[]
    with open("static/result/user","r",encoding="utf-8") as f:
        user=f.read().splitlines()
    JS=""
    for i in user:
        with open("static/result/"+str(i), "r" ,encoding="utf-8") as f:
            lines = f.read()
            JS+=lines+"\n"
    return render_template('results.html',JS=JS)

@app.route("/mos", methods=['GET', 'POST'])
def mos():
    user=[]
    with open("static/result/user","r",encoding="utf-8") as f:
        user=f.read().splitlines()
    JS=""
    MOS_TRUTH=0
    MOS_TACO=0
    for i in user:
        if i[0]!="_":
            continue
        with open("static/result/"+str(i), "r" ,encoding="utf-8") as f:
            lines = f.read().splitlines()
            print(float(lines[2]))
            MOS_TACO=MOS_TACO+float(lines[1])
            MOS_TRUTH=MOS_TRUTH+float(lines[2])
    JS = "MOS of Tacotron is: " + str(float("{:.2f}".format(MOS_TACO/float(len(user))))) + "\n"
    JS +="MOS of Ground Truth is: " + str(float("{:.2f}".format(MOS_TRUTH/float(len(user))))) + "\n"
    return render_template('results.html',JS=JS)

if __name__ == "__main__":
    app.run(host= '192.168.100.8')


'''
IPv4 Address. . . . . . . . . . . : 192.168.100.8
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : 192.168.100.1
   '''
