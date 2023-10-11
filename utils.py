import math,constants,time,config
from typing import List

from selenium import webdriver

def chromeBrowserOptions():
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-extensions")
    options.add_argument('--disable-gpu')
    if(config.headless):
        options.add_argument("--headless")
    # options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # if(len(config.chromeProfilePath)>0):
    #     initialPath = config.chromeProfilePath[0:config.chromeProfilePath.rfind("/")]
    #     profileDir = config.chromeProfilePath[config.chromeProfilePath.rfind("/")+1:]
    #     options.add_argument('--user-data-dir=' +initialPath)
    #     options.add_argument("--profile-directory=" +profileDir)
    # else:
    options.add_argument("--incognito")
    return options

def prRed(prt):
    print(f"\033[91m{prt}\033[00m")

def prGreen(prt):
    print(f"\033[92m{prt}\033[00m")

def prYellow(prt):
    print(f"\033[93m{prt}\033[00m")

def getUrlDataFile():
    urlData = ""
    try:
        file = open('data/urlData.txt', 'r')
        urlData = file.readlines()
    except FileNotFoundError:
        text = "FileNotFound:urlData.txt file is not found. Please run ./data folder exists and check config.py values of yours. Then run the bot again"
        prRed(text)
    return urlData

def jobsToPages(numOfJobs: str) -> int:
  number_of_pages = 1

  if (' ' in numOfJobs):
    spaceIndex = numOfJobs.index(' ')
    totalJobs = (numOfJobs[0:spaceIndex])
    totalJobs_int = int(totalJobs.replace(',', ''))
    number_of_pages = math.ceil(totalJobs_int/constants.jobsPerPage)
    if (number_of_pages > 40 ): number_of_pages = 40

  else:
      number_of_pages = int(numOfJobs)

  return number_of_pages

def urlToKeywords(url: str) -> List[str]:
    keywordUrl = url[url.index("keywords=")+9:]
    keyword = keywordUrl[0:keywordUrl.index("&") ] 
    locationUrl =  url[url.index("location=")+9:]
    location = locationUrl[0:locationUrl.index("&") ] 
    return [keyword,location]

def writeResults(text: str):
    timeStr = time.strftime("%Y%m%d")
    fileName = "Applied Jobs DATA - " +timeStr + ".txt"
    try:
        with open("data/" +fileName, encoding="utf-8" ) as file:
            lines = []
            for line in file:
                if "----" not in line:
                    lines.append(line)
                
        with open("data/" +fileName, 'w' ,encoding="utf-8") as f:
            f.write("---- Applied Jobs Data ---- created at: " +timeStr+ "\n" )
            f.write("---- Number | Job Title | Company | Location | Work Place | Posted Date | Applications | Result "   +"\n" )
            for line in lines: 
                f.write(line)
            f.write(text+ "\n")
            
    except:
        with open("data/" +fileName, 'w', encoding="utf-8") as f:
            f.write("---- Applied Jobs Data ---- created at: " +timeStr+ "\n" )
            f.write("---- Number | Job Title | Company | Location | Work Place | Posted Date | Applications | Result "   +"\n" )

            f.write(text+ "\n")

def printInfoMes(bot:str):
    prYellow("ℹ️ " +bot+ " is starting soon... ")

def donate(self):
    prYellow('If you like the project, please support me so that i can make more such projects, thanks!')
    try:
        self.driver.get('https://commerce.coinbase.com/checkout/923b8005-792f-4874-9a14-2992d0b30685')
    except Exception as e:
        prRed("Error in donate: " +str(e))

class LinkedinUrlGenerate:
    import config
    
    def generateUrlLinks(self):
        path = []
        for location in config.location:
            for keyword in config.keywords:
                    url = constants.linkJobUrl + "?f_AL=true&keywords=" +keyword+self.jobType()+self.remote()+self.checkJobLocation(location)+self.jobExp()+self.datePosted()+self.salary()+self.sortBy()
                    path.append(url)
        return path

    def checkJobLocation(self,job):
        jobLoc = "&location=" +job.lower()
        if job.lower() == "asia":
                jobLoc += "&geoId=102393603"
        elif job.lower() == "europe":
                jobLoc += "&geoId=100506914"
        elif job.lower() == "northamerica":
                jobLoc += "&geoId=102221843&"
        elif job.lower() == "southamerica":
                jobLoc +=  "&geoId=104514572"
        elif job.lower() == "australia":
                jobLoc +=  "&geoId=101452733"
        elif job.lower() == "africa":
                jobLoc += "&geoId=103537801"

        return jobLoc

    def jobExp(self):
        jobtExpArray = config.experienceLevels
        firstJobExp = jobtExpArray[0]
        jobExp = ""

        if firstJobExp == "Internship":
            jobExp = "&f_E=1"
        elif firstJobExp == "Entry level":
            jobExp = "&f_E=2"
        elif firstJobExp == "Associate":
            jobExp = "&f_E=3"
        elif firstJobExp == "Mid-Senior level":
            jobExp = "&f_E=4"
        elif firstJobExp == "Director":
            jobExp = "&f_E=5"
        elif firstJobExp == "Executive":
            jobExp = "&f_E=6"

        for index in range(1, len(jobtExpArray)):
            if jobtExpArray[index] == "Internship":
                jobExp += "%2C1"
            elif jobtExpArray[index] == "Entry level":
                jobExp += "%2C2"
            elif jobtExpArray[index] == "Associate":
                jobExp += "%2C3"
            elif jobtExpArray[index] == "Mid-Senior level":
                jobExp += "%2C4"
            elif jobtExpArray[index] == "Director":
                jobExp += "%2C5"
            elif jobtExpArray[index] == "Executive":
                jobExp += "%2C6"

        return jobExp
    
    def datePosted(self):
        datePosted = ""

        if config.datePosted[0] == "Any Time":
            datePosted = ""
        elif config.datePosted[0] == "Past Month":
            datePosted = "&f_TPR=r2592000&"
        elif config.datePosted[0] == "Past Week":
            datePosted = "&f_TPR=r604800&"
        elif config.datePosted[0] == "Past 24 hours":
            datePosted = "&f_TPR=r86400&"

        return datePosted

    def jobType(self):
        jobTypeArray = config.jobType
        firstjobType = jobTypeArray[0]
        jobType = ""

        if firstjobType == "Full-time":
            jobType = "&f_JT=F"
        elif firstjobType == "Part-time":
            jobType = "&f_JT=P"
        elif firstjobType == "Contract":
            jobType = "&f_JT=C"
        elif firstjobType == "Temporary":
            jobType = "&f_JT=T"
        elif firstjobType == "Volunteer":
            jobType = "&f_JT=V"
        elif firstjobType == "Intership":
            jobType = "&f_JT=I"
        elif firstjobType == "Other":
            jobType = "&f_JT=O"

        for index in range(1, len(jobTypeArray)):
            if jobTypeArray[index] == "Full-time":
                jobType += "%2CF"
            elif jobTypeArray[index] == "Part-time":
                jobType += "%2CP"
            elif jobTypeArray[index] == "Contract":
                jobType += "%2CC"
            elif jobTypeArray[index] == "Temporary":
                jobType += "%2CT"
            elif jobTypeArray[index] == "Volunteer":
                jobType += "%2CV"
            elif jobTypeArray[index] == "Intership":
                jobType += "%2CI"
            elif jobTypeArray[index] == "Other":
                jobType += "%2CO"

        jobType += "&"

        return jobType

    def remote(self):
        remoteArray = config.remote
        firstJobRemote = remoteArray[0]
        jobRemote = ""

        if firstJobRemote == "On-site":
            jobRemote = "f_WT=1"
        elif firstJobRemote == "Remote":
            jobRemote = "f_WT=2"
        elif firstJobRemote == "Hybrid":
            jobRemote = "f_WT=3"

        for index in range(1, len(remoteArray)):
            if remoteArray[index] == "On-site":
                jobRemote += "%2C1"
            elif remoteArray[index] == "Remote":
                jobRemote += "%2C2"
            elif remoteArray[index] == "Hybrid":
                jobRemote += "%2C3"

        return jobRemote

    def salary(self):
        salary = ""
        firstSalary = config.salary[0]
        if firstSalary == "$40,000+":
            salary = "f_SB2=1&"
        elif firstSalary == "$60,000+":
            salary = "f_SB2=2&"
        elif firstSalary == "$80,000+":
            salary = "f_SB2=3&"
        elif firstSalary == "$100,000+":
            salary = "f_SB2=4&"
        elif firstSalary == "$120,000+":
            salary = "f_SB2=5&"
        elif firstSalary == "$140,000+":
            salary = "f_SB2=6&"
        elif firstSalary == "$160,000+":
            salary = "f_SB2=7&"
        elif firstSalary == "$180,000+":
            salary = "f_SB2=8&"
        elif firstSalary == "$200,000+":
            salary = "f_SB2=9&"
        
        return salary

    def sortBy(self):
        sortBy = ""
        firstSort = config.sort[0]
        if firstSort == "Recent":
            sortBy = "sortBy=DD"
        elif firstSort == "Relevent":
            sortBy = "sortBy=R"
        
        return sortBy

