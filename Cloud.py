import hashlib
import os
import os.path
import sys
import mysql.connector
import random
from datetime import datetime
import datetime
import time
import math
import csv
import random  
import string  

authen = {}
global private_key


with open('test.csv') as pscfile: # for saving the authen list inside test.csv file
     reader = csv.reader(pscfile)
     authen = dict(reader)

i=0

def saveAuthen():# writng authenticated hash  key inside the test.csv file
     with open('test.csv', 'w+') as f:
         for key in authen.keys():
             f.write("%s,%s\n"%(key,authen[key]))

             
def authenticate(doc_id):
     l=int(doc_id)
     x=5
     
     if str(pow(l,x)) in authen.keys(): # a function to authenticate the file in the local system 
          return True
     else:
          return False



def string_auth(key_input):# to hash the private_key for verifying the users integrity
     find_private_key=hashlib.sha512(key_input.encode("utf-8")).hexdigest()
     mydb = mysql.connector.connect(
          host="127.0.0.1",
          user="root",
          password="root@123",
          database="server")

     mycursor = mydb.cursor()
     mycursor.execute("SELECT serial_number FROM hash_server WHERE  string_hash = %s", (find_private_key,))
     key = mycursor.fetchall()

     if(key):
          return True
     else:
          return False
     
               
def docsave():# saving the document inside the server
     
     with open('1serverdocs.txt', 'w') as o:
        original_stdout=sys.stdout
        sys.stdout=o
        for dirpath, dirnames, filenames in os.walk("."):
            for filename in [f for f in filenames if f.endswith("a.docx")]:
                print (os.path.join(filename))
        sys.stdout=original_stdout
        o.close()

     str = open('1serverdocs.txt','r').read()
     result_encrypt=hashlib.sha512(str.encode("utf-8")).hexdigest()
     encrypt=result_encrypt
     
     private_key=''.join((random.choice(string.ascii_lowercase) for x in range(10))) # run loop until the define length
     print(" Your private key is", private_key, " keep it secret ")
     private_key_hash=hashlib.sha512(private_key.encode("utf-8")).hexdigest()

     mydb = mysql.connector.connect(
          host="127.0.0.1",
          user="root",
          password="root@123",
          database="server")

     mycursor = mydb.cursor()
     now = datetime.datetime.now()
     id = 1
     formatted_date = now.strftime('%Y-%m-%d:%H:%M:%S')
     y=encrypt
     c=random.randint(1,1000)
     z=c;
     
     mycursor.execute("insert into hash (pair,location,date_time) VALUES (%s,%s,%s)",(y,z,formatted_date))
     mycursor.execute("insert into hash_server (string_hash) VALUES (%s)",(private_key_hash,))
     mycursor.execute("SELECT  id,location FROM hash WHERE  location = %s", (z,))
     data1 = mycursor.fetchall()
     date2=datetime.datetime.now()
     mydb.commit()

     print("your document is stored and its document id and its location id is ",data1,"it is saved at",date2)
     mycursor.execute("SELECT  id FROM hash WHERE  location = %s", (z,))

     data5=mycursor.fetchall()
     
     local_key=data5[0][0]**5# saving the hash inside the list
     authen[local_key]=date2.strftime("%m/%d/%Y--%H:%M:%S")

def docsearch():# searching the document and fetching it
     doc_id=input("enter your document id ")
     key_input=input("enter your private key,(case senesitive)")
     mydb = mysql.connector.connect(
     host="127.0.0.1",
     user="root",
     password="root@123",
     database="server")
     mycursor = mydb.cursor()

     if(authenticate(doc_id)  and string_auth(key_input)):# if the files's hash is inside the test.csv file, then it will only get fetched by the user, otherwise not
          mycursor.execute("SELECT  id FROM hash WHERE id= %s ", (doc_id,))
          filename= mycursor.fetchall()
          mycursor.execute("SELECT  date_time FROM hash WHERE id= %s ", (doc_id,))
          date=mycursor.fetchall()
          
          date1=datetime.datetime.now()
          now2= datetime.datetime.now()

          id2=1
          formatted_date2=now2.strftime('%Y-%m-%d:%H:%M:%S')
          mycursor.execute("SELECT  last_accessed FROM hash WHERE id= %s ", (doc_id,))
          date4=mycursor.fetchall()

          if(date4[0][0]):
               date4 = date4[0][0].strftime('%Y-%m-%d:%H:%M:%S')

          mycursor.execute("UPDATE hash SET last_accessed=%s WHERE id=%s",(formatted_date2,doc_id,))
          mydb.commit()

          if(filename):
               print(" Document has document id",filename,"and was saved on",date[0][0].strftime('%Y-%m-%d:%H:%M:%S'),"and was previously fetched on",date4,"closing in 5..4..3..2..1")
               time.sleep(5)
               exit()
               
          else:
               print("File not present")
               time.sleep(3)
               exit()
     else:
          print("the given crenedtials are incorrect, file access denied, closing program in 3..2..1..")
          time.sleep(3)
          exit()
          


     
     

if __name__ == "__main__":


     while True:
          print("1. Store a file")
          print("2. Search a file")
          print("3. Exit")
          choice1 = int(input("Enter the Choice:"))

          if choice1 == 1:
               docsave()
               saveAuthen()
               

          elif choice1 == 2:
               docsearch()

          elif choice1==3:
               break
          else:
               print("Invalid choice")

          
     

    
