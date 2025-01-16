from flask import Flask,render_template, redirect, url_for,request
from flask_sqlalchemy import SQLAlchemy
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
import os
# Ensure a secure filename
from werkzeug.utils import secure_filename
import numpy as np
basedir = os.path.abspath(os.path.dirname("22f000814"))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'CODE/HouseServiceApp.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
class Services(db.Model):
    __tablename__="Services"
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True,nullable=False)
    Service_Name = db.Column(db.String(80), nullable=False)
    Base_Price = db.Column(db.Float, nullable=False)
class Service_Professionals(db.Model):
    __tablename__="Service_Professionals"
    professional_id=db.Column(db.Integer, primary_key=True, autoincrement=True,nullable=False)
    full_name = db.Column(db.String(80))
    password=db.Column(db.String(80),nullable=False)
    email= db.Column(db.String(80),nullable=False)
    address=db.Column(db.String(180), nullable=False)
    pin_code=db.Column(db.Integer,nullable=False)
    age=db.Column(db.Integer,nullable=False)
    Experience=db.Column(db.Float,nullable=False)
    service_provide=db.Column(db.String(80),nullable=False)
    phone_number=db.Column(db.String(80))
    status=db.Column(db.String(80),default="Waiting")
class Customers(db.Model):
    __tablename__="Customers"
    customer_id=db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False)
    full_name = db.Column(db.String(80))
    password=db.Column(db.String(80),nullable=False)
    email= db.Column(db.String(80),nullable=False)
    address=db.Column(db.String(180), nullable=False)
    pin_code=db.Column(db.Integer,nullable=False)
    phone_number=db.Column(db.String(80))
    status=db.Column(db.String(80),default="Unblocked")
class Service_History(db.Model):
    __tablename__="Service_History"
    order_id=db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False)
    full_name = db.Column(db.String(80))
    service_name=db.Column(db.String(80),nullable=False)
    package_id=db.Column(db.Integer,nullable=False)
    professional_name=db.Column(db.String(80))
    phone_number=db.Column(db.String(80))
    action=db.Column(db.String(80),nullable=False,default='Requested')
    request_date=db.Column(db.String(80))

class Today_Services(db.Model):
    __tablename__="Today_Services"
    service_id=db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False)
    customer_id=db.Column(db.Integer,nullable=False)
    customer_name = db.Column(db.String(80),nullable=False)
    phone_number=db.Column(db.String(80))
    service_name=db.Column(db.String(80),nullable=False)
    pacakage_id=db.Column(db.Integer,nullable=False)
    address=db.Column(db.String(80),nullable=False)
    pin_code=db.Column(db.Integer,nullable=False)
    request_date=db.Column(db.String(80))
class Closed_Services(db.Model):
    __tablename__="Closed_Services"
    order_id=db.Column(db.Integer,primary_key=True,nullable=False)
    professional_name=db.Column(db.String(80),nullable=False)
    customer_name = db.Column(db.String(80),nullable=False)
    customer_phone_number=db.Column(db.String(80))
    location=db.Column(db.String(80),nullable=False)
    pincode=db.Column(db.Integer,nullable=False)
    service_date=db.Column(db.String(80),nullable=False)
    rating=db.Column(db.String(80),nullable=False)

class Packages(db.Model):
    __tablename__="Packages"
    service_name=db.Column(db.String(80),nullable=False)
    package_id=db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True)
    package_name=db.Column(db.String(80),nullable=False)
    package_discription=db.Column(db.String(180))
    package_price=db.Column(db.Float, nullable=False)
class Reviews(db.Model):
    __tablename__="Reviews"
    order_id=db.Column(db.Integer,primary_key=True,nullable=False)
    customer_name = db.Column(db.String(80),nullable=False)
    service_name=db.Column(db.String(80),nullable=False)
    description=db.Column(db.String(180))
    date_of_service=db.Column(db.String(80),nullable=False)
    package_id=db.Column(db.Integer,nullable=False)
    professional_name=db.Column(db.String(80),nullable=False)
    phone_number=db.Column(db.String(80))
    service_rating=db.Column(db.String(80),nullable=False)
    remarks=db.Column(db.String(180))
@app.route("/login",methods=["GET","POST"])
def login():
    if(request.method=="POST"):
        email=request.form.get('username')
        password=request.form.get('password')
        customer = Customers.query.filter_by(email=email,password=password,status="Unblocked").one_or_none()
        professional=Service_Professionals.query.filter_by(email=email,password=password,status="Accepted").one_or_none()
        if(customer):
            return redirect(url_for('customers',customer_id=customer.customer_id,customer_name=customer.full_name))
        elif(professional):
            return redirect(url_for('professional',id= professional.professional_id,name=professional.full_name))
        elif(email=="admin123@gmail.com"and password=="123456"):
            return redirect(url_for('admin'))
        else:
            pass
    return render_template('login.html')
@app.route("/signup",methods=["GET","POST"])
def signup():
    if(request.method=="POST"):
        name=request.form.get('name')
        password=request.form.get('password')
        email=request.form.get('email')
        address=request.form.get('address')
        pin_code=request.form.get('pincode')
        phone_number=request.form.get('contact_number')
        customer=Customers(full_name=name,password=password,email=email,address=address,pin_code=pin_code,phone_number=phone_number)
        db.session.add(customer)
        db.session.commit()
        return redirect(url_for('customers',customer_id=customer.customer_id,customer_name=name))
    return render_template('sign-up.html')
@app.route("/register_professional",methods=["GET","POST"])
def register_professional():
    if(request.method=="POST"):
        name=request.form.get('name')
        password=request.form.get('password')
        email=request.form.get('email')
        address=request.form.get('address')
        pin_code=request.form.get('pincode')
        age=request.form.get('Age')
        Experience=request.form.get('Experience')
        service_provide=request.form.get('service')
        phone_number=request.form.get('contact_number')
        resume = request.files['document']
        file_name = secure_filename(f"{name}.pdf")
        file_name=file_name.replace("_"," ")
        file_path = f"CODE/static/{file_name}"
        resume.save(file_path)
        professional=Service_Professionals(full_name=name,password=password,email=email,address=address,pin_code=pin_code,
                                  age=age,Experience=Experience,service_provide=service_provide,phone_number=phone_number)                        
        db.session.add(professional)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('service-professional signup.html')
@app.route("/admin",methods=["GET","POST"])
def admin():
    services = Services.query.all()
    professionals=Service_Professionals.query.all()
    service_request=Service_History.query.all()
    customers=Customers.query.all()
    return render_template('admin.html',services=services,professionals=professionals,service_request=service_request,customers=customers) 
@app.route("/admin_customers",methods=["GET","POST"])
def admin_customers():
    customers=Customers.query.all()
    if(request.method=="POST"):
        values=request.form.get('action')
        values=values.split(',')
        print(values)
        customer_id=int(values[0])
        customer=Customers.query.get(customer_id)
        if(values[1]=="Block"):
            customer.status="Unblocked"
            db.session.commit()
        else:
            customer.status="Blocked"
            db.session.commit()
    return render_template('customers_table.html',customers=customers)
@app.route("/admin_services",methods=["GET","POST"])
def admin_services():
    if(request.method=="POST"):
        action=request.form.get('action')
        if(action=='action3'):
             return render_template('add_services.html')
        else:
            name=request.form.get("name")
            price=request.form.get("price")
            service=Services(Service_Name=name,Base_Price=price)
            db.session.add(service)
            db.session.commit()
    services = Services.query.all()
    return render_template('services_table.html',services=services) 
@app.route("/admin_professionals",methods=["GET","POST"])
def admin_professionals():
    professionals=Service_Professionals.query.all()
    return render_template('professionals_table.html',professionals=professionals)
@app.route("/admin_services_requested")
def admin_services_requested():
    service_request=Service_History.query.all()
    return render_template('requests_table.html',service_request=service_request)
@app.route("/edit_services/<int:service_id>",methods=["GET","POST"])
def edit_services(service_id):
    action=request.form.get('action')
    service=Services.query.get(service_id)
    if(action=='action1'):
        return render_template('edit_service_details.html',service=service)
    elif(action=='action2'):
        packages=Packages.query.filter_by(service_name=service.Service_Name).all()
        for package in packages:
            db.session.delete(package)
            db.session.commit()
        db.session.delete(service)
        db.session.commit()
        return redirect(url_for('admin_services'))
    elif(action=='action4'):
        service.Service_Name=request.form.get('name')
        service.Base_Price=request.form.get('price')
        db.session.commit()
        return redirect(url_for('admin_services'))
    elif(action=='action5'):
        return render_template('add_package.html',service=service)
    else:
        service_name=service.Service_Name
        package_name=request.form.get('name')
        package_discription=request.form.get('discription')
        package_price=request.form.get('price')
        add_package=Packages(service_name=service_name,package_name=package_name,package_discription=package_discription,package_price=package_price)
        db.session.add(add_package)
        db.session.commit()
        return redirect(url_for('admin_services'))
@app.route("/edit/<int:professional_id>/<string:name>",methods=["GET","POST"])
def edit(professional_id,name):
    action=request.form.get('action')
    professional=Service_Professionals.query.get(professional_id)
    if(action=='approve'):
        professional.status="Accepted"
        db.session.commit()
    else:
        db.session.delete(professional)
        db.session.commit()
    return redirect(url_for('admin_professionals'))
@app.route("/admin/search",methods=["GET","POST"])
def admin_search():
    package=[]
    professionals=[]
    if(request.method=="POST"):
        service=request.form.get('service')
        specification=request.form.get('name')
        if(service=='service_status'):
            package=Service_History.query.filter_by(action=specification).all()
        elif(service=='service_request'):
            package = Service_History.query.filter_by(service_name=specification).all()
        else:
            professionals=Service_Professionals.query.filter_by(service_provide=specification).all()
        return(render_template("admin_search.html",package=package,professionals=professionals))
    return(render_template("admin_search.html",package=package,professionals=professionals))
@app.route("/admin/summary")
def admin_summary():
    service_professional=Service_Professionals.query.all()
    service_history=Service_History.query.all()
    closed_service=Closed_Services.query.all()
    dict={}
    for prof in service_history:
        if prof.professional_name not in dict.keys():
            if prof.professional_name != None:
                dict[prof.professional_name]=1
        else:
            dict[prof.professional_name]+=1
    categories=dict.keys()
    print (categories)
    service_counts=list(dict.values())
    print(service_counts)
    # Generate the chart
    fig, ax = plt.subplots(figsize=(16,4))
    bars = ax.bar(categories, service_counts, color=['green', 'blue', 'red'], edgecolor='black')
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2,
                f'{bar.get_height()}', ha='center', fontsize=12)
    ax.set_title('Professionals Summary', fontsize=16, fontweight='bold')
    ax.set_xlabel('Professional Name', fontsize=12)
    ax.set_ylabel('Number of Services', fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Save the chart as an image file
    image_path = 'CODE/static/admin1.png'
    plt.savefig(image_path)
    plt.close(fig)  # Close the figure to free resources
    # Generate the chart
    rating=['1','2','3','4','5']
    rating_count=[0,0,0,0,0]
    for service in closed_service:
        if (service.rating=='1'):
            rating_count[0]+=1
        elif(service.rating=='2'):
            rating_count[1]+=1
        elif(service.rating=='3'):
            rating_count[2]+=1
        elif(service.rating=='4'):
            rating_count[3]+=1
        else:
            rating_count[4]+=1
    fig, ax = plt.subplots(figsize=(6,4))
    bars = ax.bar(rating,rating_count, color=['green', 'blue', 'red'], edgecolor='black')
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2,
                f'{bar.get_height()}', ha='center', fontsize=12)
    ax.set_title('Ratings Summary', fontsize=16, fontweight='bold')
    ax.set_xlabel('Ratings', fontsize=12)
    ax.set_ylabel('Rate of Ratings', fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    # Save the chart as an image file
    image_path = 'CODE/static/admin2.png'
    plt.savefig(image_path)
    plt.close(fig)  # Close the figure to free resources
    return render_template('admin_summary.html')
@app.route('/customers/<int:customer_id>/<string:customer_name>')
def customers(customer_id,customer_name):
    print(customer_name)
    service_history=Service_History.query.filter_by(full_name=customer_name).all()
    services=Services.query.all()
    print(service_history)
    return render_template("customers.html",customer_id=customer_id,customer_name=customer_name,service_history=service_history,services=services)
@app.route('/packages/<int:customer_id>/<string:customer_name>/<string:service_name>',methods=["GET","POST"])
def packages(customer_id,customer_name,service_name):
    package=Packages.query.filter_by(service_name=service_name).all()
    if(request.method=="POST"):
        package_id=request.form.get("action")
        date=request.form.get("date")
        instance=Customers.query.get(customer_id)
        service_history=Service_History(full_name=customer_name,service_name=service_name,package_id=package_id,request_date=date)
        db.session.add(service_history)
        db.session.commit()
        today_service=Today_Services(customer_id=customer_id,customer_name=customer_name,service_name=service_name,pacakage_id=package_id,phone_number=instance.phone_number,
                                    address=instance.address,pin_code=instance.pin_code,request_date=date)
        db.session.add(today_service)
        db.session.commit()
        return redirect(url_for('customers',customer_id=customer_id,customer_name=customer_name))
    return render_template('packages.html',customer_id=customer_id,customer_name=customer_name,service_name=service_name,package=package)
@app.route('/customer_search/<int:customer_id>/<string:customer_name>',methods=["GET","POST"])
def customer_search(customer_id,customer_name):
    package=[]
    if(request.method=="POST"):
        service=request.form.get('service')
        specification=request.form.get('name')
        if(service=='service_name'):
            package=Packages.query.filter_by(service_name=specification).all()
            return render_template('customer_search.html',customer_id=customer_id,customer_name=customer_name,package=package)
        elif(service=='price'):
            price=float(specification)
            package = Packages.query.filter(Packages.package_price <= price).all()
            return render_template('customer_search.html',customer_id=customer_id,customer_name=customer_name,package=package)
    return render_template('customer_search.html',customer_id=customer_id,customer_name=customer_name,package=package)
@app.route('/customers/<int:customer_id>/<string:customer_name>/summary')
def summary(customer_id,customer_name):
 # Data for the chart
    categories = ['Requested', 'Closing?', 'Closed']
    service_history=Service_History.query.filter_by(full_name=customer_name).all()
    service_counts = [0, 0, 0]  # Replace with dynamic database values if needed
    service_details={}
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']  # Custom colors
    for service in service_history:
        if(service.action=='Requested'):
            service_counts[0]+=1
        elif(service.action=='Closing?'):
            service_counts[1]+=1
        else:
            service_counts[2]+=1
    # labels = ['Cleaning', 'Plumbing', 'Gardening', 'Electrical']
    #sizes = [30, 25, 20, 25]  # Percentages or counts
    for service in service_history:
        if service.service_name not in service_details.keys():
            service_details[service.service_name]=1
        else:
            service_details[service.service_name]+=1
    sizes=list(service_details.values())
    # Create the pie chart
    plt.pie(
        sizes, 
        labels=service_details.keys(), 
        colors=colors, 
        autopct='%1.1f%%', 
        shadow=True, 
        startangle=140
    )
    # Title for the pie chart
    plt.title('Service Distribution')

    # Display the chart
    plt.axis('equal')  # Ensures the pie chart is a circle
    pie_chart='CODE/static/pie_chart.png'
    plt.savefig(pie_chart)
    plt.close()
    # Generate the chart
    fig, ax = plt.subplots(figsize=(6,4))
    bars = ax.bar(categories, service_counts, color=['green', 'blue', 'red'], edgecolor='black')
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2,
                f'{bar.get_height()}', ha='center', fontsize=12)
    ax.set_title('Service Requests Summary', fontsize=16, fontweight='bold')
    ax.set_xlabel('Service Status', fontsize=12)
    ax.set_ylabel('Number of Requests', fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Save the chart as an image file
    image_path = 'CODE/static/chart_image.png'
    plt.savefig(image_path)
    plt.close(fig)  # Close the figure to free resources

    # Pass the image path to the template
    return render_template('customer_summary.html', chart_image=image_path,customer_name=customer_name,customer_id=customer_id,pie_chart=pie_chart)
@app.route('/customers/<int:customer_id>/<string:customer_name>/<int:service_details>/reviews',methods=["GET","POST"])
def review(customer_id,customer_name,service_details):
    service=Service_History.query.filter_by(order_id=service_details).one_or_none()
    package_details=Packages.query.filter_by(package_id=service.package_id).one_or_none()
    if(request.method=="POST"):
        button_val=request.form.get('action')
        if(button_val=="Submit"):
            order_id=service_details
            customer_name =customer_name
            service_name=service.service_name
            description=request.form.get('description')
            date_of_service=str(request.form.get('date'))
            package_id=service.package_id
            professional_name=service.professional_name
            phone_number=service.phone_number
            service_rating=request.form.get('service_rating')
            remarks=request.form.get("remarks")
            review=Reviews(order_id=order_id,customer_name=customer_name,service_name=service_name,description=description,
                        date_of_service=date_of_service,package_id=package_id,professional_name=professional_name,phone_number=phone_number,
                        service_rating=service_rating,remarks=remarks)
            db.session.add(review)
            db.session.commit()
            service.action="Closed"
            db.session.commit()
            customer=Customers.query.filter_by(customer_id=customer_id).one_or_none()
            closed_service=Closed_Services(order_id=service_details,professional_name=professional_name,customer_name = customer_name,
                                        customer_phone_number=customer.phone_number,location=customer.address,
                                        pincode=customer.pin_code,service_date=date_of_service,rating=service_rating)
            db.session.add(closed_service)
            db.session.commit()
            return redirect(url_for('customers',customer_id=customer_id,customer_name=customer_name))
    return render_template("customer_reviews.html",customer_name=customer_name,service_details=service,package_details=package_details,customer_id=customer_id)
@app.route('/professional/<int:id>/<string:name>',methods=["GET","POST"])
def professional(id,name):
    professional=Service_Professionals.query.filter_by(professional_id=id).one_or_none()
    service_details=Today_Services.query.all()
    closed_services=Closed_Services.query.all()
    if(request.method=="POST"):
        raw_value=request.form.get("action")
        print(raw_value)
        values = raw_value.split(',')  # Convert the string into a lis
        print(values)
        professional=Service_Professionals.query.get(id)
        history_update=Service_History.query.filter_by(full_name=values[0],service_name=values[1],package_id=values[2],action="Requested").one_or_none()
        history_update.professional_name=professional.full_name
        history_update.phone_number=professional.phone_number
        history_update.action="Closing?"
        db.session.commit()
        delete_instance=Today_Services.query.filter_by(customer_name=values[0],service_name=values[1],pacakage_id=values[2]).one_or_none()
        db.session.delete(delete_instance)
        db.session.commit()
        return (redirect(url_for('professional',id=id,name=name)))
    return(render_template('professionals.html',id=id,name=name,service_details=service_details,closed_services=closed_services,service_name=professional.service_provide))
@app.route('/professional/<int:id>/<string:name>/summary')
def summary_professional(id,name):
    service_professional=Service_Professionals.query.get(id)
    today_service=list(Today_Services.query.filter_by(service_name=service_professional.service_provide))
    service_history=(Service_History.query.filter_by(service_name=service_professional.service_provide,professional_name=name))
    closed_service=list(Closed_Services.query.filter_by(professional_name=name))
    available_services=len(today_service)
    closed_services=len(closed_service)
    in_progress=0
    for service in service_history:
        if(service.action!="Closed"):
            in_progress+=1
    categories=['Available','InProgress','Closed']
    service_counts=[available_services,in_progress,closed_services]
    # Generate the chart
    fig, ax = plt.subplots(figsize=(6,4))
    bars = ax.bar(categories, service_counts, color=['green', 'blue', 'red'], edgecolor='black')
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2,
                f'{bar.get_height()}', ha='center', fontsize=12)
    ax.set_title('Service Requests Summary', fontsize=16, fontweight='bold')
    ax.set_xlabel('Service Status', fontsize=12)
    ax.set_ylabel('Number of Requests', fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Save the chart as an image file
    image_path = 'CODE/static/professional_summary.png'
    plt.savefig(image_path)
    plt.close(fig)  # Close the figure to free resources
    # Generate the chart
    rating=['1','2','3','4','5']
    rating_count=[0,0,0,0,0]
    for service in closed_service:
        if (service.rating=='1'):
            rating_count[0]+=1
        elif(service.rating=='2'):
            rating_count[1]+=1
        elif(service.rating=='3'):
            rating_count[2]+=1
        elif(service.rating=='4'):
            rating_count[3]+=1
        else:
            rating_count[4]+=1
    fig, ax = plt.subplots(figsize=(6,4))
    bars = ax.bar(rating,rating_count, color=['green', 'blue', 'red'], edgecolor='black')
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2,
                f'{bar.get_height()}', ha='center', fontsize=12)
    ax.set_title('Ratings Summary', fontsize=16, fontweight='bold')
    ax.set_xlabel('Ratings', fontsize=12)
    ax.set_ylabel('Rate of Ratings', fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    # Save the chart as an image file
    image_path = 'CODE/static/professional_summary1.png'
    plt.savefig(image_path)
    plt.close(fig)  # Close the figure to free resources
    return render_template('professional_summary.html',id=id,name=name,service_name=service_professional.service_provide)
@app.route('/professional/<int:id>/<string:name>/search',methods=["GET","POST"])
def professional_search(id,name):
    package=[]
    professional=Service_Professionals.query.get(id)
    if(request.method=="POST"):
        service=request.form.get('service')
        specification=request.form.get('name')
        if(service=='service_name'):
            package=Today_Services.query.filter_by(pin_code=specification).all()
        else:
            package=Today_Services.query.filter_by(request_date=specification).all()
        render_template('professional_search.html',id=id,name=name,package=package,service_name=professional.service_provide)
    return render_template('professional_search.html',id=id,name=name,package=package,service_name=professional.service_provide)
if __name__ == '__main__':
    app.run(debug=True,port=5050)