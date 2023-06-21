import mysql.connector
import subprocess
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Your_password",
    database="database_name"
)

cursor = db.cursor()

query = "SELECT ip_addr FROM links"
cursor.execute(query)
ip_addresses = cursor.fetchall()

for ip_addr in ip_addresses:
    ip_addr = ip_addr[0]  
    print(f"Scanning {ip_addr}...")
    
    command = f"nmap -vv -Pn -F -oX scan_output_{ip_addr}.xml {ip_addr}"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    
    output, _ = process.communicate()
    print(output.decode('utf-8'))
    
    pdf_filename = f"scan_output_{ip_addr}.pdf"

    c = canvas.Canvas(pdf_filename, pagesize=letter)
    
    c.setFont("Helvetica", 12)
    
    lines = output.decode('utf-8').split('\n')
    y = 750
    for line in lines:
        c.drawString(50, y, line)
        y -= 15
    
    c.save()
    
    print(f"Scan report saved as {pdf_filename}")
    
    os.remove(f"scan_output_{ip_addr}.xml")

cursor.close()
db.close()
