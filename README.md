## Overview

This project is an onboarding platform for a financial services company.
It allows admins to create different onboarding forms such as KYC, loan, or investment forms.
Clients can fill these forms, upload documents, and once submitted, admins are notified automatically.

## Admin Setup

Admins can create new forms and add different types of fields such as:

Text
Number
Date
Dropdown
Checkbox
File upload

 ## Client Submission

Clients can see all available forms and fill them easily.
They can upload multiple documents where required.
After submitting, a success message is shown.

<img width="1366" height="768" alt="Screenshot from 2025-10-04 20-40-39" src="https://github.com/user-attachments/assets/553df94a-ea49-4a4d-b959-0fa0cb53a8ee" />


## Notifications
When a client submits a form, the system sends an admin notification asynchronously using Celery.
Celery + Redis are used for background notifications so the app stays responsive.

## Workflow

Admin creates a form → defines fields (e.g., Name, Email, ID Number, etc.)
Client selects the form → fills it → uploads documents → submits.
Backend saves the data → triggers Celery task → Admin receives a notification.

### How to run
```bash
git clone https://github.com/AmakoveBridgit/Onboardind-KYC-FORM-Backend

cd Onboarding-KYC-Form-Backend
```



## Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

 ## Install dependencies:
 ```bash
pip install -r requirements.txt
```

### Run migrations and start the server:
```bash
python manage.py migrate
python manage.py runserver
```

### Start Celery (in another terminal):
```bash
celery -A config worker -l info
```

## Run the tests using:
```bash
pytest
```
### why i chose certain approaches
 ### JSON-based Field Configuration
Using JSON allows admins to define any number of forms or fields without changing the backend code.
Add new forms or fields anytime.
This makes the system future-proof — even if the business introduces new types of forms (e.g., KYC, Loan, Investment), 
the system can handle them with minimal modification.
The frontend dynamically reads this JSON and renders input fields accordingly — no hardcoding required.

### using celery
Using Celery allows notifications to happen in the background so users don’t wait for the system to process them.




[cinnamon-2025-10-06T143601+0300.webm](https://github.com/user-attachments/assets/a9775d0c-7abb-4d3b-a40d-4a4fa00b0ecb)

[cinnamon-2025-10-06T142801+0300.webm](https://github.com/user-attachments/assets/3ad05c34-98a1-40c5-9f50-73bb92406b53)









