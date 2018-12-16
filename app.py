from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
import requests

app=Flask(__name__)
# app.config['DEBUG']=True


app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///D:\\study\\Python\\PythonPrograms\\contact.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    

@app.route('/', methods = ['GET','POST'])
def index():
    if request.method=='POST':
        new_city=request.form.get('city')
        if new_city:
            new_city_obj=City(name=new_city)
            db.session.add(new_city_obj)
            db.session.commit()

    c=City.query.all()
    url='http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&APPID=6cdf12445c7e9aeb333fd66c9ad6cc21'
    weather_data=[]
    for city in c:
        # print(city.name)
        r=requests.get(url.format(city.name)).json()
        
        
        weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon']
        }
        # print(weather)
        weather_data.append(weather)
        # print(weather_data)

    # print(weather_data)
    return render_template('weather.html',weather_data=weather_data)


if __name__ == '__main__':
    app.run(debug=True)

