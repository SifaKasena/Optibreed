# Optibreed IoT Application

Optibreed is an IoT application designed to monitor environmental parameters such as light, humidity, and temperature using various sensors. The application is built using Django, providing a robust and scalable framework for web development.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Sensor Integration**: Supports light, humidity, and temperature sensors.
- **Real-time Monitoring**: Provides real-time updates of sensor data.
- **Data Visualization**: Graphical representation of sensor data for easy monitoring.
- **Alerts**: Configurable alerts for threshold breaches.
- **User Management**: Supports multiple users with different roles and permissions.

## Installation

### Prerequisites

- Python 3.8 or higher
- Django 3.2 or higher
- MySQL or PostgreSQL database
- Virtualenv (optional but recommended)

### Clone the Repository

```bash
git clone https://github.com/MoseNjau/Optibreed-App.git
cd attachement
```

### Create and Activate Virtual Environment
**On Linux/MacOS**
```
python3 -m venv env
source env/bin/activate
```
**On Windows**
```
python -m venv env
.\env\Scripts\activate
```

### Install Dependencies
```
pip install -r requirements.txt
```

### Database Setup
**Ensure your database server is running and create a database for the application.**

```
CREATE DATABASE optibreed_db;
```

### Configure Environment Variables
**Create a ```.env``` file in the project root and add the following configurations:**

```
DATABASE_NAME=optibreed_db
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=localhost
DATABASE_PORT=3306  # or 5432 for PostgreSQL
SECRET_KEY=your_django_secret_key
DEBUG=True  # Set to False in production
```

### Apply Migrations
```
python manage.py migrate
```
### Create Superuser
```
python manage.py createsuperuser
```
### Navigate to the attachment Directory
```
cd attachment
```
### Run the Development Server
```
python manage.py runserver
```


## Configuration
**Sensor Configuration**
Ensure your sensors are properly connected and configured to send data to the Django application. The application expects sensor data in a specific format. Refer to the API Endpoints section for more details.

### Settings
Modify the settings.py file to configure various aspects of the application, such as allowed hosts, installed apps, middleware, etc.

## Usage

### Accessing the Application
- Open your web browser and go to http://127.0.0.1:8000/ to access the application.

### Admin Panel
- Access the admin panel at http://127.0.0.1:8000/admin/ using the superuser credentials you created earlier.

## API Endpoints
### Sensor Data Submission
`Endpoint: POST /api/sensor-data/`

```
{
  "sensor_type": "temperature",
  "value": 22.5,
  "timestamp": "2023-06-14T12:34:56Z"
}
```

### Retrieve Sensor Data
`Endpoint: GET /api/sensor-data/`

### Optional Query Parameters:

- `sensor_type:` Filter by sensor type (e.g., temperature, humidity, light)
- `start_date:` Filter data starting from this date
- `end_date:` Filter data up to this date

## Contributing
**We welcome contributions to the Optibreed IoT application! To contribute, follow these steps:**

- Fork the repository.
- Create a new branch (`git checkout -b feature-branch`).
- Make your changes.
- Commit your changes (git commit -m 'Add some feature').
- Push to the branch (git push origin feature-branch).
- Open a Pull Request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.