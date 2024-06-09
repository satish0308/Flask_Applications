from flask import Flask,url_for,render_template,redirect,flash,request
import cv2
import pandas as pd
from Login_Signup import LoginForm,SignupForm
import numpy as np
from yoloapp import predict_and_save_image,process_media
app=Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['STATIC_FOLDER'] = 'static'
app.config['INPUT_FOLDER'] = 'input'

def save_uploaded_image(image_data, filename,input=True):
    static_folder = app.config['INPUT_FOLDER']
    if not os.path.exists(static_folder):
        os.makedirs(static_folder)
    folder,filename =os.path.split(filename)
    input_file = 'input_'+filename    
    image_path = os.path.join(static_folder, input_file)
    print(folder)
    print(image_path)
    print('input_file')
    with open(image_path, 'wb') as f:
        f.write(image_data)
    print('input_file1')

import os

# Load the DataFrame from a CSV file if it exists
if os.path.exists('users.csv'):
    df = pd.read_csv('users.csv')
else:
    df = pd.DataFrame(columns=['username', 'password', 'email'])



@app.route('/')
@app.route('/Home')
def Home():
    return render_template("Home.html",tittle="Home")

@app.route('/About')
def About():
    return render_template('About.html', tittle="About")

@app.route('/Contact')
def Contact():
    return render_template('Contact.html', tittle="Contact")

@app.route('/Services')
def Services():
    return render_template('Services.html', tittle="Services")

@app.route('/Login', methods=['GET', 'POST'])
def Login():
    form = LoginForm()
    if form.validate_on_submit():
        users = df['username'].tolist()  # Using df['username'] instead of df.username
        passwords = df['password'].tolist()
        
        # Print statements for debugging
        print("Submitted username:", form.username.data)
        print("Submitted password:", form.password.data)
        print("Users list:", users)
        
        # Check if username exists
        if form.username.data in users:
            index_number = users.index(form.username.data)
            # Check if password matches
            if form.password.data == passwords[index_number]:
                flash('Login successful!', 'success')
                return redirect(url_for('Dashboard'))  # Redirect to dashboard on successful login
            else:
                flash('Incorrect password. Please try again.', 'danger')
        else:
            flash('Username not found. Please try again or sign up.', 'danger')

    return render_template('Login.html', title="Login", form=form)



@app.route('/SignUp', methods=['GET', 'POST'])
def SignUp():
    form = SignupForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data

        # Check if username already exists
        if username in df['username'].values:
            flash('Username already exists!', 'danger')
        else:
            # Add the user to the DataFrame
            df.loc[len(df.index)] = [username, email,password]

            # Save the DataFrame to a CSV file (optional, for persistence)
            df.to_csv('users.csv', index=False)

            flash('Signup successful!', 'success')
            return redirect(url_for('Login'))  # Redirect to login page
    return render_template('signup.html', title="Sign Up", form=form)



@app.route('/Dashboard')
def Dashboard():
    return render_template('Dashboard.html', tittle="Dashboard")


@app.route('/MyModelYolo',methods=['GET', 'POST']) 
def MyModelYolo():
    return render_template('MyModelYolo.html', tittle="MyModelYolo")

@app.route('/run_yolo', methods=['POST', 'GET'])
def run_yolo():
    output_images = []

    if request.method == 'POST':
        # Check if an image file was uploaded
        print('satish')
        print(request.files)
        if 'image' in request.files and request.files['image'].filename!='' :
            image_file = request.files['image']
        
            image_data = image_file.read()
            # Process the image using OpenCV
            #img = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
            # Perform YOLO detection on the input image
            file_name=image_file.filename
            save_uploaded_image(image_data, str(file_name))
            print('hello')
            folder,base_file_name =os.path.split(file_name)
            print(base_file_name)
            # Set input and output paths
            input_image_path = os.path.join(app.config['INPUT_FOLDER'], 'input_'+str(base_file_name))
            print(input_image_path)
            output_image_path = os.path.join(app.config['STATIC_FOLDER'], 'out_'+str(base_file_name))
            print(output_image_path)
            # Perform YOLO detection and save the output image
            predict_and_save_image(input_image_path, output_image_path)

            # Retrieve output images from the static directory
            for file in os.listdir('static'):
                if file.endswith('.jpg') or file.endswith('.png'):
                    output_images.append(file)
            
            print(output_images)

        # Check if an image folder was uploaded
        elif 'image_folder' in request.files:
            # Process images in the uploaded folder
            image_files = request.files.getlist('image_folder')  # Get list of files
            for image_file in image_files:
                # Read the image file
                image_data = image_file.read()
                file_name = image_file.filename # Ensure safe filename
                save_uploaded_image(image_data, file_name)
                
                folder,base_file_name =os.path.split(file_name)
                print(base_file_name)

                # Set input and output paths
                input_image_path = os.path.join(app.config['INPUT_FOLDER'], 'input_'+str(base_file_name))
                print(input_image_path)
                output_image_path = os.path.join(app.config['STATIC_FOLDER'], 'out_'+str(base_file_name))
                print(output_image_path)

                # Perform YOLO detection and save the output image
                predict_and_save_image(input_image_path, output_image_path)

            # Retrieve output images from the static directory
            for file in os.listdir('static'):
                if file.endswith('.jpg') or file.endswith('.png'):
                    output_images.append(file)
            
            print(output_images)
            
            

        # Check if a video file was uploaded
        elif 'video' in request.files:
            # Read the uploaded video file
            video_file = request.files['video']
            # Process the video file using OpenCV and YOLO
            # output_file = process_video(video_file)
            # output_files.append(output_file)

    return render_template('result.html', output_images=output_images)


if __name__ == '__main__':
    app.run(debug=True)