from django.shortcuts import render
from django.http import HttpResponseRedirect
import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
from django import forms
from datetime import datetime

dynamodb = boto3.resource('dynamodb')



#Creating class for passing the problem
class assignEmployee:

    def __init__(self,cmp_id,org_id,dep_id=None):
        self.cmp_id=cmp_id
        self.org_id=org_id
        self.dep_id=dep_id

    def assign(self):
        dynamodb=boto3.resource('dynamodb')
        emp_table=dynamodb.Table('employees')
        cmp_table=dynamodb.Table('ComplaintS')
        dep_table=dynamodb.Table('departments')
        hie_table=dynamodb.Table('hierarchy')

        if(self.dep_id==None):
            dep_id_list=[]

            dep_response = dep_table.scan(
                ProjectionExpression="department_id,department_name",
                FilterExpression=Attr('organization_id').eq(self.org_id)
            )

            for de in dep_response["Items"]:
                dep_id_list.append(str(int(de['department_id']))+','+str(de['department_name']))

            sel_dept_temp=random.choice(dep_id_list).split(',')
            sel_dept=int(sel_dept_temp[0])

            hie_response = hie_table.scan(
                ProjectionExpression="hierarchy",
                FilterExpression=Attr('dep_id').eq(sel_dept)
            )

            while(len(hie_response["Items"])==0):
                sel_dept_temp=random.choice(dep_id_list).split(',')
                sel_dept=int(sel_dept_temp[0])

                hie_response = hie_table.scan(
                    ProjectionExpression="hierarchy",
                    FilterExpression=Attr('dep_id').eq(sel_dept)
                )

            hie_dict=hie_response["Items"][0]['hierarchy']
            hie_updated=hie_dict[1:(len(hie_dict)-1)]
            hie_updated_dict=ast.literal_eval(hie_updated)

            print(hie_updated_dict)

            ind=[]

            j=0
            k=0
            for i in range(len(hie_updated_dict)-2,0,-1):
                if(hie_updated_dict[len(hie_updated_dict)-1]['pid']==hie_updated_dict[i]['pid']):
                    k=k+1
                    if(j==0):
                        ind.append(len(hie_updated_dict)-1)
                        ind.append(i)
                        j=j+1
                    else:
                        ind.append(i)
                else:
                    if(k==0):
                        ind.append(len(hie_updated_dict)-1)
                        break

            emp_id_retrieved=[]
            for i in ind:
                emp_response=emp_table.scan(
                    ProjectionExpression="emp_id",
                    FilterExpression=Attr('org_id').eq(self.org_id) & Attr('hierarchy').eq(hie_updated_dict[i]['hierarchy']) and Attr('department').eq(sel_dept_temp[1])
                )

            while(len(emp_response["Items"])==0):
                sel_dept_temp=random.choice(dep_id_list).strip(',')
                sel_dept=int(sel_dept_temp[0])

                hie_response = hie_table.scan(
                    ProjectionExpression="hierarchy",
                    FilterExpression=Attr('dep_id').eq(sel_dept)
                )

                while(len(hie_response["Items"])==0):
                    sel_dept_temp=random.choice(dep_id_list).split(',')
                    sel_dept=int(sel_dept_temp[0])

                    hie_response = hie_table.scan(
                        ProjectionExpression="hierarchy",
                        FilterExpression=Attr('dep_id').eq(sel_dept)
                    )

                hie_dict=hie_response["Items"][0]['hierarchy']
                hie_updated=hie_dict[1:(len(hie_dict)-1)]
                hie_updated_dict=ast.literal_eval(hie_updated)


                ind=[]

                j=0
                k=0
                for i in range(len(hie_updated_dict)-2,0,-1):
                    if(hie_updated_dict[len(hie_updated_dict)-1]['pid']==hie_updated_dict[i]['pid']):
                        k=k+1
                        if(j==0):
                            ind.append(len(hie_updated_dict)-1)
                            ind.append(i)
                            j=j+1
                        else:
                            ind.append(i)
                    else:
                        if(k==0):
                            ind.append(len(hie_updated_dict)-1)
                            break

                emp_id_retrieved=[]

                for i in ind:
                    emp_response=emp_table.scan(
                        ProjectionExpression="emp_id",
                        FilterExpression=Attr('org_id').eq(self.org_id) & Attr('hierarchy').eq(hie_updated_dict[i]['hierarchy']) and Attr('department').eq(sel_dept_temp[1])
                    )



            for em in emp_response["Items"]:
                emp_id_retrieved.append(int(em['emp_id']))

            cmp_response=cmp_table.scan()

            count={}

            for i in emp_id_retrieved:
                for cmpl in cmp_response["Items"]:
                    if( int(cmpl['emp_id'])==int(i) ):
                        if(j==0):
                            count[int(cmpl['emp_id'])]=1
                        else:
                            count[int(cmpl['emp_id'])]=count[int(cmpl['emp_id'])]+1

            if (len(count)==0):
                emp_id_selected=random.choice(emp_id_retrieved)
                return emp_id_selected,self.cmp_id
            else:
                emp_id_selected=sorted(count.items(),key=operator.itemgetter(1))
                return emp_id_selected[0][0],self.cmp_id

        else:
            dep_response = dep_table.scan(
                ProjectionExpression="department_id,department_name",
                FilterExpression=Attr('organization_id').eq(self.org_id) & Attr('department_id').eq(self.dep_id)
            )

            sel_dept=dep_response['Items'][0]['department_id']

            hie_response = hie_table.scan(
                ProjectionExpression="hierarchy",
                FilterExpression=Attr('dep_id').eq(sel_dept)
            )

            hie_dict=hie_response["Items"][0]['hierarchy']
            hie_updated=hie_dict[1:(len(hie_dict)-1)]
            hie_updated_dict=ast.literal_eval(hie_updated)

            ind=[]

            j=0
            k=0
            for i in range(len(hie_updated_dict)-2,0,-1):
                if(hie_updated_dict[len(hie_updated_dict)-1]['pid']==hie_updated_dict[i]['pid']):
                    k=k+1
                    if(j==0):
                        ind.append(len(hie_updated_dict)-1)
                        ind.append(i)
                        j=j+1
                    else:
                        ind.append(i)
                else:
                    if(k==0):
                        ind.append(len(hie_updated_dict)-1)
                        break

            emp_id_retrieved=[]

            for i in ind:
                emp_response=emp_table.scan(
                    ProjectionExpression="emp_id",
                    FilterExpression=Attr('org_id').eq(self.org_id) & Attr('hierarchy').eq(hie_updated_dict[i]['hierarchy']) and Attr('department').eq(dep_response['Items'][0]['department_name'])
                )


            for em in emp_response["Items"]:
                emp_id_retrieved.append(int(em['emp_id']))

            cmp_response=cmp_table.scan()

            count={}

            for i in emp_id_retrieved:
                j=0
                for cmpl in cmp_response["Items"]:
                    if( int(cmpl['emp_id'])==int(i) ):
                        if(j==0):
                            count[int(cmpl['emp_id'])]=1
                        else:
                            count[int(cmpl['emp_id'])]=count[int(cmpl['emp_id'])]+1

            if (len(count)==0):
                emp_id_selected=random.choice(emp_id_retrieved)
                return emp_id_selected,self.cmp_id
            else:
                emp_id_selected=sorted(count.items(),key=operator.itemgetter(1))
                return emp_id_selected[0][0],self.cmp_id


def formCreateMain(req):
    if "email" in req.session  and  "org_id" in req.session :
        return render(req, "formCreation/form_main.html",{"org_id":req.session["org_id"]})
    return HttpResponseRedirect('/login/')

def testF(req):
    return render(req, "formCreation/form2.html")


def complaintIFrame(req):
    if 'email' in req.session  :
        if req.method == "GET" :
            formId = req.GET["form_id"]
            table = dynamodb.Table('Complaint_forms')
            response1 = table.scan(
                FilterExpression=Attr('form_id').eq(formId)
            )

            if response1["Count"] > 0 :
                form =response1["Items"][0] 
                print(form)
                form0 = json.dumps(form)
                return render(req,'formCreation/iframe0.html',{'form':form0})
                
                
        if req.method == "POST":
            formId = req.POST["form_id"]
            foRm=ComplaintForm(req.POST)
            
            table = dynamodb.Table('Complaint_forms')
            response1 = table.scan(
                FilterExpression=Attr('form_id').eq(formId)
            )

            if response1["Count"] > 0 :
                form =response1["Items"][0] 
                if foRm.is_valid():
                    Complaint00 = {}
                    print(req.POST)
                    for field in form :
                        
                        print(field)
                        if field not in ["form_id" , "org_id" ] :
                            data00 = json.loads(form[field])
                            typE = data00["type"]
                            if typE in ["textfield","datepicker","textarea","radiogroup"] :
                                #if req.POST[field] == "" :
                                    #return render(req,'formCreation/iframe0.html',{'form':form0,"msg":"error"})
                                Complaint00[data00["label"]] = req.POST[field]
                            
                            elif typE == "mobile" :
                                Complaint00[data00["label"]] = req.POST[field+"_0"]+req.POST[field+"_1"]
                            
                            elif typE == "image_Upload" or typE == "file_Upload" :
                                fname = req.session["email"] + datetime.now().strftime("%Y%m%d%H%M")
                                Complaint00[data00["label"]] = fname
                                handle_uploaded_file(req.FILES[field],fname)
                            elif typE == "checkgroup" :
                                print(data00)
                                datum00  = {}
                                i = 0
                                lim = data00['nR']
                                while(i<lim):
                                    datum00[data00['checks'][str(i)]['label']] = req.POST[field+"_"+str(i)]
                                    print("0")
                                    i += 1
                                Complaint00[data00['label']] = json.dumps(datum00)

                                

                        elif field == "form_id":
                            Complaint00["form_id"]  =   req.POST[field]
                        
                        elif field == "org_id" :
                            Complaint00["org_id"] = req.POST[field]
                            orgid=req.POST[field]
                        
                    Complaint00["user_email"] = req.session["email"]
                    Complaint00["complaint_status"] = 0 
                    Complaint00["complaint_timestamp"] = datetime.now().strftime("%Y%m%d%H%M%S")
                    
                    
                    table = dynamodb.Table("ComplaintS")
                    response1 = table.scan()
                    u_id = len(response1['Items'])+1
                    Complaint00["complaint_number"] = "Complaint" + str(u_id)
                    emp_id,cmp_id=assignEmployee(("Complaint" + str(u_id)),orgid).assign()
                    Complaint00["emp_id"]=emp_id
                    table.put_item(
                        Item= Complaint00
                    )
                    return HttpResponseRedirect("/")
                    
                
                form0 = json.dumps(form)

                print(req.POST)
                return render(req,'formCreation/iframe0.html',{'form':form0})
            
    return HttpResponseRedirect('/login/')


       
# Create your views here.



def handle_uploaded_file(f , filename):
    with open(filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

class ComplaintForm(forms.Form):
    print("hello")
