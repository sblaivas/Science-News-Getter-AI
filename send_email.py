import os                                        
import smtplib                                    
from email.message import EmailMessage            
from dotenv import load_dotenv                 

load_dotenv()                                     
gmail_address = os.getenv("GMAIL_ADDRESS")        
gmail_app_password = os.getenv("GMAIL_APP_PASSWORD") 

def send_email(subject, body):
    #create an empty email
    msg = EmailMessage()                         
    msg["Subject"] = subject                      
    msg["From"] = gmail_address                   
    msg["To"] = gmail_address                     
    msg.set_content(body)                       
    #debug check
    print(f"Gmail address set: {bool(gmail_address)}, app password length: {len(gmail_app_password or '')}", flush=True)
    
    #first we connect to gmails server
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:  
        #login in
        server.login(gmail_address, gmail_app_password)  
        #send the email  
        server.send_message(msg)  
    #closes connection automatically                

if __name__ == "__main__":
    send_email("Test from Science News Agent", "If you're reading this, email works.")
    print("Sent!")
