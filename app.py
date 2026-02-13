import streamlit as st
import os
import zipfile
import smtplib
from email.message import EmailMessage
# Importing the logic from your CLI script (assuming you named it mashup_script.py)
# Make sure to change 'mashup_script' to whatever you named Program 1
import importlib.util

# Function to send email
def send_email(receiver_email, zip_filepath):
    sender_email = "your_email@gmail.com" # Replace with your email
    # You will need to generate an App Password in your Google Account settings
    password = "your_app_password_here" 

    msg = EmailMessage()
    msg['Subject'] = 'Your Audio Mashup is Ready!'
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.set_content('Attached is your requested audio mashup.')

    with open(zip_filepath, 'rb') as f:
        file_data = f.read()
        file_name = os.path.basename(zip_filepath)
        
    msg.add_attachment(file_data, maintype='application', subtype='zip', filename=file_name)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, password)
            server.send_message(msg)
        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False

# Streamlit UI
st.title("Audio Mashup Web Service")

with st.form("mashup_form"):
    singer_name = st.text_input("Singer Name", "Sharry Mann")
    num_videos = st.number_input("Number of Videos", min_value=1, value=20)
    duration = st.number_input("Duration of each video (sec)", min_value=1, value=20)
    email_id = st.text_input("Email Id")
    
    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    if not email_id or "@" not in email_id:
        st.error("Please provide a valid email address.")
    else:
        st.info("Processing your mashup... This may take a few minutes.")
        
        output_mp3 = "mashup_output.mp3"
        zip_file = "mashup_output.zip"
        
        try:
            # We can execute the logic directly by calling the system command
            # This calls the script you built in Program 1
            os.system(f'python 102303998.py "{singer_name}" {num_videos} {duration} {output_mp3}')
            
            # Zip the output file
            if os.path.exists(output_mp3):
                with zipfile.ZipFile(zip_file, 'w') as zipf:
                    zipf.write(output_mp3)
                
                st.success("Mashup generated! Sending email...")
                
                # Send the email
                if send_email(email_id, zip_file):
                    st.success("Email sent successfully with the zipped mashup!")
                
                # Cleanup
                os.remove(output_mp3)
                os.remove(zip_file)
            else:
                st.error("Mashup generation failed. Check command line output.")
                
        except Exception as e:
            st.error(f"An error occurred: {e}")