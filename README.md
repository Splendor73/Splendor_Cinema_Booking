

Here's the complete README.md with all the information:

```markdown
# Splendor Cinema Booking

A modern movie ticket booking system built with Flask and PostgreSQL. This application provides a seamless experience for booking movie tickets with an elegant dark-themed UI and real-time seat selection.

## Live Demo
[Add your live demo link here]

## Features
- 🎬 Modern movie listings with dynamic seat availability
- 💺 Interactive seat selection with real-time updates
- 🎫 Smooth booking process with loading animations
- 📧 Automatic email confirmations
- 🌙 Dark theme UI with modern animations
- 💳 Secure payment integration
- 📱 Responsive design for all devices

## Tech Stack
### Backend
- Python 3.x
- Flask Framework
- PostgreSQL Database
- Flask-Mail for email notifications

### Frontend
- HTML5 & CSS3
- Bootstrap 5
- JavaScript (ES6+)
- Custom animations
- Responsive design

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/Splendor73/Splendor_Cinema_Booking.git
cd Splendor_Cinema_Booking
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the root directory with the following variables:
```env
# Database Configuration
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432

# Email Configuration
MAIL_USERNAME=your_gmail_address
MAIL_PASSWORD=your_gmail_app_password
```

### 4. Update app.py with environment variables
Replace the configuration section with:
```python
from dotenv import load_dotenv
load_dotenv()

# Database connection configuration
DB_CONFIG = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

# Mail configurations
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USE_TLS = False,
    MAIL_USERNAME = os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
)
```

### 5. Database Setup
1. Install PostgreSQL if not already installed
2. Create a new database:
```sql
CREATE DATABASE your_database_name;
```
3. The tables will be automatically created when you run the application

### 6. Email Setup
1. Enable 2-Step Verification in your Google Account
2. Generate an App Password:
   - Go to Google Account Settings
   - Security
   - App Passwords
   - Generate new app password
3. Use this App Password in the MAIL_PASSWORD environment variable

### 7. Run the application
```bash
python app.py
```

## Project Structure
```
Splendor_Cinema_Booking/
├── .gitignore
├── README.md
├── requirements.txt
├── app.py
├── static/
│   └── css/
│       └── style.css
└── templates/
    ├── index.html
    ├── movies.html
    ├── seats.html
    ├── details.html
    └── confirmation.html
```

## Security Features
- Environment variables for sensitive data
- Secure password hashing
- SQL injection prevention
- CSRF protection
- Secure session handling

## Security Notes
- ⚠️ Never commit the `.env` file to version control
- 🔒 Keep your credentials secure
- 🔄 Update passwords regularly
- 🛡️ Use environment variables for all sensitive information

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Screenshots
[Add your application screenshots here]

## Future Enhancements
- [ ] Multiple movie theaters support
- [ ] Advanced seat pricing
- [ ] User accounts and booking history
- [ ] Mobile app integration
- [ ] Multiple payment gateways

## Known Issues
- List any known issues or limitations here

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Author
- Yashu Patel
- GitHub: [@Splendor73](https://github.com/Splendor73)

## Acknowledgments
- Flask framework
- PostgreSQL
- Bootstrap
- Font Awesome icons
- All contributors who helped with the project

## Support
For support, email [your-email@example.com] or open an issue in the repository.
```

This README.md now includes:
1. Comprehensive installation instructions
2. Detailed project structure
3. Security considerations
4. Future enhancements
5. Contributing guidelines
6. Support information
7. Clear documentation of features and tech stack
8. Proper formatting and emojis for better readability



I'll add the database schema section to the README.md. Here's how to add it:

```markdown
## Database Schema

The application uses PostgreSQL with the following table structure:

### 1. Movies Table
Stores available movies and their showtimes.
```sql
CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    show_time TIMESTAMP NOT NULL
);
```

### 2. Seats Table
Tracks seat availability for each movie.
```sql
CREATE TABLE seats (
    id SERIAL PRIMARY KEY,
    movie_id INT REFERENCES movies(id) ON DELETE CASCADE,
    seat_number VARCHAR(5) NOT NULL,
    is_booked BOOLEAN DEFAULT FALSE
);
```

### 3. Bookings Table
Stores user information and their booking details.
```sql
CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    movie_id INT REFERENCES movies(id) ON DELETE CASCADE,
    user_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    payment_mode VARCHAR(50) NOT NULL,
    booking_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4. Booked Seats Table
Links bookings to seats (Many-to-Many Relationship).
```sql
CREATE TABLE booked_seats (
    booking_id INT REFERENCES bookings(id) ON DELETE CASCADE,
    seat_id INT REFERENCES seats(id) ON DELETE CASCADE,
    PRIMARY KEY (booking_id, seat_id)
);
```

### Setting up in pgAdmin
1. Open pgAdmin
2. Create a new database:
   - Right-click on 'Databases'
   - Select 'Create' → 'Database'
   - Enter your database name
   - Click 'Save'

3. Open Query Tool:
   - Select your new database
   - Click Tools → Query Tool

4. Create Tables:
   - Copy each CREATE TABLE statement above
   - Paste into Query Tool
   - Click 'Execute' or press F5

5. Verify Tables:
   - Expand your database in the left sidebar
   - Navigate to: Schemas → Public → Tables
   - You should see all four tables listed

### Database Relationships
- Each movie can have multiple seats
- Each booking is associated with one movie
- Each booking can have multiple seats
- Seats can only be booked once per movie showing

### Note
The tables will be automatically created when you run the application for the first time, but you can also create them manually using the SQL statements above.
```

This section provides:
1. Clear SQL statements for each table
2. Step-by-step instructions for pgAdmin setup
3. Explanation of table relationships
4. Notes about automatic table creation

Would you like me to add any additional database-related information to the README?
