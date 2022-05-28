
from operator import le
import re
from services.pbiembedservice import PbiEmbedService
from utils import Utils
from flask import Flask, render_template, send_from_directory
from flask import request
import json
import os
import pandas as pd


# Initialize the Flask app
app = Flask(__name__)

# Load configuration
app.config.from_object('config.BaseConfig')
app.config['UPLOAD_FOLDER']='static/files'
app.config['SALES']='static/sales'

#function to get X-axis labels (text format)
def Lab(df):
    Labels=[]
    for i in df.columns:
            if isinstance(df[i][0],str):
                Labels.append(i)
    return Labels

#function to get Y-axis labels (Number format)
def Dat(df):
    Dataset=[]
    for i in df.columns:
            if not isinstance(df[i][0],str):
                Dataset.append(i)
    return Dataset

def dict1(df):
    d={} 
    k=0 
    for i in df.columns:
            d[i]=k
            k=k+1 
    return d


@app.route('/')
def index():
    #the login page is rendered onto browser
    return render_template('index.html')
   
@app.route('/getembedinfo', methods=['GET'])
def get_embed_info():
    '''Returns report embed configuration'''

    config_result = Utils.check_config(app)
    if config_result is not None:
        return json.dumps({'errorMsg': config_result}), 500

    try:
        embed_info = PbiEmbedService().get_embed_params_for_single_report(app.config['WORKSPACE_ID'], app.config['REPORT_ID'])
        return embed_info
    except Exception as ex:
        return json.dumps({'errorMsg': str(ex)}), 500

@app.route('/favicon.ico', methods=['GET'])
def getfavicon():
    '''Returns path of the favicon to be rendered'''

    return send_from_directory(os.path.join(app.root_path, 'static'), 'img/favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/form_login', methods=['POST','GET'])
def login():
    #when POST request is made
    if request.method=='POST':
        #when the user uploads a custom file
        if request.form['switch']=="123":
            f=request.files['file']
            print("hey i got in")
            global x1,y1,x2,y2,x3,y3,x4,p,di
            #file is saved in static/files
            f.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],f.filename)) # saving the file
            global df
            #pandas dataframe is created
            df = pd.read_csv(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],f.filename))
            Labels=Lab(df)
            global Dataset
            Dataset=Dat(df)
            index=0
            global d
            d=dict1(df)
            list1=[]
            global data
            data=df
            global le
            le=len(df)
            return render_template('temp1.html',df1=df,d=d,Labels=Labels,Dataset=Dataset,list1=list1,x1=x1,y1=y1,x2=x2,y2=y2,x3=x3,y3=y3,x4=x4,p=p,di=di)
         #when the login button is clicked, main page gets loaded
        elif request.form['switch']=="456":
            name=request.form['u']
            psd1=request.form['v']
            print(name+" "+psd1)
            if name != "user":
                return render_template('index.html',info="Invalid User!")
            elif psd1 != "user":
                return render_template('index.html',info="Invalid Password!")
            else:
                df=[]
                list1=[]
                global list2
                list2=[]
                global x
                x = pd.read_csv(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['SALES'],"sale.csv"))
                l1=set()
                l2=[]
                for i in x['City']:
                    l1.add(i)
                for j in l1:
                    l2.append(0)
                l1=list(l1)
                for i in range(len(x)):
                        for j in range(0,len(l1)):
                            if x['City'][i]==l1[j]:
                                l2[j]+=x['Sales'][i]
                x1=l1
                y1=l2
                l1=set()
                l2=[]
                for i in x['Make']:
                    l1.add(i)
                for j in l1:
                    l2.append(0)
                l1=list(l1)
                for i in range(len(x)):
                        for j in range(0,len(l1)):
                            if x['Make'][i]==l1[j]:
                                l2[j]+=x['Sales'][i]
            
                x2=l1
                y2=l2
                l1=set()
                l2=[]
                for i in x['YearofSales']:
                    l1.add(i)
                for j in l1:
                    l2.append(0)
                l1=list(l1)
                for i in range(len(x)):
                        for j in range(0,len(l1)):
                            if x['YearofSales'][i]==l1[j]:
                                l2[j]+=x['Sales'][i]
            
                x3=l1
                y3=l2
                l1=set()
                p=[]
                di=[]
                for i in x['City']:
                    l1.add(i)
                for j in l1:
                    p.append(0)
                    di.append(0)
                l1=list(l1)
                for i in range(len(x)):
                        for j in range(0,len(l1)):
                            if x['City'][i]==l1[j]:
                                if x['FuelType'][i]=='Petrol':
                                    p[j]+=x['Sales'][i]
                                else:
                                    di[j]+=x['Sales'][i]
            
                x4=l1
                return render_template('temp.html',df1=df,list1=list1,list2=list2,x=x,x1=x1,y1=y1,x2=x2,y2=y2,x3=x3,y3=y3,x4=x4,p=p,di=di)
        #back button is clicked
        elif request.form['switch']=='goback':
            list1=[]
            list2=[]
            return render_template('temp.html',df1=df,list1=list1,list2=list2,x1=x1,y1=y1,x2=x2,y2=y2,x3=x3,y3=y3,x4=x4,p=p,di=di)
        #when button to create new graph is clicked
        elif request.form['switch']=="graph":
            X=request.form['Label']
            Y=request.form['Dataset']
            list1=[]
            list2=[]
            l1=df[X]
            l2=df[Y]
            for i in l1:
                list1.append(i)
            for i in l2:
                list2.append(i)      
            l1=set()
            l2=[]
            for i in list1:
                l1.add(i)
            for j in l1:
                l2.append(0)
            l1=list(l1)
            for i in range(len(df)):
                    for j in range(0,len(l1)):
                        if df.iat[i,d[X]]==l1[j]:
                            l2[j]+=df.iat[i,d[Y]]
    
            return render_template('temp1.html',list1=l1,list2=l2,X=X,Y=Y,df1=df,x1=x1,y1=y1,x2=x2,y2=y2,x3=x3,y3=y3,x4=x4,p=p,di=di)
    #when GET request is made
    else:
        df=[]
        list1=[]
        list2=[]
        return render_template('temp.html',df1=df,list1=list1,list2=list2,x1=x1,y1=y1,x2=x2,y2=y2,x3=x3,y3=y3,x4=x4,p=p,di=di)

if __name__ == '__main__':
    app.run()