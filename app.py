from flask import Flask,  render_template, request, redirect
import csv
import pandas as pd
import shutil

app = Flask(__name__)

DAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

DURATIONS = [
    "4 week",
    "12 week"
]
@app.route("/")
def index():
    return render_template("index.html", days=DAYS, durations=DURATIONS)

@app.route("/about")
def about():
     return render_template("about.html")

@app.route("/people")
def people():
     return render_template("people.html")

@app.route("/index")
def index2():
    return render_template("index.html", days=DAYS, durations=DURATIONS)

@app.route("/schedule", methods=["POST"])
def schedule():
    #retrieve info from form
    days = []
    days.append(request.form.get("Monday"))
    days.append(request.form.get("Tuesday"))
    days.append(request.form.get("Wednesday"))
    days.append(request.form.get("Thursday"))
    days.append(request.form.get("Friday"))
    days.append(request.form.get("Saturday"))
    days.append(request.form.get("Sunday"))
    while (None) in days:
            days.remove(None)
    if (len(days) < 3):
         return render_template("error.html")
    max = request.form.get("arrowMax")
    duration = request.form.get("duration")
    base = int(int(max)*0.8)

    with open("plan.csv", "w") as csvfile:
        fieldnames = ["Week"]
        for day in days:
             fieldnames.append(day)

        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)

        wBase = ["Base", str(round(base*(0.5))), str(round(base)), str(round(base*(0.3)))]
        for i in range(len(days) - 3):
             wBase.append(str(round(base*(0.4 + (i/10)))))
        writer.writerow(wBase)

        w10 = ["+ 10%", str(round(base*(0.5)*1.1)), str(round(base*1.1)), str(round(base*(0.3)*1.1))]
        for i in range(len(days) - 3):
             w10.append(str(round(int(base*((0.4 + (i/10))*(1.1))))))
        writer.writerow(w10)

        w20 = ["+ 20%", str(round(base*(0.5)*1.25)), str(round(base*1.25)), str(round(int(base*(0.3)*1.25)))]
        for i in range(len(days) - 3):
             w20.append(str(round(int(base*((0.4 + (i/10))*(1.25))))))
        writer.writerow(w20)

        wrec = ["Recovery", str(round(base*(0.5)*0.75)), str(round(base*0.75)), str(round(int(base*(0.3)*0.75)))]
        for i in range(len(days) - 3):
                 wrec.append(str(round(int(base*((0.4 + (i/10))*(0.75))))))
        writer.writerow(wrec)

        #add extra weeks for 12 week program/adding onto 4 week program
        if (duration == "12 week"):
          wb2 = ["Base -> 2", str(round(base*(0.5)*1.15)), str(round(base*1.15)), str(round(int(base*(0.3)*1.15)))]
          for i in range(len(days) - 3):
               wb2.append(str(round(int(base*((0.4 + (i/10))*(1.15))))))
          writer.writerow(wb2)

          secondBase = base * (1.15)

          w10number2 = ["+10% -> 2", str(round(secondBase*(0.5)*1.1)), str(round(secondBase*1.1)), str(round(int(secondBase*(0.3)*1.1)))]
          for i in range(len(days) - 3):
               w10number2.append(str(round(int(secondBase*((0.4 + (i/10))*(1.1))))))
          writer.writerow(w10number2)

          w20number2 = ["+20% -> 2", str(round(secondBase*(0.5)*1.2)), str(round(secondBase*1.2)), str(round(int(secondBase*(0.3)*1.2)))]
          for i in range(len(days) - 3):
               w20number2.append(str(round(int(secondBase*((0.4 + (i/10))*(1.2))))))
          writer.writerow(w20number2)

          wrecnumber2 = ["Recovery -> 2", str(round(secondBase*(0.5)*0.75)), str(round(secondBase*0.75)), str(round(int(secondBase*(0.3)*0.75)))]
          for i in range(len(days) - 3):
               wrecnumber2.append(str(round(int(secondBase*((0.4 + (i/10))*(0.75))))))
          writer.writerow(wrecnumber2)

          base3 = base * (1.1)

          wbase3 = ["Base -> 3", str(round(base3*(0.5)*1)), str(round(base3*1)), str(round(int(base3*(0.3)*1)))]
          for i in range(len(days) - 3):
               wbase3.append(str(round(int(base3*((0.4 + (i/10))*(1))))))
          writer.writerow(wbase3)

          w15 = ["+15% -> 3", str(round(base3*(0.5)*1.15)), str(round(base3*1.15)), str(round(int(base3*(0.3)*1.15)))]
          for i in range(len(days) - 3):
               w15.append(str(round(int(base3*((0.4 + (i/10))*(1.15))))))
          writer.writerow(w15)

          taper = ["Taper -> 3", str(round(base3*(0.5)*0.75)), str(round(base3*0.75)), str(round(int(base3*(0.3)*0.75)))]
          for i in range(len(days) - 3):
               taper.append(str(round(int(base3*((0.4 + (i/10))*(0.75))))))
          writer.writerow(taper)

          comp = ["Competition", "Peak", "Peak", "Peak"]
          for i in range(len(days) - 3):
               comp.append("Peak")
          writer.writerow(comp)
        csvfile.close()

    html_string = '''
    <html>
     <head><title>HTML Pandas Dataframe with CSS</title></head>
     <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
     <link href="static/styles.css" rel="stylesheet">
     <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
     <body class="home">
     <div class="header">
            <img class="logo" src="/static/black-logo.png" alt="Periodic Archery" height="55">
     </div>
     <div class="w3-top w3-bar w3-lightgreen">
            <a href="/index" class="w3-bar-item w3-button">Home</a>
            <a href="/about" class="w3-bar-item w3-button">About</a>
            <a href="/people" class="w3-bar-item w3-button">People</a>
     </div>
     <div>
          <h6 class="name2">Check the <a href="/about">About</a> page to get information on how to make the most out of your plan</h6>
     </div>
     {table}
     <h7 class="cWrite">Copyright © 2023 Samuel Feenane-Levine. All Rights Reserved.</h7>
    </body>
    </html>
    '''
    df = pd.read_csv("plan.csv")
    with open('table.html', 'w') as f:
     f.write(html_string.format(table=df.to_html(classes='table table-bordered border-dark')))

    #df.to_html("table.html", classes='table table-stripped')
    shutil.move("plan.csv", "templates/plan.csv")
    shutil.move("table.html", "templates/table.html")

    if duration == "4 week":
         return render_template("table.html", max=max, days=days, duration=duration)
    if duration == "12 week":
        return render_template("table.html", max=max, days=days, duration=duration)