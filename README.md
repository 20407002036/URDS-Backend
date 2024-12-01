# URDS-Backend

This repository contains the backend code for the URDS project, specifically the Flask application.

## Project Structure

- `URDS-flask/`: Contains the Flask application.
    - `app.py`: Main application file for the Flask project.
    - `db_actions.py`: Database actions for the Flask project.

## Flask Application

The Flask application handles sensor data and sends notifications via SMS and email. It uses MySQL for database storage and includes routes for adding sensor data.

### Key Files

- `app.py`: Main application file that sets up routes and configurations.
- `db_actions.py`: Contains database actions for saving sensor data.

## Environment Variables

The Flask application uses environment variables for configuration. Ensure you have a `.env` file with the following variables:

- `OZEKI_SMS_URL`
- `OZEKi_USERNAME`
- `OZEKI_PASSWORD`
- `SMTP_SERVER`
- `SMTP_PORT`
- `SMTP_USER`
- `SMTP_PASSWORD`

## Running the Application

To run the Flask application:

```bash
cd URDS-flask
python app.py
```

## License

This project is licensed under the MIT License.
