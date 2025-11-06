# RentCrew

RentCrew is a comprehensive CRM/ERP system designed for AV rental businesses (lighting, sound, staging equipment). It helps operators manage the entire rental lifecycle from planning and pricing to reservations, logistics, and invoicing.

## Features

- Client and project management
- Inventory and asset tracking
- Reservation and availability management
- Quote and invoice generation
- Warehouse operations (picklists, scanning)
- Crew scheduling
- Maintenance and damage tracking

## Technology Stack

### Backend
- Django 5.2
- Django REST Framework
- DRF Spectacular for API documentation

### Frontend
- React 19
- React Router 7
- TypeScript
- Tailwind CSS
- Vite

## Project Structure

- `/RentCrew` - Django project root
- `/web` - React frontend application
- `/templates` - Django templates
- `/prompts` - AI assistant prompts and documentation

## Setup Instructions

### Backend Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```
   python manage.py migrate
   ```

4. Start the development server:
   ```
   python manage.py runserver
   ```

### Frontend Setup

1. Navigate to the web directory:
   ```
   cd web
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm run dev
   ```

## License
