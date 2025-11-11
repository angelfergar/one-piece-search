# 🏴‍☠️  **One Piece Chapter**

This project is a QA Automation framework built with Python and Selenium to monitor the reléase of One Piece manga chapters across multiple scan webs. It uses the Page Object Model (POM) design pattern combined with OOP principles for maintainability, and sends an automatic email notification whenever a new chapter is released. This framework is integrated in Jenkins, checking the webs periodically based on a schedule.

The goal is to showcase automation skills, web scraping with Selenium, email notifications, and CI/CD pipelines in a QA Automation context.

---

## 📌 **Project Structure**

```
one-piece-search/
│
├─ base/    
│  └─ base.py  
│  └─ selenium_driver.py   
│  └─ web_factory.py   
│
├─ utils/
│  └─ utils.py 
│                
├─ webs/
│  └─ opscans.py 
│  └─ read_onepiece.py  
│  └─ tcb_scans.py 
│
└─ chapter.txt                                  
└─ chapter_search.py                                      
└─ Jenkinsfile                 
└─ requirements.txt  
└─ web_config.py                     
```

---

## ⚙️ **1. Framework Overview**

The project is built using OOP and the Page Object Model (POM) with the following layers:

### **1.1 Base Classes**

* **SeleniumDriver**
  
Its main purpose is to simplify Selenium Webdriver actions such as interacting with web elements, waiting for visibility, and clicking elements.

* **BasePage**
  
It is used by all Page Objects to share core Selenium methods, ensuring their interactions are centralized for maintainability.

* **WebDriverFactory**
  
Initializes the browser (Firefox) and navigates to the desired URL.

* **WebConfig**
  
Sets up the Selenium driver using WebDriverFactory and returns a ready-to-use browser instance.

### **1.2 Page Objects**
Each supported web has its own page class:

* OpScans → Handles OP Scans website interactions
* TcbScans → Handles TCB Scans website interactions
* ReadOnePiece → Handles Read One Piece website interactions

Every page has only a method that checks the availability of the chapter.

### **1.3 Chapter Search**

This script handles the automation workflow:

* Reads the last stored chapter from chapter.txt.

* Iterates through each of the scans webs.

* Opens the browser and checks if the chapter is available.

* Sends email notifications with the links to the websites where the chapter was found.

* Updates chapter.txt with the next chapter number.

---

## 📥 **2. Jenkins Integration**

The Jenkins configuration schedules the project to run every 15 minutes from Thursday to Saturday (The days when the chapters are usually released):

* Sets up a Python virtual environment

* Intalls dependencies

* Runs the chapter search script using email credentials stored in Jenkins

---

## 📈 **3. Project Highlights**

* It shows a Selenium automation framework using Page Object Model (POM) and OOP design.

* Supports multiple webs with a modular and reusable architecture.

* Automatically sends email notifications when a new chapter is available.

* Integrated into Jenkins for scheduled execution and CI/CD showcase.

* Easily extensible to add new manga websites or notification methods.

---

## 🤝 **4. Contribution**

Suggestions, improvements, and new features are welcome! 🚀

**Author:** Ángel Fernández

**Email:** anfernagar@gmail.com
