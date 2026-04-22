import gradio as gr
import pandas as pd
import json
import io
import re
from google import genai
import plotly.graph_objects as go
import random
from datetime import datetime
import base64
import time
import plotly.express as px
from typing import List, Dict, Tuple
import numpy as np
import speech_recognition as sr
import tempfile
import wave
from pydub import AudioSegment
import os

# Hardcoded data for all platforms and resources
class CareerData:
    def __init__(self):
        # Coding Platforms
        self.coding_platforms = [
            {
                "name": "LeetCode",
                "logo": "💻",
                "url": "https://leetcode.com",
                "description": "Practice coding problems, prepare for interviews",
                "features": ["Coding Challenges", "Interview Prep", "Contests"],
                "best_for": ["FAANG Interviews", "Algorithm Practice"],
                "pricing": "Free (Premium available)",
                "rating": "4.8/5",
                "difficulty": ["Easy", "Medium", "Hard"]
            },
            {
                "name": "HackerRank",
                "logo": "⚡",
                "url": "https://hackerrank.com",
                "description": "Develop coding skills and prepare for technical interviews",
                "features": ["Coding Tests", "Skill Certification", "Contests"],
                "best_for": ["Campus Recruitment", "Skill Assessment"],
                "pricing": "Free",
                "rating": "4.5/5",
                "difficulty": ["Beginner", "Intermediate"]
            },
            {
                "name": "CodeChef",
                "logo": "🔥",
                "url": "https://codechef.com",
                "description": "Competitive programming platform with monthly contests",
                "features": ["Competitions", "Practice Problems", "Learning Resources"],
                "best_for": ["Competitive Programming", "Indian Companies"],
                "pricing": "Free",
                "rating": "4.3/5",
                "difficulty": ["Easy", "Medium", "Hard"]
            },
            {
                "name": "freeCodeCamp",
                "logo": "🆓",
                "url": "https://freecodecamp.org",
                "description": "Learn to code with free online courses and projects",
                "features": ["Certifications", "Projects", "Community"],
                "best_for": ["Web Development", "Beginners"],
                "pricing": "Free",
                "rating": "4.9/5",
                "difficulty": ["Beginner", "Intermediate"]
            },
            {
                "name": "GeeksforGeeks",
                "logo": "📚",
                "url": "https://geeksforgeeks.org",
                "description": "Computer science portal for geeks with coding practice",
                "features": ["Articles", "Practice", "Interview Preparation"],
                "best_for": ["DSA Learning", "Company-specific Questions"],
                "pricing": "Free (Paid courses available)",
                "rating": "4.6/5",
                "difficulty": ["Easy", "Medium", "Hard"]
            },
            {
                "name": "Codecademy",
                "logo": "🎓",
                "url": "https://codecademy.com",
                "description": "Interactive coding lessons and projects",
                "features": ["Interactive Learning", "Projects", "Career Paths"],
                "best_for": ["Beginners", "Structured Learning"],
                "pricing": "Freemium",
                "rating": "4.4/5",
                "difficulty": ["Beginner", "Intermediate"]
            },
            {
                "name": "Exercism",
                "logo": "🏃",
                "url": "https://exercism.org",
                "description": "Code practice and mentorship platform",
                "features": ["Mentorship", "Multiple Languages", "Practice Exercises"],
                "best_for": ["Language Mastery", "Code Reviews"],
                "pricing": "Free",
                "rating": "4.7/5",
                "difficulty": ["Beginner", "Intermediate", "Advanced"]
            },
            {
                "name": "TopCoder",
                "logo": "🏆",
                "url": "https://topcoder.com",
                "description": "Competitive programming and freelance platform",
                "features": ["Challenges", "Competitions", "Freelance Work"],
                "best_for": ["Advanced Programmers", "Freelancing"],
                "pricing": "Free",
                "rating": "4.2/5",
                "difficulty": ["Hard", "Expert"]
            }
        ]
        
        # Hackathon Platforms
        self.hackathon_platforms = [
            {
                "name": "Unstop",
                "logo": "🚀",
                "url": "https://unstop.com",
                "description": "Comprehensive platform for tech, innovation, and case-based hackathons in India and globally",
                "features": ["Student Competitions", "Company Sponsorships", "Prize Money", "Internship Opportunities"],
                "best_for": ["Students", "Beginners", "Indian Hackathons"],
                "prizes": "Cash prizes, internships, job offers",
                "rating": "4.7/5",
                "popularity": "Very High in India",
                "difficulty": ["Beginner", "Intermediate"]
            },
            {
                "name": "Devpost",
                "logo": "🌐",
                "url": "https://devpost.com",
                "description": "Leading global hackathon directory hosting major company-sponsored and open online hackathons",
                "features": ["Global Events", "Company Sponsors", "Online Hackathons", "Web3/AI Focus"],
                "best_for": ["Global Participants", "Tech Professionals", "Remote Hackathons"],
                "prizes": "$500-$50,000+ prizes, tech gadgets, mentorship",
                "rating": "4.8/5",
                "popularity": "Global Leader",
                "difficulty": ["Intermediate", "Advanced"]
            },
            {
                "name": "HackerEarth",
                "logo": "⚡",
                "url": "https://hackerearth.com",
                "description": "Large developer community platform organizing coding hackathons and recruitment challenges",
                "features": ["Coding Challenges", "Recruitment Hackathons", "Skill Assessment", "Company Challenges"],
                "best_for": ["Developers", "Job Seekers", "Skill Showcase"],
                "prizes": "Cash rewards, job interviews, tech products",
                "rating": "4.6/5",
                "popularity": "High in Tech Industry",
                "difficulty": ["Intermediate", "Advanced"]
            },
            {
                "name": "Devfolio",
                "logo": "📱",
                "url": "https://devfolio.co",
                "description": "Popular platform in India for college and Web3 hackathons with beginner-friendly events",
                "features": ["Web3 Hackathons", "College Events", "Beginner Friendly", "Community Building"],
                "best_for": ["College Students", "Web3 Enthusiasts", "Blockchain Developers"],
                "prizes": "Crypto prizes, grants, incubation opportunities",
                "rating": "4.5/5",
                "popularity": "High in India for Web3",
                "difficulty": ["Beginner", "Intermediate"]
            },
            {
                "name": "MLH (Major League Hacking)",
                "logo": "🏆",
                "url": "https://mlh.io",
                "description": "Global student hackathon league running hundreds of events worldwide with strong community",
                "features": ["Student Hackathons", "Global Community", "Learning Workshops", "Career Opportunities"],
                "best_for": ["Students Worldwide", "Learning & Networking", "Campus Events"],
                "prizes": "Swag, scholarships, internship opportunities",
                "rating": "4.9/5",
                "popularity": "Global Student Favorite",
                "difficulty": ["Beginner", "Intermediate"]
            }
        ]
        
        # Career Roles Database with YouTube Learning Links
        self.career_roles = {
            "Data Analyst": {
                "logo": "📊",
                "description": "Analyze data to help businesses make decisions",
                "skills": ["SQL", "Excel", "Python", "Tableau", "Statistics"],
                "experience": "0-2 years",
                "salary": "$60k-85k",
                "youtube_links": [
                    "https://youtu.be/Dnch98Zf2ks",
                    "https://youtu.be/PSNXoAs2FtQ",
                    "https://youtu.be/VaSjiJMrq24"
                ]
            },
            "Data Scientist": {
                "logo": "🧮",
                "description": "Build predictive models and algorithms",
                "skills": ["Python", "Machine Learning", "Statistics", "SQL", "Pandas"],
                "experience": "2-5 years",
                "salary": "$95k-130k",
                "youtube_links": [
                    "https://youtu.be/7WRlYJFG7YI",
                    "https://youtu.be/OivTPt5LQh0",
                    "https://youtu.be/gDZ6czwuQ18"
                ]
            },
            "Web Developer": {
                "logo": "🌐",
                "description": "Build and maintain websites and web applications",
                "skills": ["HTML/CSS", "JavaScript", "React", "Node.js", "MongoDB"],
                "experience": "0-2 years",
                "salary": "$60k-85k",
                "youtube_links": [
                    "https://youtu.be/HVjjoMvutj4",
                    "https://youtu.be/nu_pCVPKzTk"
                ]
            },
            "Frontend Developer": {
                "logo": "🎨",
                "description": "Build user interfaces and client-side applications",
                "skills": ["HTML/CSS", "JavaScript", "React", "Vue.js", "TypeScript"],
                "experience": "1-3 years",
                "salary": "$70k-100k",
                "youtube_links": [
                    "https://www.youtube.com/live/PGrLUvpVde0",
                    "https://youtu.be/zJSY8tbf_ys"
                ]
            },
            "Backend Developer": {
                "logo": "⚙️",
                "description": "Build server-side logic and databases",
                "skills": ["Node.js", "Python", "Java", "SQL", "APIs"],
                "experience": "1-3 years",
                "salary": "$75k-110k",
                "youtube_links": [
                    "https://youtu.be/7fjOw8ApZ1I",
                    "https://youtu.be/ftKiHCDVwfA"
                ]
            },
            "Full Stack Developer": {
                "logo": "🚀",
                "description": "Handle both frontend and backend development",
                "skills": ["React", "Node.js", "MongoDB", "APIs", "Deployment"],
                "experience": "2-4 years",
                "salary": "$85k-120k",
                "youtube_links": [
                    "https://youtu.be/gxHXPmePnvo",
                    "https://www.youtube.com/live/09Je_ZqxuUs"
                ]
            },
            "Android Developer": {
                "logo": "🤖",
                "description": "Develop mobile applications for Android",
                "skills": ["Kotlin", "Java", "Android SDK", "Firebase", "XML"],
                "experience": "1-3 years",
                "salary": "$70k-100k",
                "youtube_links": [
                    "https://youtu.be/BCSlZIUj18Y",
                    "https://youtu.be/tZvjSl9dswg"
                ]
            },
            "iOS Developer": {
                "logo": "📱",
                "description": "Develop mobile applications for iOS",
                "skills": ["Swift", "UIKit", "Xcode", "Core Data", "APIs"],
                "experience": "1-3 years",
                "salary": "$75k-110k",
                "youtube_links": [
                    "https://youtu.be/uEhmQd0Z1CA",
                    "https://youtu.be/blKkRoZPxLc"
                ]
            },
            "Game Developer": {
                "logo": "🎮",
                "description": "Create video games for various platforms",
                "skills": ["C#", "Unity", "C++", "Game Physics", "3D Graphics"],
                "experience": "1-3 years",
                "salary": "$65k-95k",
                "youtube_links": [
                    "https://youtu.be/ZEtKg9AyEJc",
                    "https://youtu.be/6UlU_FsicK8"
                ]
            },
            "DevOps Engineer": {
                "logo": "🔧",
                "description": "Automate development and deployment processes",
                "skills": ["Docker", "Kubernetes", "AWS", "CI/CD", "Linux"],
                "experience": "2-5 years",
                "salary": "$90k-130k",
                "youtube_links": [
                    "https://youtu.be/hQcFE0RD0cQ",
                    "https://youtu.be/JHoy3lDZOfY",
                    "https://youtu.be/saWZQr0RMpw"
                ]
            },
            "Cloud Engineer": {
                "logo": "☁️",
                "description": "Design and manage cloud infrastructure",
                "skills": ["AWS/Azure/GCP", "Docker", "Terraform", "Linux", "Networking"],
                "experience": "1-3 years",
                "salary": "$85k-120k",
                "youtube_links": [
                    "https://youtu.be/eZeNIakuqbc",
                    "https://youtu.be/j_StCjwpfmk"
                ]
            },
            "Embedded Systems Developer": {
                "logo": "⚡",
                "description": "Develop software for embedded systems",
                "skills": ["C/C++", "RTOS", "Microcontrollers", "Python", "Hardware"],
                "experience": "1-3 years",
                "salary": "$70k-100k",
                "youtube_links": [
                    "https://youtu.be/c7pi9-VQmLk",
                    "https://youtu.be/7WRlYJFG7YI"
                ]
            },
            "ML Engineer": {
                "logo": "🤖",
                "description": "Build and deploy machine learning systems",
                "skills": ["Python", "TensorFlow", "PyTorch", "MLOps", "Docker"],
                "experience": "2-5 years",
                "salary": "$110k-150k",
                "youtube_links": [
                    "https://youtu.be/hA3spbCBBF0",
                    "https://www.youtube.com/live/FP9kL-_k5Ys",
                    "https://youtu.be/NWONeJKn6kc"
                ]
            },
            "AI Engineer": {
                "logo": "🧠",
                "description": "Develop artificial intelligence solutions",
                "skills": ["Python", "Deep Learning", "NLP", "Computer Vision", "PyTorch"],
                "experience": "2-5 years",
                "salary": "$100k-140k",
                "youtube_links": [
                    "https://youtu.be/mEsleV16qdo",
                    "https://youtu.be/F0GQ0l2NfHA",
                    "https://youtu.be/9tbaiFIm0HU"
                ]
            },
            "Power BI Developer": {
                "logo": "📈",
                "description": "Create business intelligence dashboards and reports",
                "skills": ["Power BI", "DAX", "SQL", "Data Visualization", "Excel"],
                "experience": "1-3 years",
                "salary": "$65k-90k",
                "youtube_links": [
                    "https://youtu.be/5NWbU7zXw5Q",
                    "https://www.youtube.com/live/Pr9q6HTt4L0"
                ]
            },
            "Cybersecurity Analyst": {
                "logo": "🔒",
                "description": "Protect systems and networks from cyber threats",
                "skills": ["Network Security", "Ethical Hacking", "SIEM", "Linux", "Cryptography"],
                "experience": "1-3 years",
                "salary": "$75k-110k",
                "youtube_links": [
                    "https://youtu.be/FwjaHCVNBWA",
                    "https://youtu.be/s19BxFpoSd0",
                    "https://youtu.be/0tahsDhiQwI",
                    "https://www.youtube.com/live/qYfqJJAqMkQ"
                ]
            },
            "Software Engineer": {
                "logo": "💻",
                "description": "Design, develop, and maintain software applications",
                "skills": ["Programming", "Data Structures", "Algorithms", "System Design"],
                "experience": "0-2 years",
                "salary": "$80k - $180k",
                "youtube_links": [
                    "https://youtu.be/rfscVS0vtbw",
                    "https://youtu.be/8hly31xKli0"
                ]
            },
            "Product Manager": {
                "logo": "📱",
                "description": "Define product vision and work with teams to build successful products",
                "skills": ["Product Strategy", "Market Research", "Agile", "Communication", "Analytics"],
                "experience": "2-5 years",
                "salary": "$100k - $250k",
                "youtube_links": [
                    "https://youtu.be/K9H3M4pY2us",
                    "https://youtu.be/6I4gYfJk9qQ"
                ]
            },
            "UX Designer": {
                "logo": "🎨",
                "description": "Design user experiences and interfaces for digital products",
                "skills": ["Figma", "User Research", "Wireframing", "Prototyping", "UI Design"],
                "experience": "1-3 years",
                "salary": "$65k - $140k",
                "youtube_links": [
                    "https://youtu.be/c9Wg6Cb_YlU",
                    "https://youtu.be/_W1tKKeDs6Q"
                ]
            }
        }
        
        # Industry Skills Database
        self.industry_skills = {
            "Software Development": {
                "core": ["Data Structures", "Algorithms", "System Design", "OOP", "Testing"],
                "frontend": ["HTML/CSS", "JavaScript", "React", "Vue.js", "TypeScript"],
                "backend": ["Node.js", "Python", "Java", "Spring Boot", ".NET", "SQL", "NoSQL"],
                "tools": ["Git", "Docker", "Kubernetes", "AWS", "CI/CD"]
            },
            "Data Science": {
                "programming": ["Python", "R", "SQL"],
                "ml": ["Scikit-learn", "TensorFlow", "PyTorch", "XGBoost"],
                "stats": ["Statistics", "Probability", "Hypothesis Testing"],
                "visualization": ["Matplotlib", "Seaborn", "Plotly", "Tableau", "Power BI"],
                "big_data": ["Hadoop", "Spark", "Hive", "Airflow"]
            },
            "DevOps & Cloud": {
                "cloud": ["AWS", "Azure", "GCP", "Cloud Architecture"],
                "containers": ["Docker", "Kubernetes", "Container Orchestration"],
                "iac": ["Terraform", "CloudFormation", "Ansible"],
                "cicd": ["Jenkins", "GitLab CI", "GitHub Actions", "ArgoCD"],
                "monitoring": ["Prometheus", "Grafana", "ELK Stack", "Datadog"]
            },
            "Cybersecurity": {
                "fundamentals": ["Network Security", "Cryptography", "Security Protocols"],
                "tools": ["Wireshark", "Nmap", "Metasploit", "Burp Suite"],
                "defense": ["SIEM", "Firewalls", "IDS/IPS", "Endpoint Security"],
                "offensive": ["Ethical Hacking", "Penetration Testing", "Vulnerability Assessment"]
            },
            "Product & Business": {
                "product": ["Product Strategy", "Roadmapping", "User Research", "Metrics"],
                "business": ["Market Analysis", "Business Models", "Financial Analysis"],
                "communication": ["Stakeholder Management", "Presentation", "Documentation"],
                "tools": ["Jira", "Confluence", "Figma", "Analytics Tools"]
            }
        }
        
        # Free Certification Platforms
        self.certification_platforms = {
            "Infosys Springboard": {
                "description": "Provides free industry-backed courses (especially in digital marketing & tech) with free certificates after assessments",
                "best_for": ["Students & beginners to build credentials without paying"],
                "url": "https://springboard.infosys.com",
                "free_certificates": "Yes",
                "topics": ["Digital Marketing", "Tech", "AI", "Data Science"]
            },
            "Coursera": {
                "description": "Huge collection of courses from universities & companies like Google, IBM, Meta, etc.",
                "best_for": ["Mostly free to audit — you can watch course content for free. Certificates require payment but financial aid available"],
                "url": "https://coursera.org",
                "free_certificates": "With Financial Aid",
                "topics": ["All Tech Fields", "Business", "Data Science", "AI"]
            },
            "Class Central": {
                "description": "A search engine/aggregator that lists thousands of free courses + free certificates from many providers",
                "best_for": ["Browse specific categories like data science, IT, marketing, and more"],
                "url": "https://classcentral.com",
                "free_certificates": "Yes",
                "topics": ["All Categories"]
            },
            "IBM SkillsBuild": {
                "description": "100% free learning paths in tech topics like Data Science, AI, Cybersecurity, Cloud, and more",
                "best_for": ["Earn IBM-branded digital badges / certificates upon completion"],
                "url": "https://skillsbuild.org",
                "free_certificates": "Yes",
                "topics": ["Data Science", "AI", "Cybersecurity", "Cloud"]
            },
            "freeCodeCamp": {
                "description": "Entirely free online curriculum in web dev, JavaScript, Python, data analysis, APIs, and more",
                "best_for": ["Full modules award free certificates when completed"],
                "url": "https://freecodecamp.org",
                "free_certificates": "Yes",
                "topics": ["Web Development", "JavaScript", "Python", "Data Analysis"]
            },
            "Kaggle Learn": {
                "description": "Short, hands-on courses from the Kaggle platform on Python, Pandas, SQL, Machine Learning, and more",
                "best_for": ["After finishing lessons and exercises, you can download certificates (completely free)"],
                "url": "https://kaggle.com/learn",
                "free_certificates": "Yes",
                "topics": ["Python", "SQL", "Machine Learning", "Data Visualization"]
            },
            "Google Skillshop": {
                "description": "Free learning about Google products: Analytics, Ads, Measurement, etc.",
                "best_for": ["Free certificates are available after passing assessments"],
                "url": "https://skillshop.withgoogle.com",
                "free_certificates": "Yes",
                "topics": ["Google Analytics", "Google Ads", "Digital Marketing"]
            }
        }
        
        # Job Platforms
        self.job_platforms = [
            {
                "name": "LinkedIn Jobs",
                "logo": "💼",
                "rating": "⭐ 5.0/5",
                "description": "Best for professional, IT, data, and corporate roles",
                "features": ["Recruiter visibility", "Referrals & networking", "Company insights"],
                "url": "https://linkedin.com/jobs",
                "best_for": ["IT Professionals", "Corporate Jobs", "Networking"]
            },
            {
                "name": "Naukri.com",
                "logo": "🇮🇳",
                "rating": "⭐ 4.8/5",
                "description": "India's largest job portal for freshers + experienced professionals",
                "features": ["Freshers + experienced", "IT & corporate jobs", "Resume building"],
                "url": "https://naukri.com",
                "best_for": ["Indian Job Market", "Freshers", "IT Jobs"]
            },
            {
                "name": "Indeed",
                "logo": "🌐",
                "rating": "⭐ 4.7/5",
                "description": "Global job portal with easy & quick apply feature",
                "features": ["Easy & quick apply", "Direct company postings", "Salary insights"],
                "url": "https://indeed.com",
                "best_for": ["Global Jobs", "Quick Applications", "Direct Hiring"]
            },
            {
                "name": "Glassdoor",
                "logo": "🏢",
                "rating": "⭐ 4.6/5",
                "description": "Jobs + company reviews and salary insights",
                "features": ["Company reviews", "Salary insights", "Interview experiences"],
                "url": "https://glassdoor.com",
                "best_for": ["Company Research", "Salary Negotiation", "Interview Prep"]
            },
            {
                "name": "Foundit (Monster)",
                "logo": "🔍",
                "rating": "⭐ 4.5/5",
                "description": "Corporate & MNC jobs with skill-based matching",
                "features": ["Resume insights", "Skill-based matching", "MNC jobs"],
                "url": "https://foundit.in",
                "best_for": ["Corporate Jobs", "MNCs", "Skill Matching"]
            },
            {
                "name": "Freshersworld",
                "logo": "🎓",
                "rating": "⭐ 4.7/5",
                "description": "Best for students & freshers with entry-level & internships",
                "features": ["Entry-level & internships", "Govt & private jobs", "Fresher friendly"],
                "url": "https://freshersworld.com",
                "best_for": ["Students", "Freshers", "Internships"]
            },
            {
                "name": "Wellfound (AngelList Talent)",
                "logo": "🚀",
                "rating": "⭐ 4.6/5",
                "description": "Startup-focused jobs with direct founder interaction",
                "features": ["Direct founder interaction", "Tech & product roles", "Startup culture"],
                "url": "https://wellfound.com",
                "best_for": ["Startups", "Tech Roles", "Product Management"]
            },
            {
                "name": "Apna App",
                "logo": "📱",
                "rating": "⭐ 4.4/5",
                "description": "Local & non-tech jobs, fast-growing in India",
                "features": ["Local jobs", "Fast-growing in India", "Support, sales, ops roles"],
                "url": "https://apna.co",
                "best_for": ["Local Jobs", "Non-Tech Roles", "India Market"]
            },
            {
                "name": "Hirist",
                "logo": "💻",
                "rating": "⭐ 4.5/5",
                "description": "Tech-only job portal for developers and engineers",
                "features": ["Tech-only portal", "Data science, AI, developer roles", "Tech focused"],
                "url": "https://hirist.com",
                "best_for": ["Tech Professionals", "Developers", "AI/ML Roles"]
            }
        ]
        
        # Resume Builders
        self.resume_builders = [
            {
                "name": "Overleaf",
                "logo": "📝",
                "description": "LaTeX-based professional resumes",
                "best_for": "Technical, engineering, research roles",
                "features": ["Excellent ATS-friendly formatting", "Great control over layout", "Clean formatting"],
                "url": "https://overleaf.com",
                "ats_friendly": "Excellent"
            },
            {
                "name": "Novoresume",
                "logo": "🤖",
                "description": "Smart templates optimized for ATS",
                "best_for": "Students, professionals & freshers",
                "features": ["Built-in writing suggestions", "ATS-optimized", "Easy to customize"],
                "url": "https://novoresume.com",
                "ats_friendly": "Excellent"
            },
            {
                "name": "Zety",
                "logo": "✨",
                "description": "AI-based content suggestions",
                "best_for": "Corporate & tech roles",
                "features": ["ATS-safe templates", "Step-by-step creation", "AI suggestions"],
                "url": "https://zety.com",
                "ats_friendly": "Excellent"
            },
            {
                "name": "Resume.io",
                "logo": "📄",
                "description": "Clean, modern templates",
                "best_for": "Global job applications",
                "features": ["ATS-friendly formatting", "Easy to create & download", "Modern templates"],
                "url": "https://resume.io",
                "ats_friendly": "Excellent"
            },
            {
                "name": "Canva",
                "logo": "🎨",
                "description": "Creative yet can be made ATS-friendly",
                "best_for": "Design-focused but ATS compatible",
                "features": ["Creative designs", "Can be ATS-friendly", "Easy PDFs & sharing"],
                "url": "https://canva.com",
                "ats_friendly": "Good (with simple layouts)"
            }
        ]
        
        # ATS Resume Score Evaluators
        self.ats_evaluators = [
            {
                "name": "Jobscan",
                "logo": "⭐",
                "description": "Compares your resume with a job description",
                "features": ["ATS match score (%)", "Keyword & skill gap analysis", "Used by recruiters"],
                "url": "https://jobscan.co",
                "rating": "Most Popular"
            },
            {
                "name": "Resume Worded",
                "logo": "📊",
                "description": "Instant ATS score with bullet-point feedback",
                "features": ["Instant ATS score", "Action verb suggestions", "Impact suggestions"],
                "url": "https://resumeworded.com",
                "rating": "Commonly used on LinkedIn"
            },
            {
                "name": "SkillSyncer",
                "logo": "🔍",
                "description": "Resume vs JD keyword matching",
                "features": ["Keyword matching", "ATS optimization", "Beginner-friendly"],
                "url": "https://skillsyncer.com",
                "rating": "Good for freshers"
            },
            {
                "name": "Zety Resume Checker",
                "logo": "✨",
                "description": "ATS compatibility check with formatting feedback",
                "features": ["ATS compatibility", "Formatting feedback", "Easy to understand"],
                "url": "https://zety.com/resume-checker",
                "rating": "Popular resume platform"
            },
            {
                "name": "Enhancv ATS Check",
                "logo": "📈",
                "description": "ATS readiness score with section-wise feedback",
                "features": ["ATS readiness score", "Section-wise feedback", "Strengths & weaknesses"],
                "url": "https://enhancv.com/resume-checker",
                "rating": "Clean UI, widely used"
            }
        ]
        
        # Free Internship Platforms
        self.internship_platforms = [
            {
                "name": "Internshala",
                "logo": "⭐",
                "description": "Most popular in India for paid & unpaid internships",
                "features": ["Best for students & freshers", "Wide variety", "Indian companies"],
                "url": "https://internshala.com",
                "rating": "Most Popular in India"
            },
            {
                "name": "LinkedIn Internships",
                "logo": "💼",
                "description": "Verified companies with corporate, tech & data roles",
                "features": ["Networking advantage", "Verified companies", "Corporate roles"],
                "url": "https://linkedin.com/jobs/internships",
                "rating": "Professional Network"
            },
            {
                "name": "Indeed Internships",
                "logo": "🌐",
                "description": "Easy & quick apply with direct company postings",
                "features": ["Easy apply", "Direct company postings", "Wide availability"],
                "url": "https://indeed.com/q-internship-jobs.html",
                "rating": "Easy Application"
            },
            {
                "name": "AICTE Internship Portal",
                "logo": "🇮🇳",
                "description": "Government-recognized for engineering & diploma students",
                "features": ["Government recognized", "Safe & authentic", "Engineering focus"],
                "url": "https://internship.aicte-india.org",
                "rating": "Government Authentic"
            },
            {
                "name": "Forage",
                "logo": "🚀",
                "description": "Free virtual internships with real company projects",
                "features": ["Virtual internships", "Real company projects", "Certificate included"],
                "url": "https://theforage.com",
                "rating": "Virtual Experience"
            }
        ]

# Gemini AI Integration with Speech Recognition
class CareerMasterAI:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        self.model_name = "models/gemma-3-4b-it"
        self.recognizer = sr.Recognizer()
    
    def analyze_resume(self, resume_text, job_description=""):
        prompt = f"""
        As a career expert, analyze this resume against the job description:
        
        RESUME:
        {resume_text[:3000]}
        
        {f"JOB DESCRIPTION: {job_description[:1500]}" if job_description else ""}
        
        Provide analysis in this exact format:
        
        ATS_SCORE: [0-100]
        STRENGTHS:
        - [Strength 1]
        - [Strength 2]
        - [Strength 3]
        
        IMPROVEMENTS:
        - [Improvement 1]
        - [Improvement 2]
        - [Improvement 3]
        
        KEYWORDS_MISSING: [Comma separated keywords]
        
        SKILL_GAPS:
        - [Skill 1]
        - [Skill 2]
        - [Skill 3]
        
        ACTIONABLE_STEPS:
        1. [Step 1]
        2. [Step 2]
        3. [Step 3]
        """
        
        try:
            response = self.client.models.generate_content(model=self.model_name, contents=prompt)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def suggest_career_roles(self, skills, interests, education, experience):
        prompt = f"""
        Based on this profile, suggest the top 5 most suitable career roles:
        
        SKILLS: {skills}
        INTERESTS: {interests}
        EDUCATION: {education}
        EXPERIENCE: {experience}
        
        For each role, provide:
        1. Role Name
        2. Match Score (0-100%)
        3. Why it fits
        4. Skills needed
        5. Learning resources (YouTube/Coursera/Udemy links)
        6. Expected salary range
        7. Timeline to transition
        
        Format as a structured JSON-like output.
        """
        
        try:
            response = self.client.models.generate_content(model=self.model_name, contents=prompt)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def generate_roadmap(self, current_level, target_role, timeline):
        prompt = f"""
        Create a personalized career roadmap:
        
        CURRENT LEVEL: {current_level}
        TARGET ROLE: {target_role}
        TIMELINE: {timeline}
        
        Create a month-by-month roadmap with:
        
        MONTH 1-3 (Foundation):
        - Skills to learn
        - Projects to build
        - Certifications
        - Resources
        
        MONTH 4-6 (Intermediate):
        - Advanced skills
        - Complex projects
        - Hackathons
        - Networking
        
        MONTH 7-12 (Advanced):
        - Portfolio polishing
        - Interview prep
        - Job search strategy
        - Mock interviews
        
        Include specific resources (free where possible).
        """
        
        try:
            response = self.client.models.generate_content(model=self.model_name, contents=prompt)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def skill_gap_analysis(self, current_skills, target_role):
        prompt = f"""
        Analyze skill gaps for transitioning to {target_role}:
        
        CURRENT SKILLS: {current_skills}
        TARGET ROLE: {target_role}
        
        Provide:
        
        SKILLS_MATCH: [0-100%]
        
        CRITICAL_GAPS (Must Learn):
        - [Skill 1 with priority]
        - [Skill 2 with priority]
        - [Skill 3 with priority]
        
        LEARNING_RESOURCES:
        - Free resources (YouTube, freeCodeCamp)
        - Paid courses (Coursera, Udemy)
        - Certifications
        - Projects to build
        
        TIMELINE_ESTIMATE: [Weeks/Months]
        
        ACTION_PLAN:
        1. [Immediate action]
        2. [Week 1-2 plan]
        3. [Month 1 plan]
        """
        
        try:
            response = self.client.models.generate_content(model=self.model_name, contents=prompt)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def mock_interview(self, role, experience_level, question_count=5):
        prompt = f"""
        Generate a mock interview for {role} at {experience_level} level:
        
        Generate {question_count} questions covering:
        1. Technical questions
        2. Behavioral questions (STAR format)
        3. System design (if applicable)
        4. Problem-solving
        
        For each question, provide:
        - Question
        - What interviewer looks for
        - Sample answer structure
        - Difficulty level
        
        Also provide:
        - Interview tips
        - Common mistakes to avoid
        - How to prepare
        """
        
        try:
            response = self.client.models.generate_content(model=self.model_name, contents=prompt)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def evaluate_interview_answer(self, question, answer, role):
        prompt = f"""
        Evaluate this interview answer:
        
        QUESTION: {question}
        ANSWER: {answer}
        ROLE: {role}
        
        Provide evaluation in:
        
        SCORE: [0-100]
        
        STRENGTHS:
        - [Strength 1]
        - [Strength 2]
        
        IMPROVEMENTS:
        - [Improvement 1]
        - [Improvement 2]
        
        STAR_METHOD_EVALUATION:
        - Situation: [Score/Feedback]
        - Task: [Score/Feedback]
        - Action: [Score/Feedback]
        - Result: [Score/Feedback]
        
        TECHNICAL_ACCURACY: [Score/Feedback]
        
        COMMUNICATION: [Score/Feedback]
        
        BETTER_ANSWER_SUGGESTION: [Improved answer]
        """
        
        try:
            response = self.client.models.generate_content(model=self.model_name, contents=prompt)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def suggest_hackathons_projects(self, skills, interests, experience_level):
        prompt = f"""
        Suggest hackathons and projects for:
        
        SKILLS: {skills}
        INTERESTS: {interests}
        EXPERIENCE: {experience_level}
        
        Provide:
        
        HACKATHON_RECOMMENDATIONS:
        1. [Hackathon name + platform + why suitable]
        2. [Hackathon name + platform + why suitable]
        3. [Hackathon name + platform + why suitable]
        
        PROJECT_IDEAS (Resume-worthy):
        1. [Project idea + tech stack + difficulty + timeline]
        2. [Project idea + tech stack + difficulty + timeline]
        3. [Project idea + tech stack + difficulty + timeline]
        
        IMPACT_ON_RESUME: How each helps
        
        TIMELINE_SUGGESTION: When to do what
        
        RESOURCES: Where to find more
        """
        
        try:
            response = self.client.models.generate_content(model=self.model_name, contents=prompt)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def calculate_placement_score(self, skills, projects, certifications, resume_score, test_score):
        prompt = f"""
        Calculate placement readiness score based on:
        
        SKILLS_COUNT: {len(skills.split(',')) if skills else 0}
        PROJECTS_COUNT: {len(projects.split(',')) if projects else 0}
        CERTIFICATIONS_COUNT: {len(certifications.split(',')) if certifications else 0}
        RESUME_ATS_SCORE: {resume_score}
        MOCK_TEST_SCORE: {test_score}
        
        Calculate weighted score (0-100):
        - Skills: 30%
        - Projects: 25%
        - Certifications: 15%
        - Resume: 20%
        - Test: 10%
        
        Provide:
        
        FINAL_SCORE: [0-100]
        
        BREAKDOWN:
        - Skills: [score/30]
        - Projects: [score/25]
        - Certifications: [score/15]
        - Resume: [score/20]
        - Test: [score/10]
        
        IMPROVEMENT_AREAS:
        - [Area 1 with priority]
        - [Area 2 with priority]
        - [Area 3 with priority]
        
        TIMELINE_TO_READY: [Estimated timeline]
        
        ACTION_PLAN: Specific steps
        """
        
        try:
            response = self.client.models.generate_content(model=self.model_name, contents=prompt)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def career_chatbot(self, message, conversation_history=""):
        prompt = f"""
        You are CareerMaster Pro AI Mentor - an expert career advisor.
        
        {conversation_history}
        
        User Question: {message}
        
        Provide comprehensive, actionable advice covering:
        - Career guidance
        - Learning paths
        - Interview prep
        - Resume tips
        - Skill development
        - Job search strategy
        
        Be specific, encouraging, and practical.
        Include resources where relevant.
        """
        
        try:
            response = self.client.models.generate_content(model=self.model_name, contents=prompt)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def process_voice_input(self, audio_bytes):
        """Convert audio bytes to text using speech recognition"""
        try:
            # Create a temporary file for the audio
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
                temp_audio.write(audio_bytes)
                temp_audio_path = temp_audio.name
            
            # Use speech recognition
            with sr.AudioFile(temp_audio_path) as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                # Listen to the audio file
                audio_data = self.recognizer.record(source)
                
                # Try Google Speech Recognition
                try:
                    text = self.recognizer.recognize_google(audio_data)
                    return text, "✅ Voice recognized successfully"
                except sr.UnknownValueError:
                    return "", "❌ Could not understand audio"
                except sr.RequestError as e:
                    return "", f"❌ Speech recognition service error: {e}"
                finally:
                    # Clean up temp file
                    if os.path.exists(temp_audio_path):
                        os.unlink(temp_audio_path)
                        
        except Exception as e:
            return "", f"❌ Error processing audio: {str(e)}"

# Initialize data
career_data = CareerData()

# Enhanced Custom CSS with SELECTIVE black text (preserving special elements)
custom_css = """
:root {
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    --warning-gradient: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
    --danger-gradient: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%);
    --card-shadow: 0 20px 40px rgba(0,0,0,0.1);
    --hover-shadow: 0 30px 60px rgba(0,0,0,0.15);
}

/* ==================== SELECTIVE BLACK TEXT (MAIN CONTENT) ==================== */
/* Force black text for main content areas but preserve special elements */
body, .gradio-container, .gr-container, .gr-box, .gr-panel, .gr-form {
    color: #000000 !important;
}

/* Main text elements - black by default */
p:not(.stat-label):not(.chatbot-header):not(.youtube-link):not(.badge):not(.user-message):not(.bot-message),
div:not(.stat-number):not(.progress-fill):not(.badge):not(.skill-badge):not(.platform-badge):not(.user-message):not(.bot-message):not(.chatbot-header):not(.gr-header):not(.gr-header *),
span:not(.stat-number):not(.badge):not(.skill-badge):not(.platform-badge):not(.user-message *):not(.bot-message *):not(.chatbot-header *):not(.gr-header *) {
    color: #000000 !important;
}

/* Headers - black and bold */
h1:not(.gr-header h1), 
h2:not(.gr-header h2), 
h3:not(.gr-header h3), 
h4:not(.gr-header h4), 
h5:not(.gr-header h5), 
h6:not(.gr-header h6) {
    color: #000000 !important;
    font-weight: 800 !important;
}

/* Labels - black and bold */
label, .gr-label, .form-label {
    color: #000000 !important;
    font-weight: 700 !important;
}

/* ================= TAB TEXT FORCE BLACK (EMOJI + TEXT) ================= */

/* All tab buttons */
.gr-tabs button,
.gr-tabs button span,
.gr-tabs button span * {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    font-weight: 700 !important;
}

/* Selected tab */
.gr-tabs button.selected,
.gr-tabs button.selected span,
.gr-tabs button.selected span * {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    font-weight: 800 !important;
}

/* Tab background */
.gr-tabs button {
    background: #e5e7eb !important;
}

.gr-tabs button.selected {
    background: #c7d2fe !important;
}

/* Hover */
.gr-tabs button:hover {
    background: #dbeafe !important;
}


/* ==================== PRESERVED SPECIAL ELEMENTS ==================== */
/* Header - WHITE text */
.gr-header,
.gr-header *,
.gr-header h1,
.gr-header h2,
.gr-header h3,
.gr-header p {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}

/* Stat numbers - GRADIENT text */
.stat-number {
    background: var(--primary-gradient) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    font-size: 3.5rem !important;
    font-weight: 800 !important;
}

/* Badges - WHITE text */
.badge, 
.skill-badge, 
.platform-badge {
    color: white !important;
    -webkit-text-fill-color: white !important;
}

/* YouTube links - WHITE text */
.youtube-link,
.youtube-link * {
    color: white !important;
    -webkit-text-fill-color: white !important;
}

/* Chatbot header - WHITE text */
.chatbot-header,
.chatbot-header * {
    color: white !important;
    -webkit-text-fill-color: white !important;
}

/* Chat messages */
.user-message,
.user-message * {
    color: white !important;
    -webkit-text-fill-color: white !important;
}

.bot-message,
.bot-message * {
    color: #1e293b !important;
    -webkit-text-fill-color: #1e293b !important;
}

/* Button text on gradient backgrounds */
.quick-start-btn,
.platform-btn,
.nav-btn,
.gr-button-primary,
.gr-button-secondary,
.voice-btn {
    color: white !important;
    -webkit-text-fill-color: white !important;
}

.quick-start-btn *,
.platform-btn *,
.nav-btn *,
.gr-button-primary *,
.gr-button-secondary *,
.voice-btn * {
    color: white !important;
    -webkit-text-fill-color: white !important;
}

/* ==================== REST OF YOUR CSS (UNCHANGED) ==================== */
/* Main container */
.gradio-container {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif !important;
    min-height: 100vh;
}

h1 { 
    font-size: 3.5rem !important; 
    text-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
}
h2 { font-size: 2.5rem !important; }
h3 { font-size: 2rem !important; }
h4 { font-size: 1.5rem !important; }
h5 { font-size: 1.25rem !important; }
h6 { font-size: 1.1rem !important; }

/* Header */
.gr-header {
    background: var(--primary-gradient) !important;
    border-radius: 20px !important;
    padding: 40px 30px !important;
    margin-bottom: 30px !important;
    box-shadow: var(--card-shadow) !important;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.gr-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
    animation: shimmer 3s infinite linear;
}

@keyframes shimmer {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

/* Feature Cards */
.feature-card {
    background: white !important;
    border-radius: 20px !important;
    padding: 30px !important;
    margin: 20px 0 !important;
    box-shadow: var(--card-shadow) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    position: relative;
    overflow: hidden;
}

.feature-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 5px;
    background: var(--primary-gradient);
}

.feature-card:hover {
    transform: translateY(-10px) scale(1.02) !important;
    box-shadow: var(--hover-shadow) !important;
}

/* Stats Cards */
.stats-grid {
    display: grid !important;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)) !important;
    gap: 20px !important;
    margin: 30px 0 !important;
}

.stat-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.9) 100%) !important;
    border-radius: 20px !important;
    padding: 25px !important;
    text-align: center !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1) !important;
    transition: all 0.3s ease !important;
    border: 2px solid transparent !important;
}

.stat-card:hover {
    transform: translateY(-5px) !important;
    box-shadow: 0 20px 40px rgba(0,0,0,0.15) !important;
    border-color: rgba(102, 126, 234, 0.2) !important;
}

/* Progress Dashboard */
.progress-dashboard {
    background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.9) 100%) !important;
    border-radius: 20px !important;
    padding: 30px !important;
    margin: 20px 0 !important;
    box-shadow: var(--card-shadow) !important;
}

.progress-bar-container {
    margin: 20px 0 !important;
}

.progress-label {
    display: flex !important;
    justify-content: space-between !important;
    margin-bottom: 8px !important;
    font-weight: 600 !important;
}

.progress-bar {
    height: 12px !important;
    background: #e2e8f0 !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

.progress-fill {
    height: 100% !important;
    background: var(--primary-gradient) !important;
    border-radius: 10px !important;
    transition: width 1s ease-in-out !important;
}

/* Interview System */
.interview-container {
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important;
    border-radius: 20px !important;
    padding: 30px !important;
    margin: 20px 0 !important;
    box-shadow: var(--card-shadow) !important;
}

.interview-question {
    background: white !important;
    border-radius: 15px !important;
    padding: 20px !important;
    margin: 15px 0 !important;
    border-left: 5px solid #667eea !important;
    box-shadow: 0 5px 15px rgba(0,0,0,0.05) !important;
}

.interview-answer {
    background: #f1f5f9 !important;
    border-radius: 15px !important;
    padding: 20px !important;
    margin: 15px 0 !important;
    border-left: 5px solid #10b981 !important;
}

.evaluation-result {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.1) 100%) !important;
    border-radius: 15px !important;
    padding: 20px !important;
    margin: 15px 0 !important;
    border: 2px solid #10b981 !important;
}

/* Role Cards */
.role-grid {
    display: grid !important;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)) !important;
    gap: 25px !important;
    margin: 30px 0 !important;
}

.role-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.9) 100%) !important;
    border-radius: 20px !important;
    padding: 25px !important;
    margin: 10px 0 !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1) !important;
    border: 2px solid transparent !important;
    transition: all 0.3s ease !important;
}

.role-card:hover {
    transform: translateY(-5px) !important;
    box-shadow: 0 20px 40px rgba(0,0,0,0.15) !important;
    border-color: rgba(102, 126, 234, 0.3) !important;
}

.role-header {
    display: flex !important;
    align-items: center !important;
    margin-bottom: 15px !important;
}

.role-icon {
    font-size: 2.5rem !important;
    margin-right: 15px !important;
    background: var(--primary-gradient) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
}

/* Roadmap */
.roadmap-container {
    background: white !important;
    border-radius: 20px !important;
    padding: 30px !important;
    margin: 20px 0 !important;
    box-shadow: var(--card-shadow) !important;
}

.roadmap-phase {
    background: #f8fafc !important;
    border-radius: 15px !important;
    padding: 20px !important;
    margin: 15px 0 !important;
    border-left: 5px solid #8b5cf6 !important;
}

/* Chatbot */
.chatbot-container {
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important;
    border-radius: 20px !important;
    overflow: hidden !important;
    box-shadow: var(--card-shadow) !important;
    height: 600px !important;
}

.chatbot-header {
    background: var(--primary-gradient) !important;
    padding: 20px !important;
    text-align: center !important;
    font-weight: 700 !important;
    font-size: 1.2rem !important;
}

.chat-messages {
    height: 400px !important;
    overflow-y: auto !important;
    padding: 20px !important;
    background: white !important;
}

.chat-message {
    margin: 10px 0 !important;
    padding: 15px 20px !important;
    border-radius: 15px !important;
    max-width: 80% !important;
    animation: fadeIn 0.3s ease !important;
    line-height: 1.5 !important;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.user-message {
    background: var(--primary-gradient) !important;
    margin-left: auto !important;
    border-bottom-right-radius: 5px !important;
}

.bot-message {
    background: #f1f5f9 !important;
    margin-right: auto !important;
    border-bottom-left-radius: 5px !important;
}

.chat-input-area {
    display: flex !important;
    gap: 10px !important;
    padding: 20px !important;
    background: white !important;
    border-top: 2px solid #f1f5f9 !important;
}

/* Voice Mode Styles */
.voice-mode-container {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%) !important;
    border-radius: 15px !important;
    padding: 20px !important;
    margin: 15px 0 !important;
    border: 2px solid #667eea !important;
}

.voice-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 12px 24px !important;
    font-weight: 700 !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 10px !important;
}

.voice-btn:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3) !important;
    font-weight: 800 !important;
}

.voice-btn.recording {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
    animation: pulse 1.5s infinite !important;
}

.voice-status {
    text-align: center !important;
    font-weight: 600 !important;
    margin-top: 10px !important;
}

.audio-input {
    width: 100%;
    margin: 10px 0;
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}

/* Badges */
.badge {
    display: inline-block !important;
    background: var(--primary-gradient) !important;
    padding: 6px 16px !important;
    border-radius: 20px !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    margin: 4px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    box-shadow: 0 3px 10px rgba(102, 126, 234, 0.3) !important;
}

.skill-badge {
    display: inline-block !important;
    background: var(--success-gradient) !important;
    padding: 4px 12px !important;
    border-radius: 12px !important;
    font-size: 11px !important;
    margin: 3px !important;
    font-weight: 500 !important;
}

.platform-badge {
    display: inline-block !important;
    background: var(--warning-gradient) !important;
    padding: 4px 10px !important;
    border-radius: 10px !important;
    font-size: 10px !important;
    margin: 2px !important;
    font-weight: 600 !important;
}

/* Button Styles */
.quick-start-btn {
    border: none !important;
    padding: 15px !important;
    border-radius: 10px !important;
    cursor: pointer !important;
    text-align: center !important;
    transition: all 0.3s ease !important;
    width: 100%;
    font-weight: 600 !important;
}

.quick-start-btn:hover {
    transform: translateY(-3px) !important;
    font-weight: 800 !important;
}

/* Platform buttons */
.platform-btn {
    width: 100%;
    padding: 12px;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    cursor: pointer;
    margin-top: 10px;
    transition: all 0.3s ease;
}

.platform-btn:hover {
    transform: translateY(-3px);
    font-weight: 800 !important;
}

/* Navigation buttons */
.nav-btn {
    border: none;
    padding: 15px;
    border-radius: 10px;
    font-weight: 600;
    cursor: pointer;
    text-align: center;
    transition: all 0.3s ease;
    width: 100%;
}

.nav-btn:hover {
    transform: translateY(-3px);
    font-weight: 800 !important;
}

/* Gradio primary buttons */
.gr-button-primary {
    background: var(--primary-gradient) !important;
    border: none !important;
    font-weight: 700 !important;
    padding: 16px 32px !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    font-size: 1rem !important;
}

.gr-button-primary:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 15px 30px rgba(102, 126, 234, 0.4) !important;
    font-weight: 800 !important;
}

.gr-button-secondary {
    background: var(--secondary-gradient) !important;
    border: none !important;
    font-weight: 700 !important;
    padding: 16px 32px !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
}

.gr-button-secondary:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 15px 30px rgba(245, 87, 108, 0.4) !important;
    font-weight: 800 !important;
}

/* YouTube link styling */
.youtube-link {
    display: inline-flex;
    align-items: center;
    background: #FF0000;
    padding: 8px 16px;
    border-radius: 8px;
    text-decoration: none;
    font-weight: 600;
    margin: 5px;
    transition: all 0.3s ease;
}

.youtube-link:hover {
    background: #CC0000;
    transform: translateY(-2px);
    font-weight: 800 !important;
}

.youtube-link i {
    margin-right: 8px;
}

/* Resource card styling */
.resource-card {
    background: white;
    border-radius: 15px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    border-left: 4px solid #667eea;
    transition: all 0.3s ease;
}

.resource-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}

/* Typography */
p {
    line-height: 1.7 !important;
    margin-bottom: 16px !important;
    font-size: 1.1rem !important;
    font-weight: 500 !important;
}

/* Tabs */
.gr-tabs button {
    background: rgba(102, 126, 234, 0.15) !important;
    border-radius: 10px 10px 0 0 !important;
    padding: 12px 24px !important;
    font-weight: 700 !important;
    transition: all 0.3s ease !important;
}

.gr-tabs button.selected {
    background: var(--primary-gradient) !important;
    font-weight: 800 !important;
}

.gr-tabs button:hover {
    background: #000000 !important;
}

/* Footer */
.footer {
    text-align: center !important;
    padding: 40px 20px !important;
    font-size: 14px !important;
    margin-top: 50px !important;
    border-top: 2px solid #f1f5f9 !important;
    background: white !important;
    border-radius: 20px !important;
    margin: 30px 0 !important;
    box-shadow: var(--card-shadow) !important;
}

.footer h3 {
    margin-bottom: 20px !important;
}

/* Responsive */
@media (max-width: 768px) {
    .role-grid {
        grid-template-columns: 1fr !important;
    }
    
    .stats-grid {
        grid-template-columns: repeat(2, 1fr) !important;
    }
    
    .feature-card {
        padding: 20px !important;
    }
    
    h1 { font-size: 2.5rem !important; }
    h2 { font-size: 2rem !important; }
    h3 { font-size: 1.5rem !important; }
    
    .chatbot-container {
        height: 500px !important;
    }
}

/* ... all your existing CSS ... */

/* Textbox styling */
.gr-textbox textarea, .gr-textbox input {
    border-radius: 12px !important;
    border: 2px solid #e2e8f0 !important;
    padding: 16px !important;
    font-size: 16px !important;
    transition: all 0.3s ease !important;
}

.gr-textbox textarea:focus, .gr-textbox input:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    outline: none !important;
}

/* ==================== TAB TEXT ONLY - BLACK ==================== */
/* Target ONLY the specific tab section */
.gr-tabs button span,
.gr-tabs .tab-nav button span {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}
"""

# Create Gradio Interface
def create_interface():
    with gr.Blocks(title="🚀 Career Master") as demo:
        # Header
        gr.Markdown("""
        <div class="gr-header">
            <h1>🚀 Career Master</h1>
            <p>Your Complete AI-Powered Career Development Ecosystem</p>
        </div>
        """)
        
        # Features Overview
        gr.Markdown("""
        <div class="feature-card">
            <h2>🌟 FEATURES OF CAREER MASTER</h2>
            <p>All career resources in one platform - no more switching between 15+ websites</p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 30px;">
                <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1)); padding: 20px; border-radius: 15px; border-left: 5px solid #667eea;">
                    <h4>🌐 Unified Career Ecosystem</h4>
                    <p>All career resources in one platform - no more switching between 15+ websites</p>
                </div>
                <div style="background: linear-gradient(135deg, rgba(240, 147, 251, 0.1), rgba(245, 87, 108, 0.1)); padding: 20px; border-radius: 15px; border-left: 5px solid #f093fb;">
                    <h4>🤖 AI Career Role Suggester</h4>
                    <p>Personalized role recommendations based on skills, interests & background</p>
                </div>
                <div style="background: linear-gradient(135deg, rgba(79, 172, 254, 0.1), rgba(0, 242, 254, 0.1)); padding: 20px; border-radius: 15px; border-left: 5px solid #4facfe;">
                    <h4>🧭 Personalized Roadmap Generator</h4>
                    <p>Month-by-month roadmap tailored to your career goals</p>
                </div>
                <div style="background: linear-gradient(135deg, rgba(246, 211, 101, 0.1), rgba(253, 160, 133, 0.1)); padding: 20px; border-radius: 15px; border-left: 5px solid #f6d365;">
                    <h4>📊 AI Resume Analyzer & Builder</h4>
                    <p>ATS-optimized scoring with keyword gap detection</p>
                </div>
                <div style="background: linear-gradient(135deg, rgba(255, 154, 158, 0.1), rgba(250, 208, 196, 0.1)); padding: 20px; border-radius: 15px; border-left: 5px solid #ff9a9e;">
                    <h4>🎤 AI Mock Interview System</h4>
                    <p>Role-based interviews with STAR-method evaluation</p>
                </div>
                <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(5, 150, 105, 0.1)); padding: 20px; border-radius: 15px; border-left: 5px solid #10b981;">
                    <h4>📚 Free Certifications</h4>
                    <p>Platforms for free certificates & learning paths</p>
                </div>
                <div style="background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(217, 119, 6, 0.1)); padding: 20px; border-radius: 15px; border-left: 5px solid #f59e0b;">
                    <h4>💼 Job Platforms</h4>
                    <p>Job applying platforms with ratings & features</p>
                </div>
                <div style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(124, 58, 237, 0.1)); padding: 20px; border-radius: 15px; border-left: 5px solid #8b5cf6;">
                    <h4>📝 Resume Builders</h4>
                    <p>ATS-friendly resume builders</p>
                </div>
                <div style="background: linear-gradient(135deg, rgba(236, 72, 153, 0.1), rgba(219, 39, 119, 0.1)); padding: 20px; border-radius: 15px; border-left: 5px solid #ec4899;">
                    <h4>🔍 ATS Evaluators</h4>
                    <p>Platforms to check your resume ATS score</p>
                </div>
                <div style="background: linear-gradient(135deg, rgba(6, 182, 212, 0.1), rgba(8, 145, 178, 0.1)); padding: 20px; border-radius: 15px; border-left: 5px solid #06b6d4;">
                    <h4>🏆 Internship Platforms</h4>
                    <p>Free internship platforms for students</p>
                </div>
            </div>
        </div>
        """)
        
        # API Configuration
        with gr.Row():
            with gr.Column(scale=3):
                api_key = gr.Textbox(
                    label="🔑 Google Gemini API Key",
                    placeholder="Enter your API key to unlock all AI features...",
                    type="password",
                    info="Required for AI-powered features"
                )
            
            with gr.Column(scale=1):
                api_status = gr.Textbox(
                    label="Status",
                    value="⏳ Enter API key and click Configure",
                    interactive=False
                )
                configure_btn = gr.Button("⚡ Configure AI", variant="primary", size="lg")
        
        career_ai = [None]
        conversation_history = [""]
        
        def configure_api(api_key):
            if not api_key:
                return "❌ Please enter an API key"
            try:
                career_ai[0] = CareerMasterAI(api_key)
                conversation_history[0] = ""
                return "✅ AI Configured Successfully! All features unlocked."
            except Exception as e:
                return f"❌ Configuration failed: {str(e)}"
        
        configure_btn.click(configure_api, inputs=[api_key], outputs=[api_status])
        
        # Main Tabs - Text changed to BLACK
        with gr.Tabs() as tabs:
            # Dashboard
            with gr.Tab("🏠 Dashboard"):
                create_dashboard_tab(career_ai)
            
            # AI Career Role Suggester
            with gr.Tab("🤖 AI Role Suggester"):
                create_role_suggester_tab(career_ai)
            
            # Personalized Roadmap Generator
            with gr.Tab("🧭 Career Roadmap"):
                create_roadmap_generator_tab(career_ai)
            
            # AI Resume Analyzer
            with gr.Tab("📊 Resume Analyzer"):
                create_resume_analyzer_tab(career_ai)
            
            # Skill Gap Analyzer
            with gr.Tab("📈 Skill Gap Analyzer"):
                create_skill_gap_tab(career_ai)
            
            # Placement Readiness Score
            with gr.Tab("🚀 Placement Score"):
                create_placement_score_tab(career_ai)
            
            # AI Mock Interview System
            with gr.Tab("🎤 Mock Interviews"):
                create_mock_interview_tab(career_ai)
            
            # Hackathon & Project Recommender
            with gr.Tab("🏆 Hackathons & Projects"):
                create_hackathon_project_tab(career_ai)
            
            # Coding Platforms
            with gr.Tab("💻 Coding Platforms"):
                create_coding_platforms_tab()
            
            # Learning Progress Dashboard
            with gr.Tab("📊 Progress Tracker"):
                create_progress_tracker_tab(career_ai)
            
            # AI Career Mentor Chatbot with Voice Mode
            with gr.Tab("💬 AI Mentor"):
                create_career_chatbot_tab(career_ai, conversation_history)
            
            # Career Resources
            with gr.Tab("📚 Career Resources"):
                create_career_resources_tab()
            
            # Unified Resources
            with gr.Tab("🌐 All Resources"):
                create_unified_resources_tab()
        
        # Footer
        gr.Markdown("""
        <div class="footer">
            <h3>🚀 Career Master Pro</h3>
            <p>Your Complete Career Development Ecosystem</p>
            <p style="font-size: 12px; color: #94a3b8; font-weight: 500;">
                © 2024 Career Master Pro • 10 Premium Features • AI Powered by Google Gemini • Made for Career Success
            </p>
        </div>
        """)
        
        return demo

def create_dashboard_tab(career_ai):
    with gr.Column():
        # Stats Overview
        gr.Markdown("""
        <div class="stats-grid">
            <div class="stat-card">
                <div style="font-size: 2.5rem; margin-bottom: 10px;">🌐</div>
                <div class="stat-number">12</div>
                <div>Integrated Features</div>
                <div>Unified Career Platform</div>
            </div>
            <div class="stat-card">
                <div style="font-size: 2.5rem; margin-bottom: 10px;">💼</div>
                <div class="stat-number">20+</div>
                <div>Career Roles</div>
                <div>With YouTube Learning Links</div>
            </div>
            <div class="stat-card">
                <div style="font-size: 2.5rem; margin-bottom: 10px;">📚</div>
                <div class="stat-number">50+</div>
                <div>Resources</div>
                <div>Platforms & Tools</div>
            </div>
            <div class="stat-card">
                <div style="font-size: 2.5rem; margin-bottom: 10px;">🚀</div>
                <div class="stat-number">24/7</div>
                <div>AI Support</div>
                <div>Career Guidance</div>
            </div>
        </div>
        """)
        
        # Quick Start
        gr.Markdown("""
        <div class="feature-card">
            <h3>⚡ Quick Start</h3>
            <p>Get started with these essential features:</p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin-top: 20px;">
                <button onclick="document.querySelector('#role-tab button').click()" class="quick-start-btn" style="background: var(--primary-gradient);">
                    🤖 Find Your Career Role
                </button>
                <button onclick="document.querySelector('#resume-tab button').click()" class="quick-start-btn" style="background: var(--secondary-gradient);">
                    📊 Analyze Your Resume
                </button>
                <button onclick="document.querySelector('#roadmap-tab button').click()" class="quick-start-btn" style="background: var(--success-gradient);">
                    🧭 Get Personalized Roadmap
                </button>
                <button onclick="document.querySelector('#interview-tab button').click()" class="quick-start-btn" style="background: var(--warning-gradient);">
                    🎤 Practice Mock Interviews
                </button>
                <button onclick="document.querySelector('#resources-tab button').click()" class="quick-start-btn" style="background: var(--danger-gradient);">
                    📚 Explore Resources
                </button>
            </div>
        </div>
        """)
        
        # Recent Activity
        gr.Markdown("""
        <div class="feature-card">
            <h3>📈 Your Career Progress</h3>
            <div class="progress-dashboard">
                <div class="progress-bar-container">
                    <div class="progress-label">
                        <span>Skills Development</span>
                        <span>65%</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: 65%;"></div>
                    </div>
                </div>
                <div class="progress-bar-container">
                    <div class="progress-label">
                        <span>Resume Optimization</span>
                        <span>80%</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: 80%;"></div>
                    </div>
                </div>
                <div class="progress-bar-container">
                    <div class="progress-label">
                        <span>Interview Readiness</span>
                        <span>45%</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: 45%;"></div>
                    </div>
                </div>
                <div class="progress-bar-container">
                    <div class="progress-label">
                        <span>Placement Readiness</span>
                        <span>70%</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: 70%;"></div>
                    </div>
                </div>
            </div>
        </div>
        """)

def create_role_suggester_tab(career_ai):
    with gr.Column():
        gr.Markdown("""
        <div class="feature-card">
            <h2>🤖 AI-Powered Career Role Suggester</h2>
            <p>Get personalized career role recommendations based on your profile</p>
        </div>
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                skills_input = gr.Textbox(
                    label="🛠️ Your Skills",
                    placeholder="e.g., Python, JavaScript, React, SQL, Communication, Problem-solving",
                    lines=3
                )
                
                interests_input = gr.Textbox(
                    label="❤️ Your Interests",
                    placeholder="e.g., Web Development, Data Analysis, AI/ML, Cybersecurity, UI/UX Design",
                    lines=3
                )
                
                education_input = gr.Textbox(
                    label="🎓 Education Background",
                    placeholder="e.g., B.Tech Computer Science, BCA, Diploma in IT, Self-taught",
                    lines=2
                )
                
                experience_input = gr.Textbox(
                    label="📅 Experience Level",
                    placeholder="e.g., Fresher, 0-2 years, Internship experience, Projects completed",
                    lines=2
                )
                
                suggest_btn = gr.Button("🚀 Get Role Suggestions", variant="primary", size="lg")
            
            with gr.Column(scale=2):
                suggestions_output = gr.Textbox(
                    label="🎯 Recommended Career Roles",
                    lines=20,
                    interactive=False
                )
        
        # Display career roles with YouTube links
        gr.Markdown("""
        <div class="feature-card">
            <h3>🌟 Popular Career Roles with YouTube Learning Links</h3>
        </div>
        """)
        
        html = "<div class='role-grid'>"
        for role_name, role_data in career_data.career_roles.items():
            youtube_links = ""
            if "youtube_links" in role_data and role_data["youtube_links"]:
                youtube_links = "<div style='margin-top: 10px;'><strong>🎬 YouTube Learning:</strong><br>"
                for i, link in enumerate(role_data["youtube_links"][:2]):
                    youtube_links += f"""<a href='{link}' target='_blank' class='youtube-link'>
                    <i>▶️</i> Video {i+1}
                    </a>"""
                youtube_links += "</div>"
            
            html += f"""
            <div class="role-card">
                <div class="role-header">
                    <div class="role-icon">{role_data.get('logo', '💼')}</div>
                    <div>
                        <h4>{role_name}</h4>
                        <div style="color: #10b981; font-weight: 600;">{role_data.get('salary', role_data.get('salary_range', 'Not specified'))}</div>
                    </div>
                </div>
                <p>{role_data.get('description', '')}</p>
                <div style="margin: 15px 0;">
                    <div style="font-size: 12px; margin-bottom: 6px; font-weight: 600;">SKILLS NEEDED:</div>
                    <div>{" ".join([f"<span class='skill-badge'>{skill}</span>" for skill in role_data.get('skills', [])[:4]])}</div>
                </div>
                <div style="margin: 10px 0;">
                    <div style="font-size: 12px; margin-bottom: 6px; font-weight: 600;">EXPERIENCE:</div>
                    <span class="badge">{role_data.get('experience', 'Not specified')}</span>
                </div>
                {youtube_links}
            </div>
            """
        html += "</div>"
        gr.HTML(html)
        
        def get_role_suggestions(skills, interests, education, experience):
            if career_ai[0] is None:
                return "Please configure Gemini API key first"
            
            if not skills.strip():
                return "Please enter your skills"
            
            suggestions = career_ai[0].suggest_career_roles(skills, interests, education, experience)
            
            # Format output
            formatted = "🌟 **AI Career Role Recommendations** 🌟\n\n"
            formatted += f"**Skills:** {skills}\n"
            formatted += f"**Interests:** {interests}\n"
            formatted += f"**Education:** {education}\n"
            formatted += f"**Experience:** {experience}\n\n"
            formatted += "---\n\n"
            formatted += suggestions
            
            return formatted
        
        suggest_btn.click(
            get_role_suggestions,
            inputs=[skills_input, interests_input, education_input, experience_input],
            outputs=[suggestions_output]
        )

def create_roadmap_generator_tab(career_ai):
    with gr.Column():
        gr.Markdown("""
        <div class="feature-card">
            <h2>🧭 Personalized Career Roadmap Generator</h2>
            <p>Get a month-by-month roadmap tailored to your career goals</p>
        </div>
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                current_level = gr.Dropdown(
                    label="📊 Your Current Level",
                    choices=["Beginner (0-6 months)", "Intermediate (6-18 months)", "Advanced (18+ months)"],
                    value="Beginner (0-6 months)"
                )
                
                target_role = gr.Dropdown(
                    label="🎯 Target Career Role",
                    choices=list(career_data.career_roles.keys()),
                    value="Software Engineer"
                )
                
                timeline = gr.Dropdown(
                    label="⏱️ Desired Timeline",
                    choices=["3 months", "6 months", "1 year", "2 years"],
                    value="1 year"
                )
                
                additional_notes = gr.Textbox(
                    label="📝 Additional Notes",
                    placeholder="Any specific technologies or preferences...",
                    lines=3
                )
                
                generate_btn = gr.Button("🚀 Generate Roadmap", variant="primary", size="lg")
            
            with gr.Column(scale=2):
                roadmap_output = gr.Textbox(
                    label="📅 Your Personalized Roadmap",
                    lines=25,
                    interactive=False
                )
        
        def generate_roadmap(current_level_val, target_role_val, timeline_val, notes):
            if career_ai[0] is None:
                return "Please configure Gemini API key first"
            
            roadmap = career_ai[0].generate_roadmap(current_level_val, target_role_val, timeline_val)
            
            formatted = f"🎯 **Personalized Career Roadmap for {target_role_val}**\n\n"
            formatted += f"**Current Level:** {current_level_val}\n"
            formatted += f"**Target Timeline:** {timeline_val}\n"
            if notes:
                formatted += f"**Notes:** {notes}\n"
            formatted += "\n" + "="*50 + "\n\n"
            formatted += roadmap
            
            return formatted
        
        generate_btn.click(
            generate_roadmap,
            inputs=[current_level, target_role, timeline, additional_notes],
            outputs=[roadmap_output]
        )

def create_resume_analyzer_tab(career_ai):
    with gr.Column():
        gr.Markdown("""
        <div class="feature-card">
            <h2>📊 AI Resume Analyzer & Builder</h2>
            <p>Get ATS-optimized resume analysis with keyword gap detection</p>
        </div>
        """)
        
        with gr.Row():
            with gr.Column(scale=2):
                resume_text = gr.Textbox(
                    label="📝 Paste Your Resume",
                    placeholder="Paste your complete resume text here...",
                    lines=15
                )
                
                job_description = gr.Textbox(
                    label="🎯 Target Job Description (Optional)",
                    placeholder="Paste the job description for targeted analysis...",
                    lines=8
                )
                
                analyze_btn = gr.Button("🔍 Analyze Resume", variant="primary", size="lg")
            
            with gr.Column(scale=3):
                analysis_output = gr.Textbox(
                    label="📈 Analysis Results",
                    lines=25,
                    interactive=False
                )
        
        def analyze_resume(resume_text_input, job_desc):
            if career_ai[0] is None:
                return "Please configure Gemini API key first"
            
            if not resume_text_input.strip():
                return "Please provide your resume text"
            
            analysis = career_ai[0].analyze_resume(resume_text_input, job_desc)
            
            formatted = "📊 **AI Resume Analysis Report**\n\n"
            formatted += f"**Resume Length:** {len(resume_text_input)} characters\n"
            if job_desc:
                formatted += "**Analysis Type:** Targeted (Job Description Provided)\n"
            else:
                formatted += "**Analysis Type:** General (No Job Description)\n"
            formatted += "\n" + "="*50 + "\n\n"
            formatted += analysis
            
            return formatted
        
        analyze_btn.click(
            analyze_resume,
            inputs=[resume_text, job_description],
            outputs=[analysis_output]
        )

def create_skill_gap_tab(career_ai):
    with gr.Column():
        gr.Markdown("""
        <div class="feature-card">
            <h2>📈 Skill Gap Analyzer</h2>
            <p>Identify gaps between your current skills and industry requirements</p>
        </div>
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                current_skills = gr.Textbox(
                    label="🛠️ Your Current Skills",
                    placeholder="e.g., Python, HTML/CSS, JavaScript basics, SQL",
                    lines=4
                )
                
                target_role_skill = gr.Dropdown(
                    label="🎯 Target Role",
                    choices=list(career_data.career_roles.keys()),
                    value="Software Engineer"
                )
                
                analyze_gap_btn = gr.Button("🔍 Analyze Skill Gaps", variant="primary", size="lg")
            
            with gr.Column(scale=2):
                gap_analysis_output = gr.Textbox(
                    label="📊 Skill Gap Analysis",
                    lines=25,
                    interactive=False
                )
        
        # Industry Skills Display
        gr.Markdown("""
        <div class="feature-card">
            <h3>🏢 Industry Skill Requirements</h3>
        </div>
        """)
        
        html = ""
        for domain, skills_dict in career_data.industry_skills.items():
            html += f"""
            <div style="background: white; border-radius: 15px; padding: 20px; margin: 15px 0; box-shadow: 0 5px 15px rgba(0,0,0,0.05);">
                <h4 style="margin: 0 0 15px 0;">{domain}</h4>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
            """
            for skill_type, skills in skills_dict.items():
                html += f"""
                <div>
                    <div style="font-size: 12px; margin-bottom: 8px; font-weight: 600; text-transform: uppercase;">{skill_type.replace('_', ' ').title()}</div>
                    <div>{" ".join([f"<span class='skill-badge'>{skill}</span>" for skill in skills[:5]])}</div>
                </div>
                """
            html += "</div></div>"
        
        gr.HTML(html)
        
        def analyze_skill_gaps(current_skills_input, target_role_input):
            if career_ai[0] is None:
                return "Please configure Gemini API key first"
            
            if not current_skills_input.strip():
                return "Please enter your current skills"
            
            analysis = career_ai[0].skill_gap_analysis(current_skills_input, target_role_input)
            
            formatted = f"📊 **Skill Gap Analysis for {target_role_input}**\n\n"
            formatted += f"**Current Skills:** {current_skills_input}\n\n"
            formatted += "="*50 + "\n\n"
            formatted += analysis
            
            return formatted
        
        analyze_gap_btn.click(
            analyze_skill_gaps,
            inputs=[current_skills, target_role_skill],
            outputs=[gap_analysis_output]
        )

def create_placement_score_tab(career_ai):
    with gr.Column():
        gr.Markdown("""
        <div class="feature-card">
            <h2>🚀 Placement Readiness Score (0-100)</h2>
            <p>Calculate your placement readiness with detailed breakdown</p>
        </div>
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                skills_count = gr.Number(
                    label="🛠️ Number of Skills",
                    value=5,
                    minimum=0,
                    maximum=50
                )
                
                projects_count = gr.Number(
                    label="💼 Number of Projects",
                    value=2,
                    minimum=0,
                    maximum=20
                )
                
                certifications_count = gr.Number(
                    label="📜 Number of Certifications",
                    value=1,
                    minimum=0,
                    maximum=20
                )
                
                resume_score = gr.Slider(
                    label="📄 Resume ATS Score",
                    minimum=0,
                    maximum=100,
                    value=65,
                    step=1
                )
                
                test_score = gr.Slider(
                    label="📝 Mock Test Score",
                    minimum=0,
                    maximum=100,
                    value=70,
                    step=1
                )
                
                calculate_btn = gr.Button("🧮 Calculate Score", variant="primary", size="lg")
            
            with gr.Column(scale=2):
                score_output = gr.Textbox(
                    label="📊 Placement Readiness Report",
                    lines=25,
                    interactive=False
                )
        
        def calculate_placement_score(skills, projects, certifications, resume, test):
            if career_ai[0] is None:
                return "Please configure Gemini API key first"
            
            score = career_ai[0].calculate_placement_score(
                str(skills), str(projects), str(certifications), str(resume), str(test)
            )
            
            formatted = "🚀 **Placement Readiness Score Report**\n\n"
            formatted += "**Input Metrics:**\n"
            formatted += f"- Skills: {skills}\n"
            formatted += f"- Projects: {projects}\n"
            formatted += f"- Certifications: {certifications}\n"
            formatted += f"- Resume ATS Score: {resume}/100\n"
            formatted += f"- Mock Test Score: {test}/100\n\n"
            formatted += "="*50 + "\n\n"
            formatted += score
            
            return formatted
        
        calculate_btn.click(
            calculate_placement_score,
            inputs=[skills_count, projects_count, certifications_count, resume_score, test_score],
            outputs=[score_output]
        )

def create_mock_interview_tab(career_ai):
    with gr.Column():
        gr.Markdown("""
        <div class="feature-card">
            <h2>🎤 AI Mock Interview System</h2>
            <p>Practice role-based interviews with AI evaluation</p>
        </div>
        """)
        
        # Interview Generator
        with gr.Row():
            with gr.Column(scale=1):
                interview_role = gr.Dropdown(
                    label="🎯 Interview Role",
                    choices=list(career_data.career_roles.keys()),
                    value="Software Engineer"
                )
                
                experience_level = gr.Dropdown(
                    label="📊 Experience Level",
                    choices=["Fresher", "0-2 years", "2-5 years", "5+ years"],
                    value="Fresher"
                )
                
                question_count = gr.Slider(
                    label="🔢 Number of Questions",
                    minimum=3,
                    maximum=10,
                    value=5,
                    step=1
                )
                
                generate_interview_btn = gr.Button("🎬 Generate Interview", variant="primary", size="lg")
            
            with gr.Column(scale=2):
                interview_output = gr.Textbox(
                    label="📝 Interview Questions",
                    lines=20,
                    interactive=False
                )
        
        # Interview Answer Evaluation
        gr.Markdown("""
        <div class="feature-card" style="margin-top: 30px;">
            <h3>📊 Answer Evaluation</h3>
        </div>
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                question = gr.Textbox(
                    label="❓ Interview Question",
                    placeholder="Paste the interview question here...",
                    lines=3
                )
                
                answer = gr.Textbox(
                    label="💬 Your Answer",
                    placeholder="Type your answer here...",
                    lines=6
                )
                
                answer_role = gr.Dropdown(
                    label="🎯 Role Context",
                    choices=list(career_data.career_roles.keys()),
                    value="Software Engineer"
                )
                
                evaluate_btn = gr.Button("📈 Evaluate Answer", variant="primary", size="lg")
            
            with gr.Column(scale=2):
                evaluation_output = gr.Textbox(
                    label="📊 Evaluation Results",
                    lines=25,
                    interactive=False
                )
        
        def generate_interview(role, level, count):
            if career_ai[0] is None:
                return "Please configure Gemini API key first"
            
            interview = career_ai[0].mock_interview(role, level, int(count))
            
            formatted = f"🎤 **Mock Interview for {role} ({level})**\n\n"
            formatted += f"**Questions:** {count}\n"
            formatted += "="*50 + "\n\n"
            formatted += interview
            
            return formatted
        
        def evaluate_answer(question_input, answer_input, role_input):
            if career_ai[0] is None:
                return "Please configure Gemini API key first"
            
            if not question_input.strip() or not answer_input.strip():
                return "Please provide both question and answer"
            
            evaluation = career_ai[0].evaluate_interview_answer(question_input, answer_input, role_input)
            
            formatted = "📊 **Interview Answer Evaluation**\n\n"
            formatted += f"**Role:** {role_input}\n"
            formatted += f"**Question:** {question_input}\n\n"
            formatted += "="*50 + "\n\n"
            formatted += evaluation
            
            return formatted
        
        generate_interview_btn.click(
            generate_interview,
            inputs=[interview_role, experience_level, question_count],
            outputs=[interview_output]
        )
        
        evaluate_btn.click(
            evaluate_answer,
            inputs=[question, answer, answer_role],
            outputs=[evaluation_output]
        )

def create_hackathon_project_tab(career_ai):
    with gr.Column():
        gr.Markdown("""
        <div class="feature-card">
            <h2>🏆 Hackathon & Project Recommendation Engine</h2>
            <p>Get personalized hackathon and project recommendations</p>
        </div>
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                hp_skills = gr.Textbox(
                    label="🛠️ Your Skills",
                    placeholder="e.g., React, Node.js, Python, ML basics",
                    lines=3
                )
                
                hp_interests = gr.Textbox(
                    label="❤️ Your Interests",
                    placeholder="e.g., Web Development, AI, Blockchain, IoT",
                    lines=3
                )
                
                hp_experience = gr.Dropdown(
                    label="📊 Experience Level",
                    choices=["Beginner", "Intermediate", "Advanced"],
                    value="Beginner"
                )
                
                suggest_hp_btn = gr.Button("🚀 Get Recommendations", variant="primary", size="lg")
            
            with gr.Column(scale=2):
                hp_output = gr.Textbox(
                    label="🎯 Recommendations",
                    lines=25,
                    interactive=False
                )
        
        def suggest_hackathons_projects(skills, interests, experience):
            if career_ai[0] is None:
                return "Please configure Gemini API key first"
            
            if not skills.strip():
                return "Please enter your skills"
            
            suggestions = career_ai[0].suggest_hackathons_projects(skills, interests, experience)
            
            formatted = "🏆 **Hackathon & Project Recommendations**\n\n"
            formatted += f"**Skills:** {skills}\n"
            formatted += f"**Interests:** {interests}\n"
            formatted += f"**Experience:** {experience}\n\n"
            formatted += "="*50 + "\n\n"
            formatted += suggestions
            
            return formatted
        
        suggest_hp_btn.click(
            suggest_hackathons_projects,
            inputs=[hp_skills, hp_interests, hp_experience],
            outputs=[hp_output]
        )

def create_coding_platforms_tab():
    with gr.Column():
        gr.Markdown("""
        <div class="feature-card">
            <h2>💻 Top Coding Practice Platforms</h2>
            <p>Master coding skills through these top platforms for DSA, competitive programming, and interview prep</p>
        </div>
        """)
        
        # Coding platforms in a grid
        html = "<div class='role-grid'>"
        for platform in career_data.coding_platforms:
            html += f"""
            <div class="role-card">
                <div class="role-header">
                    <div class="role-icon">{platform['logo']}</div>
                    <div>
                        <h4>{platform['name']}</h4>
                        <div style="color: #10b981; font-weight: 600;">{platform['rating']}</div>
                    </div>
                </div>
                <p>{platform['description']}</p>
                <div style="margin: 15px 0;">
                    <div style="font-size: 12px; margin-bottom: 6px; font-weight: 600;">FEATURES:</div>
                    <div style="font-size: 14px;">{" • ".join(platform['features'][:2])}</div>
                </div>
                <div style="margin: 10px 0;">
                    <div style="font-size: 12px; margin-bottom: 6px; font-weight: 600;">BEST FOR:</div>
                    <div>{" ".join([f"<span class='skill-badge'>{bf}</span>" for bf in platform['best_for'][:2]])}</div>
                </div>
                <div style="margin: 10px 0;">
                    <div style="font-size: 12px; margin-bottom: 6px; font-weight: 600;">DIFFICULTY:</div>
                    <div>{" ".join([f"<span class='platform-badge'>{d}</span>" for d in platform['difficulty'][:2]])}</div>
                </div>
                <div style="margin: 10px 0;">
                    <div style="font-size: 12px; margin-bottom: 6px; font-weight: 600;">PRICING:</div>
                    <span class="badge" style="background: linear-gradient(135deg, #3b82f6, #1d4ed8);">{platform['pricing']}</span>
                </div>
                <a href="{platform['url']}" target="_blank">
                    <button class="platform-btn" style="background: linear-gradient(135deg, #667eea, #764ba2);">
                        Visit Platform →
                    </button>
                </a>
            </div>
            """
        html += "</div>"
        gr.HTML(html)

def create_progress_tracker_tab(career_ai):
    with gr.Column():
        gr.Markdown("""
        <div class="feature-card">
            <h2>📊 Learning Progress Dashboard</h2>
            <p>Track your career development progress</p>
        </div>
        """)
        
        # Progress Input
        with gr.Row():
            with gr.Column(scale=1):
                completed_skills = gr.Textbox(
                    label="✅ Skills Learned",
                    placeholder="List skills you've learned (comma separated)",
                    lines=3
                )
                
                completed_projects = gr.Textbox(
                    label="💼 Projects Completed",
                    placeholder="List projects completed",
                    lines=3
                )
                
                completed_certifications = gr.Textbox(
                    label="📜 Certifications Earned",
                    placeholder="List certifications completed",
                    lines=3
                )
                
                job_applications = gr.Number(
                    label="📨 Job Applications",
                    value=0,
                    minimum=0
                )
                
                interviews_attended = gr.Number(
                    label="🎤 Interviews Attended",
                    value=0,
                    minimum=0
                )
                
                update_progress_btn = gr.Button("📈 Update Progress", variant="primary", size="lg")
            
            with gr.Column(scale=2):
                progress_output = gr.Textbox(
                    label="📊 Progress Report",
                    lines=20,
                    interactive=False
                )
        
        # Progress Visualization
        gr.Markdown("""
        <div class="feature-card">
            <h3>📈 Progress Visualization</h3>
            <div class="progress-dashboard">
                <div class="progress-bar-container">
                    <div class="progress-label">
                        <span>Skills Development</span>
                        <span>0%</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: 0%;"></div>
                    </div>
                </div>
                <div class="progress-bar-container">
                    <div class="progress-label">
                        <span>Project Completion</span>
                        <span>0%</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: 0%;"></div>
                    </div>
                </div>
                <div class="progress-bar-container">
                    <div class="progress-label">
                        <span>Certification Goals</span>
                        <span>0%</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: 0%;"></div>
                    </div>
                </div>
                <div class="progress-bar-container">
                    <div class="progress-label">
                        <span>Job Search Progress</span>
                        <span>0%</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: 0%;"></div>
                    </div>
                </div>
            </div>
        </div>
        """)
        
        def update_progress(skills, projects, certifications, applications, interviews):
            # Calculate progress metrics
            skill_count = len([s.strip() for s in skills.split(',') if s.strip()])
            project_count = len([p.strip() for p in projects.split(',') if p.strip()])
            cert_count = len([c.strip() for c in certifications.split(',') if c.strip()])
            
            report = "📊 **Progress Dashboard Report**\n\n"
            report += f"**Skills Learned:** {skill_count}\n"
            report += f"**Projects Completed:** {project_count}\n"
            report += f"**Certifications Earned:** {cert_count}\n"
            report += f"**Job Applications:** {applications}\n"
            report += f"**Interviews Attended:** {interviews}\n\n"
            
            report += "🎯 **Next Steps:**\n"
            if skill_count < 5:
                report += "- Focus on learning core skills for your target role\n"
            if project_count < 2:
                report += "- Build at least 2 portfolio projects\n"
            if cert_count < 1:
                report += "- Complete relevant certifications\n"
            if applications < 10:
                report += "- Increase job applications\n"
            if interviews < 3:
                report += "- Practice more mock interviews\n"
            
            report += "\n📅 **Weekly Goal:**\n"
            report += "- Learn 1 new skill\n"
            report += "- Apply to 5 jobs\n"
            report += "- Practice 2 interview questions\n"
            
            return report
        
        update_progress_btn.click(
            update_progress,
            inputs=[completed_skills, completed_projects, completed_certifications, job_applications, interviews_attended],
            outputs=[progress_output]
        )

def create_career_chatbot_tab(career_ai, conversation_history):
    with gr.Column():
        gr.Markdown("""
        <div class="feature-card">
            <h2>💬 AI Career Mentor with Voice Mode</h2>
            <p>Get 24/7 career guidance from AI mentor using text or voice</p>
        </div>
        """)
        
        # Chatbot Interface
        chatbot = gr.Chatbot(
            label=None,
            height=400,
            show_label=False
        )
        
        # Voice Input Section
        gr.Markdown("""
        <div class="voice-mode-container">
            <h4>🎤 Voice Input Mode</h4>
            <p>Click the microphone button to speak your question</p>
        </div>
        """)
        
        # Voice Recording Interface
        with gr.Row():
            audio_input = gr.Audio(
                sources=["microphone"],
                type="numpy",
                label="Record your voice",
                show_label=False
            )
            
            voice_status = gr.Textbox(
                label="Voice Recognition Status",
                value="🔴 Click the microphone icon above to start recording",
                interactive=False,
                show_label=False
            )
        
        # Text Input Interface
        with gr.Row():
            msg = gr.Textbox(
                placeholder="Type your career question here or use voice input above...",
                show_label=False,
                scale=4,
                container=False
            )
            send_btn = gr.Button("Send", variant="primary", scale=1)
        
        clear_btn = gr.Button("Clear Chat", variant="secondary")
        
        # Voice processing function
        def process_voice(audio):
            if audio is None:
                return "", "❌ No audio detected. Please try again."
            
            if career_ai[0] is None:
                return "", "❌ Please configure Gemini API key first"
            
            try:
                # Get audio data
                sample_rate, audio_data = audio
                
                # Convert to bytes
                import io
                import wave
                
                # Create a BytesIO object
                audio_bytes = io.BytesIO()
                
                # Write audio data as WAV file
                with wave.open(audio_bytes, 'wb') as wav_file:
                    wav_file.setnchannels(1)  # Mono
                    wav_file.setsampwidth(2)  # 16-bit
                    wav_file.setframerate(sample_rate)
                    
                    # Convert to bytes
                    if audio_data.dtype == np.float32:
                        audio_data = (audio_data * 32767).astype(np.int16)
                    elif audio_data.dtype == np.float64:
                        audio_data = (audio_data * 32767).astype(np.int16)
                    
                    wav_file.writeframes(audio_data.tobytes())
                
                # Get audio bytes
                audio_bytes.seek(0)
                audio_data_bytes = audio_bytes.read()
                
                # Process voice input
                text, status = career_ai[0].process_voice_input(audio_data_bytes)
                return text, status
                
            except Exception as e:
                return "", f"❌ Error processing voice: {str(e)}"
        
        # Text response function
        def respond(message, chat_history):
            if not message.strip():
                return chat_history, ""
                
            if career_ai[0] is None:
                chat_history.append({"role": "user", "content": message})
                chat_history.append({"role": "assistant", "content": "Please configure Gemini API key first to use the AI mentor."})
                return chat_history, ""
            
            # Update conversation history
            conv_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history[-10:]])
            
            # Get AI response
            try:
                response = career_ai[0].career_chatbot(message, conv_history)
                chat_history.append({"role": "user", "content": message})
                chat_history.append({"role": "assistant", "content": response})
                
                # Update stored conversation history
                if len(conversation_history[0]) > 10000:
                    conversation_history[0] = conversation_history[0][-5000:]
                
            except Exception as e:
                chat_history.append({"role": "user", "content": message})
                chat_history.append({"role": "assistant", "content": f"Error: {str(e)}"})
            
            return chat_history, ""
        
        def clear_chat():
            conversation_history[0] = ""
            return []
        
        # Voice input processing
        def process_voice_and_update(audio, chat_history):
            text, status = process_voice(audio)
            if text:
                # Update the message box with recognized text
                chat_history, _ = respond(text, chat_history)
                return chat_history, text, status
            return chat_history, "", status
        
        # Text input processing
        msg.submit(
            respond,
            inputs=[msg, chatbot],
            outputs=[chatbot, msg]
        )
        
        send_btn.click(
            respond,
            inputs=[msg, chatbot],
            outputs=[chatbot, msg]
        )
        
        # Voice input processing
        audio_input.stop_recording(
            process_voice_and_update,
            inputs=[audio_input, chatbot],
            outputs=[chatbot, msg, voice_status]
        )
        
        clear_btn.click(
            clear_chat,
            None,
            [chatbot]
        )

def create_career_resources_tab():
    with gr.Column():
        gr.Markdown("""
        <div class="feature-card">
            <h2>📚 Complete Career Resources</h2>
            <p>Everything you need for career success in one place</p>
        </div>
        """)
        
        # Free Certification Platforms
        gr.Markdown("""
        <div class="feature-card">
            <h3>🎓 Top Free Certification Platforms</h3>
        </div>
        """)
        
        html = "<div class='role-grid'>"
        for platform_name, platform_data in career_data.certification_platforms.items():
            html += f"""
            <div class="role-card">
                <div class="role-header">
                    <div class="role-icon">📜</div>
                    <div>
                        <h4>{platform_name}</h4>
                        <div style="color: #10b981; font-weight: 600;">{platform_data['free_certificates']}</div>
                    </div>
                </div>
                <p>{platform_data['description']}</p>
                <div style="margin: 15px 0;">
                    <div style="font-size: 12px; margin-bottom: 6px; font-weight: 600;">BEST FOR:</div>
                    <div style="font-size: 14px;">{platform_data['best_for']}</div>
                </div>
                <div style="margin: 10px 0;">
                    <div style="font-size: 12px; margin-bottom: 6px; font-weight: 600;">TOPICS:</div>
                    <div>{" ".join([f"<span class='platform-badge'>{topic}</span>" for topic in platform_data.get('topics', [])[:3]])}</div>
                </div>
                <a href="{platform_data['url']}" target="_blank">
                    <button class="platform-btn" style="background: linear-gradient(135deg, #10b981, #059669);">
                        Visit Platform →
                    </button>
                </a>
            </div>
            """
        html += "</div>"
        gr.HTML(html)

def create_unified_resources_tab():
    with gr.Column():
        gr.Markdown("""
        <div class="feature-card">
            <h2>🌐 Unified Career Ecosystem</h2>
            <p>All career resources in one place - No more switching between websites</p>
        </div>
        """)
        
        # All Resources Summary
        gr.Markdown("""
        <div class="feature-card">
            <h3>📚 All Resource Categories</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 20px;">
                <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1)); padding: 20px; border-radius: 15px;">
                    <h4>💻 Coding Practice</h4>
                    <p>8 platforms for DSA, competitive programming, interview prep</p>
                </div>
                <div style="background: linear-gradient(135deg, rgba(240, 147, 251, 0.1), rgba(245, 87, 108, 0.1)); padding: 20px; border-radius: 15px;">
                    <h4>🏆 Hackathons</h4>
                    <p>5 platforms for competitions, prizes, networking</p>
                </div>
                <div style="background: linear-gradient(135deg, rgba(79, 172, 254, 0.1), rgba(0, 242, 254, 0.1)); padding: 20px; border-radius: 15px;">
                    <h4>📜 Certifications</h4>
                    <p>7 platforms for free certificates & learning paths</p>
                </div>
                <div style="background: linear-gradient(135deg, rgba(246, 211, 101, 0.1), rgba(253, 160, 133, 0.1)); padding: 20px; border-radius: 15px;">
                    <h4>📝 Resume Builders</h4>
                    <p>5 ATS-friendly resume builders</p>
                </div>
                <div style="background: linear-gradient(135deg, rgba(255, 154, 158, 0.1), rgba(250, 208, 196, 0.1)); padding: 20px; border-radius: 15px;">
                    <h4>💼 Job Platforms</h4>
                    <p>10 top job applying platforms with ratings</p>
                </div>
                <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(5, 150, 105, 0.1)); padding: 20px; border-radius: 15px;">
                    <h4>🔍 ATS Evaluators</h4>
                    <p>5 platforms to check resume ATS score</p>
                </div>
                <div style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(124, 58, 237, 0.1)); padding: 20px; border-radius: 15px;">
                    <h4>🏆 Internships</h4>
                    <p>5 free internship platforms for students</p>
                </div>
                <div style="background: linear-gradient(135deg, rgba(236, 72, 153, 0.1), rgba(219, 39, 119, 0.1)); padding: 20px; border-radius: 15px;">
                    <h4>🎬 YouTube Learning</h4>
                    <p>20+ career roles with YouTube learning links</p>
                </div>
            </div>
        </div>
        """)
        
        # Job Platforms Section
        gr.Markdown("""
        <div class="feature-card">
            <h3>💼 Job Platforms</h3>
            <p>Job applying platforms with ratings & features</p>
        </div>
        """)
        
        html = "<div class='role-grid'>"
        for platform in career_data.job_platforms:
            html += f"""
            <div class="role-card">
                <div class="role-header">
                    <div class="role-icon">{platform['logo']}</div>
                    <div>
                        <h4>{platform['name']}</h4>
                        <div style="color: #f59e0b; font-weight: 600;">{platform['rating']}</div>
                    </div>
                </div>
                <p>{platform['description']}</p>
                <div style="margin: 15px 0;">
                    <div style="font-size: 12px; margin-bottom: 6px; font-weight: 600;">FEATURES:</div>
                    <div style="font-size: 14px;">{" • ".join(platform['features'])}</div>
                </div>
                <div style="margin: 10px 0;">
                    <div style="font-size: 12px; margin-bottom: 6px; font-weight: 600;">BEST FOR:</div>
                    <div>{" ".join([f"<span class='platform-badge'>{bf}</span>" for bf in platform['best_for']])}</div>
                </div>
                <a href="{platform['url']}" target="_blank">
                    <button class="platform-btn" style="background: linear-gradient(135deg, #f59e0b, #d97706);">
                        Visit Platform →
                    </button>
                </a>
            </div>
            """
        html += "</div>"
        gr.HTML(html)
        
        # Resume Builders Section
        gr.Markdown("""
        <div class="feature-card">
            <h3>📝 Resume Builders</h3>
            <p>ATS-friendly resume builders</p>
        </div>
        """)
        
        html = "<div class='role-grid'>"
        for builder in career_data.resume_builders:
            html += f"""
            <div class="role-card">
                <div class="role-header">
                    <div class="role-icon">{builder['logo']}</div>
                    <div>
                        <h4>{builder['name']}</h4>
                        <div style="color: #8b5cf6; font-weight: 600;">ATS: {builder['ats_friendly']}</div>
                    </div>
                </div>
                <p>{builder['description']}</p>
                <div style="margin: 15px 0;">
                    <div style="font-size: 12px; margin-bottom: 6px; font-weight: 600;">BEST FOR:</div>
                    <div style="font-size: 14px;">{builder['best_for']}</div>
                </div>
                <div style="margin: 10px 0;">
                    <div style="font-size: 12px; margin-bottom: 6px; font-weight: 600;">FEATURES:</div>
                    <div style="font-size: 14px;">{" • ".join(builder['features'][:2])}</div>
                </div>
                <a href="{builder['url']}" target="_blank">
                    <button class="platform-btn" style="background: linear-gradient(135deg, #8b5cf6, #7c3aed);">
                        Visit Builder →
                    </button>
                </a>
            </div>
            """
        html += "</div>"
        gr.HTML(html)
        
        # ATS Resume Score Evaluators Section
        gr.Markdown("""
        <div class="feature-card">
            <h3>🔍 ATS Resume Score Evaluating Platforms</h3>
            <p>Platforms to check your resume ATS score</p>
        </div>
        """)
        
        html = "<div class='role-grid'>"
        for evaluator in career_data.ats_evaluators:
            html += f"""
            <div class="role-card">
                <div class="role-header">
                    <div class="role-icon">{evaluator['logo']}</div>
                    <div>
                        <h4>{evaluator['name']}</h4>
                        <div style="color: #ec4899; font-weight: 600;">{evaluator['rating']}</div>
                    </div>
                </div>
                <p>{evaluator['description']}</p>
                <div style="margin: 15px 0;">
                    <div style="font-size: 12px; margin-bottom: 6px; font-weight: 600;">FEATURES:</div>
                    <div style="font-size: 14px;">{" • ".join(evaluator['features'])}</div>
                </div>
                <a href="{evaluator['url']}" target="_blank">
                    <button class="platform-btn" style="background: linear-gradient(135deg, #ec4899, #db2777);">
                        Check Score →
                    </button>
                </a>
            </div>
            """
        html += "</div>"
        gr.HTML(html)
        
        # Free Internship Platforms Section
        gr.Markdown("""
        <div class="feature-card">
            <h3>🏆 Free Internship Platforms</h3>
            <p>Free internship platforms for students</p>
        </div>
        """)
        
        html = "<div class='role-grid'>"
        for platform in career_data.internship_platforms:
            html += f"""
            <div class="role-card">
                <div class="role-header">
                    <div class="role-icon">{platform['logo']}</div>
                    <div>
                        <h4>{platform['name']}</h4>
                        <div style="color: #06b6d4; font-weight: 600;">{platform['rating']}</div>
                    </div>
                </div>
                <p>{platform['description']}</p>
                <div style="margin: 15px 0;">
                    <div style="font-size: 12px; margin-bottom: 6px; font-weight: 600;">FEATURES:</div>
                    <div style="font-size: 14px;">{" • ".join(platform['features'])}</div>
                </div>
                <a href="{platform['url']}" target="_blank">
                    <button class="platform-btn" style="background: linear-gradient(135deg, #06b6d4, #0891b2);">
                        Find Internships →
                    </button>
                </a>
            </div>
            """
        html += "</div>"
        gr.HTML(html)
        
        # Coding Platforms
        gr.Markdown("""
        <div class="feature-card">
            <h3>💻 Coding Practice Platforms</h3>
        </div>
        """)
        
        html = "<div class='role-grid'>"
        for platform in career_data.coding_platforms[:4]:
            html += f"""
            <div class="role-card">
                <div class="role-header">
                    <div class="role-icon">{platform['logo']}</div>
                    <div>
                        <h4>{platform['name']}</h4>
                        <div style="color: #10b981; font-weight: 600;">{platform['rating']}</div>
                    </div>
                </div>
                <p>{platform['description']}</p>
                <div style="margin: 15px 0;">
                    <div style="font-size: 12px; margin-bottom: 6px; font-weight: 600;">BEST FOR:</div>
                    <div>{" ".join([f"<span class='skill-badge'>{bf}</span>" for bf in platform['best_for'][:2]])}</div>
                </div>
                <a href="{platform['url']}" target="_blank">
                    <button class="platform-btn" style="background: linear-gradient(135deg, #667eea, #764ba2);">
                        Visit Platform →
                    </button>
                </a>
            </div>
            """
        html += "</div>"
        gr.HTML(html)
        
        # Hackathon Platforms
        gr.Markdown("""
        <div class="feature-card">
            <h3>🏆 Hackathon Platforms</h3>
        </div>
        """)
        
        html = "<div class='role-grid'>"
        for platform in career_data.hackathon_platforms:
            html += f"""
            <div class="role-card">
                <div class="role-header">
                    <div class="role-icon">{platform['logo']}</div>
                    <div>
                        <h4>{platform['name']}</h4>
                        <div style="color: #f59e0b; font-weight: 600;">{platform['rating']}</div>
                    </div>
                </div>
                <p>{platform['description']}</p>
                <div style="margin: 15px 0;">
                    <div style="font-size: 12px; margin-bottom: 6px; font-weight: 600;">PRIZES:</div>
                    <div style="font-size: 14px;">{platform['prizes'][:80]}...</div>
                </div>
                <a href="{platform['url']}" target="_blank">
                    <button class="platform-btn" style="background: linear-gradient(135deg, #f59e0b, #d97706);">
                        Join Hackathons →
                    </button>
                </a>
            </div>
            """
        html += "</div>"
        gr.HTML(html)

# Run the application
if __name__ == "__main__":
    demo = create_interface()

    # Launch the Gradio app
    demo.launch(
        server_name="0.0.0.0",
        server_port=7863,
        share=True,
        debug=True,
        height=1200,
        theme=gr.themes.Soft(),
        css=custom_css
    )
