# General bot settings
first = input("Before we use the feature, \nplease install the requirements.yaml file on your console \n You will also need to add your phone number on you linkedin profile\nif you want to check these please press 0\nto proceed press 1\n") #setting up the packages first

# These settings are for running Linkedin job apply bot
# Paaste your easyApply email and key below

# location you want to search the jobs - ex : ["Poland", "Singapore", "New York City Metropolitan Area", "Monroe County"]
# continent locations:["Europe", "Asia", "Australia", "NorthAmerica", "SouthAmerica", "Africa", "Australia"]
location = ["NorthAmerica"]
# keywords related with your job search
keywords = ["data", "analyst","sql", "cloud", "python", "programming","data science"]
#job experience Level - ex:  ["Internship", "Entry level" , "Associate" , "Mid-Senior level" , "Director" , "Executive"]
experienceLevels = [ "Entry level" ]
#job posted date - ex: ["Any Time", "Past Month" , "Past Week" , "Past 24 hours"] - select only one
datePosted = ["Past Week"]
#job type - ex:  ["Full-time", "Part-time" , "Contract" , "Temporary", "Volunteer", "Intership", "Other"]
jobType = ["Full-time", "Part-time" , "Contract"]
#remote  - ex: ["On-site" , "Remote" , "Hybrid"]
remote = ["On-site" , "Remote" , "Hybrid"]
#salary - ex:["$40,000+", "$60,000+", "$80,000+", "$100,000+", "$120,000+", "$140,000+", "$160,000+", "$180,000+", "$200,000+" ] - select only one
salary = [ "$80,000+"]
#sort - ex:["Recent"] or ["Relevent"] - select only one
sort = ["Recent"]

email = ""
password = ""
chromeProfilePath = ""
easyApplyEmail = ""
easyApplyKey = ""
info = "0"
def get_input(prompt, choices=None):
    while True:
        value = input(prompt)
        if choices and value not in choices:
            print(f"Invalid choice. Choose from {', '.join(choices)}")
        else:
            return value
if first != "0":
    email = get_input("Enter email: ")
    password = get_input("Enter password: ")
    chromeProfilePath = get_input("Enter Chrome Profile Path: ")
    easyApplyEmail = get_input("Enter Easy Apply Email: ")
    easyApplyKey = get_input("Enter Easy Apply Key: ")
    info = get_input("Want to enter more info? (0 for default and 1 for yes): ")
if info != "0":
    # For lists, you can adapt a bit
    location_choices = ["Europe", "Asia", "Australia", "NorthAmerica", "SouthAmerica", "Africa", "Australia"]
    location = get_input("(Choose from: Europe, Asia, Australia, NorthAmerica, SouthAmerica, Africa, Australia)\nEnter location: ", location_choices).split(',')

    keywords = get_input("Enter keywords (comma separated): ").split(',')
    experience_levels_choices = ["Internship", "Entry level", "Associate", "Mid-Senior level", "Director", "Executive"]
    experienceLevels = get_input("(Choose from: Internship, Entry level, Associate, Mid-Senior level, Director, Executive)\nEnter experience level: ", experience_levels_choices).split(',')

    date_posted_choices = ["Any Time", "Past Month", "Past Week", "Past 24 hours"]
    datePosted = [get_input("(Choose from:Any Time, Past Month, Past Week, Past 24 hours)\nEnter date posted: ", date_posted_choices)]

    job_type_choices = ["Full-time", "Part-time", "Contract", "Temporary", "Volunteer", "Intership", "Other"]
    jobType = get_input("(Choose from: Full-time, Part-time, Contract, Temporary, Volunteer, Intership, Other)\nEnter job type: ", job_type_choices).split(',')

    remote_choices = ["On-site", "Remote", "Hybrid"]
    remote = get_input("Enter remote option:(On-site, Remote, Hybrid) ", remote_choices).split(',')

    salary_choices = ["$40,000+", "$60,000+", "$80,000+", "$100,000+", "$120,000+", "$140,000+", "$160,000+", "$180,000+", "$200,000+"]
    salary = [get_input("(Choose from:$40,000+, $60,000+, $80,000+, $100,000+, $120,000+, $140,000+, $160,000+, $180,000+, $200,000+)\nEnter salary: ", salary_choices)]

    sort_choices = ["Recent", "Relevant"]
    sort = [get_input("Enter sort option: (Recent, Relevant)", sort_choices)]


    print("Configuration saved!")


browser = ["Chrome"]
headless = False

#Blacklist companies you dont want to apply - ex: ["Apple","Google"]
blacklistCompanies = []
#Blaclist keywords in title - ex:["manager", ".Net"]
blackListTitles = []
#Follow companies after sucessfull application True - yes, False - no
followCompanies = False
#Below settings are for linkedin bot Pro, you can purchase monthly or yearly subscription to use them from me.
#PRO FEATURE! - If you have multiple CV's you can choose which one you want the bot to use. (1- the first one on the list, 2 - second , etc)
preferredCv = 1
#PRO FEAUTRE! - Output unaswered questions into a seperate text file, will output radio box, dropdown and input field questions into seperate .yaml file
outputSkippedQuestions = True
#PRO FEATURE! - Use AI to fill and answer skipped questions. Will cost 5 credits per answer cause of computational power.
useAiAutocomplete = False
#PRO FEATURE! - Only Apply these companies -  ex: ["Apple","Google"] -  leave empty for all companies 
onlyApplyCompanies = []
#PRO FEATURE! - Only Apply titles having these keywords -  ex:["web", "remote"] - leave empty for all companies 
onlyApplyTitles = [] 
#PRO FEATURE! - Dont apply the job posted by the Hiring member contains this in his/her name - ex: ["adam","Sarah"]
blockHiringMember = [] 
#PRO FEATURE! - Only apply the job sposted by the Hiring member contains this in his/her name - ex: ["adam","Sarah"]
onlyApplyHiringMember = [] 
#PRO FEATURE! - Only apply jobs having less than applications - ex:["100"] will apply jobs having upto 100 applications 
onlyApplyMaxApplications = []
#PRO FEATURE! - Only apply jobs having more than applications - ex:["10"] will apply jobs having more than 10 applications 
onlyApplyMinApplications = []
#PRO FEATURE! - Only apply jobs having these keywords in the job description
onlyApplyJobDescription = []
#PRO FEATURE! - Do not apply the jobs having these keywords in the job description
blockJobDescription = []
#PRO FEATURE! - Apply companies having equal or more than employes - ex: ["100"]
onlyAppyMimEmployee = []
#PRO FEATURE - Apply the ones linkedin is saying "you may be a goodfit"
onlyApplyLinkedinRecommending = False
#PRO FEATURE - Only apply the ones you have skilled badge
onlyApplySkilledBages = False
#PRO FEATURE! - Save the jobs by pressing SAVE button before apply  True - yes, False - no
saveBeforeApply = False
#PRO FEATURE! - Sent a message to the hiring manager once you apply for the role
messageToHiringManager = ""
#PRO FEATURE! - List and output non Easy Apply jobs links
listNonEasyApplyJobsUrl = False
#PRO FEATURE! - Select radio button for unsawered questions. If the bot cannot find an answer for a radio button, it will automatically select first or second option. Default radio button answer, 1 for Yes, 2 for No. Leave empty if you dont want this option.
selectRadioOptionForUnasweredQuestions = 1
#PRO FEATURE! - Check yes or no to all checkbox questions (True - yes, False - no), leave empty if you dont want this option
answerAllCheckboxes = ""
#PRO FEAUTRE! - Output file type. Can be .txt or .csv (excel) 
outputFileType = [".txt"]

# These settings are for running AngelCO job apply bot you need to purchase AngelCo bot obtain bot password, paste below and then run the bot.
AngelCoBotPassword = ""
# AngelCO credits
AngelCoEmail = ""
AngelCoPassword = ""
# jobTitle ex: ["Frontend Engineer", "Marketing"]
angelCoJobTitle = ["Frontend Engineer"]
# location ex: ["Poland"]
angelCoLocation = ["Poland"]

# These settings are for running GlobalLogic job apply bot you need to purchase GlobalLogic bot obtain bot password, paste below and then run the bot.
GlobalLogicBotPassword = ""
# AngelCO credits
GlobalLogicEmail = ""
GlobalLogicPassword = ""
# Functions ex: ["Administration", "Business Development", "Business Solutions", "Content Engineering", 	
# Delivery Enablement", Engineering, Finance, IT Infrastructure, Legal, Marketing, People Development,
# Process Management, Product Support, Quality Assurance,Sales, Sales Enablement,Technology, Usability and Design]
GlobalLogicFunctions = ["Engineering"]
# Global logic experience: ["0-1 years", "1-3 years", "3-5 years", "5-10 years", "10-15 years","15+ years"]
GlobalLogicExperience = ["0-1 years", "1-3 years"]
# Global logic location filter: ["Argentina", "Chile", "Crotia", "Germany", "India","Japan", "Poland"
# Romania, Sweden, Switzerland,Ukraine, United States]
GlobalLogicLocation = ["poland"]
# Freelance yes or no
GlobalLogicFreelance = ["no"]
# Remote work yes or no
GlobalLogicRemoteWork = ["yes"]
# Optional! Keyword:["javascript", "react", "angular", ""]
GlobalLogicKeyword = ["react"]
# Global Logic Job apply settinngs
FirstName = "O"
LastName = "D"
Email = "chrisbwang66@gmail.com"
LinkedInProfileURL = "www.google.com"
Phone = "80086988888" #OPTIONAL
Location = "PA" #OPTIONAL
HowDidYouHeard = "Li" #OPTIONAL
ConsiderMeForFutureOffers = True #true = yes, false = no

 # Testing & Debugging features
displayWarnings = False
