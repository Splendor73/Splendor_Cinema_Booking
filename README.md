

Here's the complete README.md with all the information:

markdown
# Splendor Cinema Booking

A modern movie ticket booking system built with Flask and PostgreSQL. This application provides a seamless experience for booking movie tickets with an elegant dark-themed UI and real-time seat selection.

## Live Demo

### Welcome Page
<img width="500" alt="Welcome Page" src="https://github.com/user-attachments/assets/dfbe8494-8b06-4a75-8c6b-246304c6dc68">

### Movies Selection
<img width="600" alt="Movies Page" src="https://github.com/user-attachments/assets/2a2582bd-d140-4a79-80f2-ef2e23f4e1f9">

### Seat Layout
<img width="600" alt="Seat Selection" src="https://github.com/user-attachments/assets/71711220-431f-4879-9f22-1a6b81daccc8">

### Booking Details Form
<img width="500" alt="Booking Details" src="https://github.com/user-attachments/assets/1a4f0fff-6718-4cae-b2be-88386e3022c7">

### Payment Selection
<img width="500" alt="Payment Options" src="https://github.com/user-attachments/assets/19b1c9ea-81f3-4ecd-a4e6-286298b8fc19">

### Booking Processing
<img width="500" alt="Processing" src="https://github.com/user-attachments/assets/d9f67ba3-6523-4d74-aead-d4130e6e7ff3">

### Confirmation Screen
<img width="400" alt="Confirmation" src="https://github.com/user-attachments/assets/c9a800a7-f65d-43e6-9073-1152407f3224">

### Email Notification
<img width="500" alt="Email" src="https://github.com/user-attachments/assets/df1b615c-29a5-4325-95bb-a8653e6c9754">

### Booking Complete
<img width="400" alt="Complete" src="https://github.com/user-attachments/assets/29c166b0-519d-44de-96f7-bb901b2f5c17">
## Live Demo



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



```markdown
## Database Seeding

### Adding Sample Movies and Seats
You can add sample data to your database using pgAdmin's Query Tool or psql. Here's how:

1. Connect to your database
2. Run the following SQL commands:

```sql
-- Add new movies
INSERT INTO movies (title, show_time) 
VALUES 
    ('The Matrix', '2024-03-25 18:00:00'),
    ('Pulp Fiction', '2024-03-25 21:00:00'),
    ('The Shawshank Redemption', '2024-03-26 19:00:00');

-- Add seats for each movie
INSERT INTO seats (movie_id, seat_number, is_booked)
SELECT 
    m.id,
    s.seat_number,
    FALSE
FROM movies m
CROSS JOIN (
    SELECT 
    CASE 
        WHEN num <= 5 THEN 'A' || num
        WHEN num <= 10 THEN 'B' || (num - 5)
        WHEN num <= 15 THEN 'C' || (num - 10)
        ELSE 'D' || (num - 15)
    END as seat_number
    FROM generate_series(1, 20) num
) s
WHERE m.title IN ('The Matrix', 'Pulp Fiction', 'The Shawshank Redemption');
```

### Adding Your Own Movies

To add your own movies, use this template:
```sql
INSERT INTO movies (title, show_time) 
VALUES 
    ('Movie Title 1', 'YYYY-MM-DD HH:MI:SS'),
    ('Movie Title 2', 'YYYY-MM-DD HH:MI:SS');

-- Then add seats for your new movies
INSERT INTO seats (movie_id, seat_number, is_booked)
SELECT 
    m.id,
    s.seat_number,
    FALSE
FROM movies m
CROSS JOIN (
    SELECT 
    CASE 
        WHEN num <= 5 THEN 'A' || num
        WHEN num <= 10 THEN 'B' || (num - 5)
        WHEN num <= 15 THEN 'C' || (num - 10)
        ELSE 'D' || (num - 15)
    END as seat_number
    FROM generate_series(1, 20) num
) s
WHERE m.title IN ('Movie Title 1', 'Movie Title 2');
```

### Viewing Current Data

To view all movies:
```sql
SELECT * FROM movies ORDER BY show_time;
```

To view available seats for a specific movie:
```sql
SELECT s.seat_number, s.is_booked
FROM seats s
JOIN movies m ON s.movie_id = m.id
WHERE m.title = 'Your Movie Title'
ORDER BY s.seat_number;
```

To view all bookings:
```sql
SELECT 
    b.id as booking_id,
    m.title as movie,
    b.user_name,
    b.email,
    array_agg(s.seat_number) as booked_seats
FROM bookings b
JOIN movies m ON b.movie_id = m.id
JOIN booked_seats bs ON b.id = bs.booking_id
JOIN seats s ON bs.seat_id = s.id
GROUP BY b.id, m.title, b.user_name, b.email
ORDER BY b.id;
```

### Notes
- Make sure to update the show_time values to future dates
- The seat generation creates 20 seats (A1-A5, B1-B5, C1-C5, D1-D5) for each movie
- All seats are initially set as not booked (is_booked = FALSE)
- Movie titles must be unique for the seat insertion query to work correctly
```


