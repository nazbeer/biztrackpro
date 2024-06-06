# BizTrackPro

## Overview

**BizTrackPro** is designed to manage various aspects of a business, including shops, users, business profiles, employees, business timings, transactions, and financial records. It provides a comprehensive solution for business operations, facilitating efficient management and organization.

## Features

- Shop management
- User and admin roles
- Business profile management
- Employee records
- Financial transaction tracking
- Reminders for license expiration, VAT submissions, and employee document renewals

## Installation

### Prerequisites

- Python 3.6+
- Django 3.0+
- PostgreSQL (or any preferred database)

### Steps

1. **Clone the repository:**

   ```bash
   git clone https://bitbucket.org/mite-team/web-biztrack-pro-mitesolutions/
   cd biztrackpro
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the database:**

   Update the `DATABASES` setting in `settings.py` with your database credentials.

5. **Apply migrations:**

   ```bash
   python manage.py migrate
   ```

6. **Create a superuser:**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

8. **Access the application:**

   Open your browser and go to `http://127.0.0.1:8000/admin` to access the admin interface.

## Project Structure

- `models.py`: Contains the database models for shops, users, business profiles, employees, and financial transactions.
- `views.py`: Contains views for rendering templates and handling business logic.
- `urls.py`: URL configurations for routing requests to appropriate views.
- `templates/`: HTML templates for the application.
- `static/`: Static files (CSS, JavaScript, images).

## Key Models

- **Shop**: Represents a shop with various attributes and reminders.
- **User**: Custom user model with additional fields.
- **BusinessProfile**: Contains business-specific details and reminders.
- **Employee**: Represents an employee within a business.
- **DailySummary**: Tracks daily financial summaries.
- **TransactionMode**: Different modes of transactions (e.g., cash, card, bank transfer).

For more detailed information, refer to the source code and inline documentation.

## License

This project is licensed under the MIT License.

---

For any further inquiries or support, please contact Nasbeer Ahammed at Mite Solutions Pvt Ltd.