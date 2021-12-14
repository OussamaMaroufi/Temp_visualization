import datetime
import json
from django.shortcuts import render,redirect
from .forms import UserInputForm

#Request is a library to make calls to the api 
import requests




def Home(request):

    if request.method == 'POST':
        form = UserInputForm(request.POST)
        delta = datetime.timedelta(days=1)
        if form.is_valid():
            start = form.cleaned_data.get('start')
            end = form.cleaned_data.get('end') if form.cleaned_data.get('end') - start <= (delta*7) else start + delta * 7
            lat = form.cleaned_data['latitude']
            lon = form.cleaned_data['longititude']
            print(lat,lon)
            
            
            labels = []
            s = start
            e = end
            while s <= e:
                labels.append(str(s))
                s += delta
            labels =  labels [:7] if len(labels) > 7 else labels
            date_start =datetime.datetime.strptime(str(start), "%Y-%m-%d")
            date_end = datetime.datetime.strptime(str(end+delta),"%Y-%m-%d")

            
            start_timestamp = int(datetime.datetime.timestamp(date_start))
            end_timestamp = int(datetime.datetime.timestamp(date_end))




            
            
            
            
            #Make a call to the api "http://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&start={start}&cnt={cnt}&appid={API key} '
            
            response = requests.get("http://history.openweathermap.org/data/2.5/history/city?lat=%f&lon=%f&type=hour&start=%d&end=%d&appid=f8634aa3de2a12d86e25251370726e02" %(lat,lon,start_timestamp,end_timestamp))
            

            res = json.loads(response.text)
            
            lis_avg = []
            list_avg_max = []
            list_avg_min = []
            
            res["cnt"]
            for i in range(1,res["cnt"],24):

                
                avg_max=0
                avg_min = 0
                avg = 0
                for j in range(i,i+24):
                    
                    avg_max += res["list"][j]["main"]["temp_max"]
                    avg_min += res["list"][j]["main"]["temp_min"]
                    avg += res["list"][j]["main"]["temp"]
                print("average",avg // 24)
                print("average max",avg_max // 24)
                print("average min",avg_min // 24)
                avg_max = (avg_max//24) - 273.15
                avg_min = (avg_min//24) - 273.15
                avg = (avg//24) - 273.15




                lis_avg.append(avg)
                list_avg_max.append(avg_max)
                list_avg_min.append(avg_min)
            






            

            #Here to send data to the graph 
           
            context = {
                "labels":labels,
                "list_avg":lis_avg,
                "list_avg_min":list_avg_min,
                "list_avg_max":list_avg_max,
                "lon":lon,
                "lat":lat
                }
        
            return render(request,'progetto/graph.html',context)

    else:
        form = UserInputForm()

    return render(request,'progetto/index.html',{'form':form})


