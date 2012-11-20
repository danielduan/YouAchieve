import re
import cgi
import csv
import os
import datetime
import urllib
import webapp2
import time

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers


class SchoolEntry(db.Model):
    name = db.StringProperty()
    s_id = db.IntegerProperty()

def schoolList_key(schoolList_name=None):
  #give back the key of school List
  return db.Key.from_path('schoolList', schoolList_name or 'schoolList_default')

class SchoolEntity(webapp2.RequestHandler):
  def get(self):
	#couple of random schools to put in atm
      schoolList = SchoolEntry.gql("WHERE ANCESTOR IS :1 ORDER BY name",
                            schoolList_key("colleges"))
      checkEmpty = 5
      for i, school in enumerate(schoolList):
         if (i > 0):
           checkEmpty = 1
      
      if (checkEmpty == 0):
        s1 = SchoolEntry(parent=schoolList_key("colleges"))
        s1.name = "UCLA"
        s1.s_id = "01"
        s1.put()
        s2 = SchoolEntry(parent=schoolList_key("colleges"))
        s2.name = "USC"
        s2.s_id = "02"
        s2.put()
        s3 = SchoolEntry(parent=schoolList_key("colleges"))
        s3.name = "Caltech"
        s3.s_id = "03"
        s3.put()
        s4 = SchoolEntry(parent=schoolList_key("colleges"))
        s4.name = "Berkeley"
        s4.s_id = "04"
        s4.put()
        s5 = SchoolEntry(parent=schoolList_key("colleges"))
        s5.name = "MIT"
        s5.s_id = "05"
        s5.put()

#      ifile = open("schoollist.csv", "rb")
      blob_reader = blobstore.BlobReader(key, buffer_size=1048576)
#      ifile = blob_reader.read()
      reader = csv.reader(blob_reader)

      count = 0
      for school in schoolList:
        count += 1
      if count < 2:
        rownum = 0
        for row in reader:
            header = row
            colnum = 0
            schoolentry = SchoolEntry(parent=schoolList_key("colleges"))
            for col in row:
                 if colnum == 0:
                    schoolentry.s_id = rownum
                    schoolentry.name = col
                 colnum += 1
                 schoolentry.put()
            rownum += 1
     # ifile.close() 
      self.response.write("{\"colleges\": [")
      schoolList = SchoolEntry.gql("WHERE ANCESTOR IS :1 ORDER BY name",
                             schoolList_key("colleges"))
      	
      for i, school in enumerate(schoolList):
        if (i == 0):
          self.response.write("{\"Name\": ")
        else:
          self.response.write(", {\"Name\": ")
        self.response.write("\"" + school.name + "\", ")
        self.response.write("\"School id\": ")
        self.response.write("\"" + str(school.s_id) + "\"}")
      self.response.write("]}")	

class DeadlineEntry(db.Model):
    deadline1 = db.DateProperty()
    deadline2 = db.DateProperty()
    deadline3 = db.DateProperty()
    s_id = db.IntegerProperty()

class DeadlineEntity(webapp2.RequestHandler):
    def get(self):
	#couple of random schools to put in atm
#      ifile = open("schoollist.csv", "rb")
      blob_reader = blobstore.BlobReader(key, buffer_size=1048576)
      reader = csv.reader(blob_reader)
      deadlineList = DeadlineEntry.gql("WHERE ANCESTOR IS :1 ORDER BY s_id ASC",schoolList_key("deadlines"))
      count = 0
      for deadline in deadlineList:
        count += 1;
      if count < 2:
        rownum = 0
        for row in reader:
            colnum = 0
            deadlineentry = DeadlineEntry(parent=schoolList_key("deadlines"))
            deadlineentry.s_id = rownum
            for col in row:
	     if col == "":
	       if colnum == 1:
	          deadlineentry.deadline1 = datetime.date(5000, 1, 1)
	       if colnum == 2:
	          deadlineentry.deadline2 = datetime.date(5000, 1, 1)
	     else:	  
	      if col[0].isalpha():
                 if colnum == 1:
                       deadlineentry.deadline1 = datetime.date(5000, 1, 1)
                 if colnum == 2:
                       deadlineentry.deadline2 = datetime.date(5000, 1, 1)
                 if colnum == 3:
                    deadlineentry.deadline3 = datetime.date(3000, 1, 1)
	      else:
	        d = re.split('[/ ,]', col)
		if colnum == 1:
		   if d[0] == '1':
		      deadlineentry.deadline1 = datetime.date(2013,int(d[0]),int(d[1]))
		   else:
		    if d[0] == '2':
		      deadlineentry.deadline1 = datetime.date(2013, int(d[0]), int(d[1]))
		    else:
		     if d[0] == '3':
		      deadlineentry.deadline1 = datetime.date(2013, int(d[0]), int(d[1]))
		     else:
		      deadlineentry.deadline1 = datetime.date(2012, int(d[0]), int(d[1]))
		if colnum == 2:
                   if d[0] == '1':
		      deadlineentry.deadline2 = datetime.date(2013, int(d[0]), int(d[1]))
		   else:
		    if d[0] == '2':
                      deadlineentry.deadline2 = datetime.date(2013, int(d[0]),int( d[1]))
		    else:
		     if d[0] == '3':
                      deadlineentry.deadline2 = datetime.date(2013, int(d[0]), int(d[1]))
		     else:
		      deadlineentry.deadline2 = datetime.date(2012, int(d[0]), int(d[1]))
		if colnum == 3:
		   if d[0] =='1':
		      deadlineentry.deadline3 = datetime.date(2013, int(d[0]), int(d[1]))
		   else:
		    if d[0] == '2':
		      deadlineentry.deadline3 = datetime.date(2013, int(d[0]), int(d[1]))
		    else:
		     if d[0] == '3':
		      deadlineentry.deadline3 = datetime.date(2013, int(d[0]), int(d[1]))
		     else:
		      deadlineentry.deadline3 = datetime.date(2012, int(d[0]), int(d[1]))
	     colnum += 1
            deadlineentry.put()
            rownum += 1
#      ifile.close()
      request_id = self.request.get('id')
      if (request_id == ""):
        deadlineList = DeadlineEntry.gql("WHERE ANCESTOR IS :1",
                                     schoolList_key("deadlines"))
      else:
        deadlineList = DeadlineEntry.gql("WHERE ANCESTOR IS :1 AND s_id = " + request_id,
                             schoolList_key("deadlines"))

      self.response.write("{\"Deadlines\" : ")	
      for i, deadline in enumerate(deadlineList):
            if (i == 0):
	       self.response.write("{\"Early Decision\": ")
            else:
              self.response.write(", {\"Early Decision\": ")
            self.response.write("\"" + str(deadline.deadline1) + "\", ")
            self.response.write("\"Early Action\": ")
            self.response.write("\"" + str(deadline.deadline2) + "\", ")
            self.response.write("\"Regular Admission\": ")
            self.response.write("\"" + str(deadline.deadline3) + "\", ")
      d1 = deadline.deadline1 - datetime.date.today()	    
      self.response.write("\"Early Decision Countdown\": \"%s" % d1.days + "\", ")
      d2 = deadline.deadline2 - datetime.date.today()
      self.response.write("\"Early Action Countdown\": \"%s" % d2.days + "\", ")
      d3 = deadline.deadline3 - datetime.date.today()
      self.response.write("\"Regular Admission Countdown\": \"%s" % d3.days + "\"}}")

class agEntry(db.Model):
    fulfillment = db.ListProperty(bool)
    user_id = db.StringProperty()

class agEntity(webapp2.RequestHandler):
    def get(self):
	#couple of random schools to put in atm
      request_id = self.request.get('id')	
      agList = agEntry.gql("WHERE ANCESTOR IS :1",
                             schoolList_key("agReqs"))
      checkEmpty = 0
      for i, deadline in enumerate(agList):
        if (i > 0):
          checkEmpty = 1
      if (checkEmpty == 0):
        s1 = agEntry(parent=schoolList_key("agReqs"))
        s1.fulfillment = [True, False, True, True, False, False, False, False, True, False, False, True, False, False, True, False, False, False, True, True, False, True, True, False]
        s1.user_id = "01"
        s1.put()
        s2 = agEntry(parent=schoolList_key("agReqs"))
        s2.fulfillment = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        s2.user_id = "02"
        s2.put()
      userList = agEntry.gql("WHERE ANCESTOR IS :1 AND user_id = \'" + request_id + "\'",
                             schoolList_key("agReqs"))


#List of classes to consider:
#0. Eng year 1
#1. Eng year 2
#2. Eng year 3
#3. Eng year 4
#4. Sci year 1
#5. Sci year 2
#6. Sci year 3
#7. Foreign year 1
#8. Foreign year 2
#9. Foreign year 3
#10. Algebra II
#11. Geometry
#12. Math Year 1
#13. Math year 2
#14. Math year 3
#15. Soc year 1
#16. Soc year 2
#17. US History
#18. World History
#19. Visual Arts
#20. Elective
#21. Physics
#22. Chem
#23. Bio
      for user in userList:
        self.response.write("{\"English_1\": ")
        self.response.write("\"" + str(user.fulfillment[0]) + "\", ")
        self.response.write("\"English_2\": ")
        self.response.write("\"" + str(user.fulfillment[1]) + "\", ")
        self.response.write("\"English_3\": ")
        self.response.write("\"" + str(user.fulfillment[2]) + "\", ")
        self.response.write("\"English_4\": ")
        self.response.write("\"" + str(user.fulfillment[3]) + "\", ")
        self.response.write("\"Science_(Year_1)\": ")
        self.response.write("\"" + str(user.fulfillment[4]) + "\", ")
        self.response.write("\"Science_(Year_2)\": ")
        self.response.write("\"" + str(user.fulfillment[5]) + "\", ")
        self.response.write("\"Science_(Year_3)\": ")
        self.response.write("\"" + str(user.fulfillment[6]) + "\", ")
        self.response.write("\"Foreign_Language_(Year_1)\": ")
        self.response.write("\"" + str(user.fulfillment[7]) + "\", ")        
        self.response.write("\"Foreign_Language_(Year_2)\": ")
        self.response.write("\"" + str(user.fulfillment[8]) + "\", ")
        self.response.write("\"Foreign_Language_(Year_3)\": ")
        self.response.write("\"" + str(user.fulfillment[9]) + "\", ")
        self.response.write("\"Algebra_II\": ")
        self.response.write("\"" + str(user.fulfillment[10]) + "\", ")
        self.response.write("\"Geometry\": ")
        self.response.write("\"" + str(user.fulfillment[11]) + "\", ")
        self.response.write("\"Math_(Year_1)\": ")
        self.response.write("\"" + str(user.fulfillment[12]) + "\", ")
        self.response.write("\"Math_(Year_2)\": ")
        self.response.write("\"" + str(user.fulfillment[13]) + "\", ")
        self.response.write("\"Math_(Year_3)\": ")
        self.response.write("\"" + str(user.fulfillment[14]) + "\", ")
        self.response.write("\"US_History\": ")
        self.response.write("\"" + str(user.fulfillment[15]) + "\", ")
        self.response.write("\"World_History\": ")
        self.response.write("\"" + str(user.fulfillment[16]) + "\", ")
        self.response.write("\"Visual/Performing_Arts\": ")
        self.response.write("\"" + str(user.fulfillment[17]) + "\", ")
        self.response.write("\"Elective\": ")
        self.response.write("\"" + str(user.fulfillment[18]) + "\", ")
        self.response.write("\"Biology\": ")
        self.response.write("\"" + str(user.fulfillment[19]) + "\", ")
        self.response.write("\"Chemistry\": ")
        self.response.write("\"" + str(user.fulfillment[20]) + "\", ")
        self.response.write("\"Physics\": ")
        self.response.write("\"" + str(user.fulfillment[21]) + "\"}")


class sat1Entry(db.Model):
    testDates = db.ListProperty(str)
    writeScore = db.ListProperty(int)
    readScore = db.ListProperty(int)
    mathScore = db.ListProperty(int)
    user_id = db.StringProperty()

class sat1Entity(webapp2.RequestHandler):
    def get(self):
      #couple of random schools to put in atm
      sat1List = sat1Entry.gql("WHERE ANCESTOR IS :1",
                             schoolList_key("SAT1s"))
      checkEmpty = 0
      for i, test in enumerate(sat1List):
        if (i > 0):
          checkEmpty = 1
      if (checkEmpty == 0):
        s1 = sat1Entry(parent=schoolList_key("SAT1s"))
        s1.testDates = ["9/30"]
        s1.writeScore =[720]
        s1.readScore = [600]
        s1.mathScore = [750]
        s1.user_id = "01"
        s1.put()
        s2 = sat1Entry(parent=schoolList_key("SAT1s"))
        s2.testDates = ["9/30", "10/21"]
        s2.writeScore =[700, 720]
        s2.readScore = [550, 560]
        s2.mathScore = [800, 780]
        s2.user_id = "02"
        s2.put()
      request_id = self.request.get('id')	
      sat1List = sat1Entry.gql("WHERE ANCESTOR IS :1 AND user_id = \'" + request_id + "\'",
                             schoolList_key("SAT1s"))
      
      self.response.write("{\"SATI_scores\" : [")
      for user in sat1List:
        for i, date in enumerate((user.testDates)):
          if (i == 0):
            self.response.write("{\"Date\": ")
          else:
            self.response.write(", {\"Date\": ")
          self.response.write("\"" + user.testDates[i] + "\", ")
          self.response.write("\"Writing_Score\": ")
          self.response.write("\"" + str(user.writeScore[i]) + "\", ")
          self.response.write("\"Reading_Score\": ")
          self.response.write("\"" + str(user.readScore[i]) + "\", ")
          self.response.write("\"Math_Score\": ")
          self.response.write("\"" + str(user.mathScore[i]) + "\"}")
        self.response.write("]}")

class sat2Entry(db.Model):
    testDates = db.ListProperty(str)
    testSubjects = db.ListProperty(str)
    scores = db.ListProperty(int)
    user_id = db.StringProperty()

class sat2Entity(webapp2.RequestHandler):
    def get(self):
      #couple of random schools to put in atm
      sat2List = sat2Entry.gql("WHERE ANCESTOR IS :1",
                             schoolList_key("SAT2s"))
      checkEmpty = 0
      for i, test in enumerate(sat2List):
        if (i > 0):
          checkEmpty = 1
      if (checkEmpty == 0):
        s1 = sat2Entry(parent=schoolList_key("SAT2s"))
        s1.testDates = ["9/30"]
        s1.testSubjects =["Math IIC"]
        s1.scores = [800]
        s1.user_id = "01"
        s1.put()
        s2 = sat2Entry(parent=schoolList_key("SAT2s"))
        s2.testDates = ["9/30", "10/21"]
        s2.testSubjects =["Physics", "Math I"]
        s2.scores = [550, 560]
        s2.user_id = "02"
        s2.put()
      request_id = self.request.get('id')	
      sat2List = sat2Entry.gql("WHERE ANCESTOR IS :1 AND user_id = \'" + request_id + "\'",
                             schoolList_key("SAT2s"))
      
      self.response.write("{\"SATII_scores\" : [")
      for user in sat2List:
        for i, date in enumerate((user.testDates)):
          if (i == 0):
            self.response.write("{\"Date\": ")
          else:
            self.response.write(", {\"Date\": ")
          self.response.write("\"" + user.testDates[i] + "\", ")
          self.response.write("\"Subject\": ")
          self.response.write("\"" + str(user.testSubjects[i]) + "\", ")
          self.response.write("\"Score\": ")
          self.response.write("\"" + str(user.scores[i]) + "\"}")
        self.response.write("]}")

class AddForm(webapp2.RequestHandler):
   def get(self):
       self.response.out.write("""
        <html>
           <body>
              <form action="/addschool" method="post">
              <p>School Name: <input type="text" name="name"> </p>
              <p>Early Decision: <input type="text" name="deadline1"></p>
              <p>Early Action: <input type="text" name="deadline2"></p>
              <p>Regular Admission: <input type="text" name="deadline3"></p>
             <div><input type="submit" value="Submit"></div>
              </form>
            </body>
        </html>""")
         
class AddSchool(webapp2.RequestHandler):
   def post(self):
     schoolList = SchoolEntry.gql("WHERE ANCESTOR IS :1 ORDER BY name ASC", schoolList_key("colleges"))
     schoolentry = SchoolEntry(parent=schoolList_key("colleges"))
     num = 0

     #quick check for existing College - if exists, update
     #q = db.Query(SchoolEntry)
     #q = SchoolEntry.all()
     #q.filter('name =', cgi.escape(self.request.get('name')))
     #result = q.get()
     #result.deadline1 = cgi.escape(self.request.get('deadline1'))
     #result.deadline2 = cgi.escape(self.request.get('deadline2'))
     #result.deadline3 = cgi.escape(self.request.get('deadline3'))
     #result.put()

     for school in schoolList:
       num += 1
     schoolentry.s_id = num
     name = cgi.escape(self.request.get('name'))
     schoolentry.name = name
     schoolentry.put()
 
     deadlineList = DeadlineEntry.gql("WHERE ANCESTOR IS :1 ORDER BY deadline1 DESC",schoolList_key("deadlines"))
     deadlineentry = DeadlineEntry(parent=schoolList_key("deadlines"))
     deadlineentry.s_id = num
     deadline1 = cgi.escape(self.request.get('deadline1'))
     deadlineentry.deadline1 = deadline1
     deadline2 = cgi.escape(self.request.get('deadline2'))
     deadlineentry.deadline2 = deadline2
     deadline3 = cgi.escape(self.request.get('deadline3'))
     deadlineentry.deadline3 = deadline3
     deadlineentry.put()
     #self.response.out.write("%s has been successfully added!" % name)

class EditAGForm(webapp2.RequestHandler):
   def get(self):
       self.response.out.write("""
        <html>
            <body>
              <form action="/editAG" method="post">
              <p>User ID: <input type="text" name="id"> </p>
              <p>Subject: <input type="text" name="req_name"></p>
              <div><input type="submit" value="Submit"></div>
              </form>
            </body>
        </html>""")

class EditAG(webapp2.RequestHandler):
   def post(self):
     q = db.Query(agEntry)
     q = agEntry.all()
     q.filter('user_id', cgi.escape(self.request.get('id')))
     result = q.get()
     subject = cgi.escape(self.request.get('req_name'))
     self.response.write(subject)
     self.response.write(cgi.escape(self.request.get('id')))
     
     if (subject == "English_1"):
       i = 0
     if (subject == "English_2"):
       i = 1
     if (subject == "English_3"):
       i = 2
     if (subject == "English_4"):
       i = 3
     if (subject == "Science_(Year_1)"):
       i = 4
     if (subject == "Science_(Year_2)"):
       i = 5
     if (subject == "Science_(Year_3)"):
       i = 6
     if (subject == "Foreign_Language_(Year_1)"):
       i = 7
     if (subject == "Foreign_Language_(Year_2)"):
       i = 8
     if (subject == "Foreign_Language_(Year_3)"):
       i = 9
     if (subject == "Algebra_II"):
       i = 10
     if (subject == "Geometry"):
       i = 11
     if (subject == "Math_(Year_1)"):
       i = 12
     if (subject == "Math_(Year_2)"):
       i = 13
     if (subject == "Math_(Year_3)"):
       i = 14
     if (subject == "US_History"):
       i = 15
     if (subject == "World_History"):
       i = 16
     if (subject == "Visual/Performing_Arts"):
       i = 17
     if (subject == "Elective"):
       i = 18
     if (subject == "Biology"):
       i = 19
     if (subject == "Chemistry"):
       i = 20
     if (subject == "Physics"):
       i = 21
     
     if (result.fulfillment[i] == True):
       result.fulfillment[i] = False
     else:
       result.fulfillment[i] = True
     result.put()

class PersonalSchoolEntry(db.Model):
    names = db.ListProperty(str)
    s_IDs = db.ListProperty(str)
    user_id = db.StringProperty()

class PersonalSchoolEntity(webapp2.RequestHandler):
  def get(self):
      request_id = self.request.get('id')
      if (request_id == ""):
        schoolList = PersonalSchoolEntry.gql("WHERE ANCESTOR IS :1",
                                     schoolList_key("personal_colleges"))
      else:
        schoolList = PersonalSchoolEntry.gql("WHERE ANCESTOR IS :1 AND user_id = \'" + request_id +"\'",
                             schoolList_key("personal_colleges"))
      
      self.response.write("{\"colleges\": [")
      for user in schoolList:
        for i, college in enumerate(user.names):
          if (i == 0):
            self.response.write("{\"Name\": ")
          else:
            self.response.write(", {\"Name\": ")
          self.response.write("\"" + user.names[i] + "\", ")
          self.response.write("\"School id\": ")
          self.response.write("\"" + str(user.s_IDs[i]) + "\"}")
      
      self.response.write("]}")

class AddPersonalSchool(webapp2.RequestHandler):
   def post(self):
     #quick check for existing College - if exists, update
     q = db.Query(PersonalSchoolEntry)
     q = PersonalSchoolEntry.all()
     q.filter('user_id =', cgi.escape(self.request.get('ID')))
     result = q.get()
     schoolList = PersonalSchoolEntry.gql("WHERE ANCESTOR IS :1 AND user_id = \'" + cgi.escape(self.request.get('ID')) + "\'", schoolList_key("personal_colleges"))
     num = 0
     for i in schoolList:
       num += 1
     self.response.write(num)
     if (num == 0):
       result = PersonalSchoolEntry(parent=schoolList_key("personal_colleges"))
       result.user_id = cgi.escape(self.request.get('ID'))

     result.names.append(cgi.escape(self.request.get('schoolName')))
     result.s_IDs.append(cgi.escape(self.request.get('schoolID')))
     result.put()
     self.response.write(result)
     	

class EditPersonalForm(webapp2.RequestHandler):
   def get(self):
       self.response.out.write("""
        <html>
            <body>
              <form action="/addPersonal" method="post">
              <p>User ID: <input type="text" name="ID"> </p>
              <p>School ID: <input type="text" name="schoolID"></p>
              <p>School Name: <input type="text" name="schoolName"></p>
              <div><input type="submit" value="Submit"></div>
              </form>
            </body>
        </html>""")

class CSVUpload(webapp2.RequestHandler):
  def get(self):
    upload_url = blobstore.create_upload_url('/csvupload')
    self.response.out.write('<html><body>')
    self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
    self.response.out.write("""Upload File: <input type="file" name="file"><br> <input type="submit" name="submit" value="Submit"> </form></body></html>""")

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
  def post(self):
    upload_files = self.get_uploads('file') 
    blob_info = upload_files[0]
    global key
    key = blob_info.key()
    blob_reader = blobstore.BlobReader(key, buffer_size=1048576)
    self.redirect('/colleges')

app = webapp2.WSGIApplication([('/csv', CSVUpload),('/csvupload', UploadHandler),('/colleges', SchoolEntity), ('/personal_colleges', PersonalSchoolEntity), ('/addPersonal', AddPersonalSchool), ('/editPersonal', EditPersonalForm), ('/deadlines', DeadlineEntity), ('/getAgReqs', agEntity), ('/sat1', sat1Entity), ('/sat2', sat2Entity),('/add', AddForm), ('/addschool', AddSchool), ('/editAG', EditAG), ('/editAgForm', EditAGForm)],
                              debug=True)
