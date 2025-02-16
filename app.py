from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import psycopg2
from psycopg2 import Error
import os

from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'splendor123'

# Database connection configuration
DB_CONFIG = {
    'dbname': '******',
    'user': '*******',
    'password': '*******',
    'host': 'localhost',
    'port': '5432'
}

# Mail configurations
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USE_TLS = False,
    MAIL_USERNAME = '*********@gmail.com',
    MAIL_PASSWORD = '***********'
)

# Initialize Flask-Mail
mail = Mail(app)

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# Initialize database tables
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Create tables
    cur.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            show_time TIMESTAMP NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS seats (
            id SERIAL PRIMARY KEY,
            movie_id INT REFERENCES movies(id) ON DELETE CASCADE,
            seat_number VARCHAR(5) NOT NULL,
            is_booked BOOLEAN DEFAULT FALSE
        );
        
        CREATE TABLE IF NOT EXISTS bookings (
            id SERIAL PRIMARY KEY,
            movie_id INT REFERENCES movies(id) ON DELETE CASCADE,
            user_name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            phone VARCHAR(20) NOT NULL,
            payment_mode VARCHAR(50) NOT NULL,
            booking_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS booked_seats (
            booking_id INT REFERENCES bookings(id) ON DELETE CASCADE,
            seat_id INT REFERENCES seats(id) ON DELETE CASCADE,
            PRIMARY KEY (booking_id, seat_id)
        );
    ''')
    
    conn.commit()
    cur.close()
    conn.close()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/movies')
def movies():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Get movies and count available seats
    cur.execute('''
        SELECT m.id, m.title, m.show_time,
               (SELECT COUNT(*) FROM seats s 
                WHERE s.movie_id = m.id AND NOT s.is_booked) as available_seats
        FROM movies m;
    ''')
    movies_data = cur.fetchall()
    
    # Convert to list of dictionaries for easier template access
    movies = []
    for movie in movies_data:
        movies.append({
            'id': movie[0],
            'title': movie[1],
            'show_time': movie[2],
            'available_seats': movie[3]
        })
    
    cur.close()
    conn.close()
    return render_template('movies.html', movies=movies)

@app.route('/seats/<int:movie_id>')
def seats(movie_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Get movie information
    cur.execute('SELECT id, title, show_time FROM movies WHERE id = %s;', (movie_id,))
    movie_data = cur.fetchone()
    
    # Debug print
    print(f"Movie data: {movie_data}")
    
    movie = {
        'id': movie_data[0],
        'title': movie_data[1],
        'show_time': movie_data[2]
    }
    
    # Get seats information with better ordering
    cur.execute('''
        SELECT id, seat_number, is_booked 
        FROM seats 
        WHERE movie_id = %s 
        ORDER BY 
            SUBSTRING(seat_number, 1, 1),
            CAST(SUBSTRING(seat_number, 2) AS INTEGER);
    ''', (movie_id,))
    
    seats_data = cur.fetchall()
    
    # Debug print
    print(f"Seats data: {seats_data}")
    
    seats = []
    for seat in seats_data:
        seats.append({
            'id': seat[0],
            'seat_number': seat[1],
            'is_booked': seat[2]
        })
    
    cur.close()
    conn.close()
    
    # Debug print
    print(f"Processed seats: {seats}")
    
    return render_template('seats.html', movie=movie, seats=seats)

def send_booking_confirmation(booking_details):
    """Send booking confirmation email using Flask-Mail"""
    try:
        msg = Message(
            'Movie Tickets Confirmed - Splendor Cinema',
            sender='patel.yashu.1129@gmail.com',
            recipients=[booking_details['email']]
        )
        
        msg.html = f"""
        <div style="font-family: 'Poppins', sans-serif; max-width: 600px; margin: 0 auto; padding: 30px; background: #ffffff; color: #333333; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
            
            <!-- Header Section -->
            <div style="text-align: center; margin-bottom: 30px; background: linear-gradient(135deg, #e50914, #b20710); padding: 20px; border-radius: 10px; color: white;">
                <h1 style="font-size: 28px; margin: 0; text-transform: uppercase; letter-spacing: 2px;">
                    🎬 Tickets Confirmed!
                </h1>
                <p style="font-size: 14px; margin-top: 5px; opacity: 0.9;">
                    Your movie experience awaits
                </p>
            </div>
            
            <!-- Main Content Box -->
            <div style="background: #f8f9fa; padding: 25px; border-radius: 10px; border: 1px solid #e9ecef;">
                
                <!-- Booking Details -->
                <div style="margin-bottom: 25px;">
                    <h2 style="color: #e50914; font-size: 20px; margin-bottom: 20px; text-align: center; border-bottom: 2px solid #e50914; padding-bottom: 10px;">
                        Booking Details
                    </h2>
                    
                    <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                        <p style="margin: 10px 0; font-size: 15px;">
                            <strong style="color: #e50914; display: inline-block; width: 120px;">Booking ID:</strong>
                            <span style="color: #333333;">#{booking_details['id']}</span>
                        </p>
                        <p style="margin: 10px 0; font-size: 15px;">
                            <strong style="color: #e50914; display: inline-block; width: 120px;">Movie:</strong>
                            <span style="color: #333333;">{booking_details['movie']}</span>
                        </p>
                        <p style="margin: 10px 0; font-size: 15px;">
                            <strong style="color: #e50914; display: inline-block; width: 120px;">Show Time:</strong>
                            <span style="color: #333333;">{booking_details['show_time'].strftime('%B %d, %Y %I:%M %p')}</span>
                        </p>
                        <p style="margin: 10px 0; font-size: 15px;">
                            <strong style="color: #e50914; display: inline-block; width: 120px;">Seats:</strong>
                            <span style="color: #333333;">{', '.join(booking_details['seats'])}</span>
                        </p>
                    </div>
                </div>
                
                <!-- Customer Details -->
                <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                    <p style="margin: 10px 0; font-size: 15px;">
                        <strong style="color: #e50914; display: inline-block; width: 120px;">Name:</strong>
                        <span style="color: #333333;">{booking_details['user_name']}</span>
                    </p>
                    <p style="margin: 10px 0; font-size: 15px;">
                        <strong style="color: #e50914; display: inline-block; width: 120px;">Email:</strong>
                        <span style="color: #333333;">{booking_details['email']}</span>
                    </p>
                    <p style="margin: 10px 0; font-size: 15px;">
                        <strong style="color: #e50914; display: inline-block; width: 120px;">Phone:</strong>
                        <span style="color: #333333;">{booking_details['phone']}</span>
                    </p>
                    <p style="margin: 10px 0; font-size: 15px;">
                        <strong style="color: #e50914; display: inline-block; width: 120px;">Payment:</strong>
                        <span style="color: #333333;">{booking_details['payment_mode']}</span>
                    </p>
                </div>
            </div>
            
            <!-- Important Information -->
            <div style="margin-top: 25px; text-align: center; background: #fff4f4; padding: 20px; border-radius: 10px; border: 1px solid #ffe0e0;">
                <h3 style="color: #e50914; margin-bottom: 15px; font-size: 18px;">
                    Important Information
                </h3>
                <p style="color: #333333; margin: 8px 0; font-size: 14px;">
                    ⏰ Please arrive 15 minutes before showtime
                </p>
                <p style="color: #333333; margin: 8px 0; font-size: 14px;">
                    🎟️ Show this email at the counter to collect your tickets
                </p>
            </div>
            
            <!-- Footer -->
            <div style="text-align: center; margin-top: 25px; padding-top: 20px; border-top: 1px solid #e9ecef;">
                <p style="color: #e50914; font-weight: bold; margin-bottom: 5px;">
                    Thank you for choosing Splendor Cinemas!
                </p>
                <p style="color: #666666; font-size: 12px;">
                    For any queries, please contact our support team
                </p>
            </div>
        </div>
        """
        
        # Send the email
        mail.send(msg)
        print(f"Confirmation email sent to {booking_details['email']}")
        
        # Also send a copy to admin
        admin_msg = Message(
            f'Booking Copy - {booking_details["movie"]}',
            sender='patel.yashu.1129@gmail.com',
            recipients=['patel.yashu.1129@gmail.com']
        )
        admin_msg.html = msg.html
        mail.send(admin_msg)
        print("Admin copy sent")
        
        return True
        
    except Exception as e:
        print(f"Error sending confirmation email: {str(e)}")
        return False

@app.route('/details/<int:movie_id>', methods=['GET', 'POST'])
def details(movie_id):
    if request.method == 'GET':
        try:
            # Get selected seat numbers from query parameters
            selected_seat_numbers = request.args.getlist('selected_seats')
            
            if not selected_seat_numbers:
                flash('Please select at least one seat', 'error')
                return redirect(url_for('seats', movie_id=movie_id))
            
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Get movie information
            cur.execute('SELECT title, show_time FROM movies WHERE id = %s;', (movie_id,))
            movie = cur.fetchone()
            
            return render_template('details.html', 
                                 movie_id=movie_id,
                                 movie=movie,
                                 selected_seats=selected_seat_numbers)
                                 
        except Exception as e:
            print(f"Error in details GET: {str(e)}")
            flash('An error occurred. Please try again.', 'error')
            return redirect(url_for('seats', movie_id=movie_id))
            
        finally:
            if 'cur' in locals():
                cur.close()
            if 'conn' in locals():
                conn.close()
    
    elif request.method == 'POST':
        conn = None
        cur = None
        try:
            # Get form data
            user_name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            payment_mode = request.form['payment_mode']
            selected_seats = request.form.getlist('selected_seats')
            
            if not selected_seats:
                flash('Please select at least one seat.', 'error')
                return redirect(url_for('seats', movie_id=movie_id))
            
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Start transaction
            cur.execute('BEGIN')
            
            # Get movie information
            cur.execute('SELECT title, show_time FROM movies WHERE id = %s;', (movie_id,))
            movie = cur.fetchone()
            
            # Get seat IDs for the selected seat numbers
            placeholders = ','.join(['%s'] * len(selected_seats))
            cur.execute(f'''
                SELECT id, seat_number 
                FROM seats 
                WHERE movie_id = %s 
                AND seat_number IN ({placeholders})
                AND NOT is_booked
            ''', (movie_id, *selected_seats))
            
            seats_data = cur.fetchall()
            
            if len(seats_data) != len(selected_seats):
                cur.execute('ROLLBACK')
                flash('Some selected seats are no longer available', 'error')
                return redirect(url_for('seats', movie_id=movie_id))
            
            # Create booking
            cur.execute('''
                INSERT INTO bookings (movie_id, user_name, email, phone, payment_mode)
                VALUES (%s, %s, %s, %s, %s) RETURNING id;
            ''', (movie_id, user_name, email, phone, payment_mode))
            
            booking_id = cur.fetchone()[0]
            
            # Update seats and create booking-seat relationships
            for seat_data in seats_data:
                seat_id = seat_data[0]
                cur.execute('''
                    UPDATE seats 
                    SET is_booked = TRUE 
                    WHERE id = %s AND is_booked = FALSE
                ''', (seat_id,))
                
                cur.execute('''
                    INSERT INTO booked_seats (booking_id, seat_id) 
                    VALUES (%s, %s)
                ''', (booking_id, seat_id))
            
            # Prepare booking details for email
            booking_details = {
                'id': booking_id,
                'movie': movie[0],
                'show_time': movie[1],
                'seats': [seat[1] for seat in seats_data],
                'user_name': user_name,
                'email': email,
                'phone': phone,
                'payment_mode': payment_mode
            }

            # Send confirmation email
            email_sent = send_booking_confirmation(booking_details)
            
            if not email_sent:
                flash('Booking confirmed but email notification failed. Please save your booking ID.', 'warning')
            
            # Commit transaction
            cur.execute('COMMIT')
            
            return redirect(url_for('confirmation', booking_id=booking_id))
            
        except Exception as e:
            if conn and cur:
                cur.execute('ROLLBACK')
            print(f"Error during booking: {str(e)}")
            flash('An error occurred while processing your booking. Please try again.', 'error')
            return redirect(url_for('seats', movie_id=movie_id))
            
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

@app.route('/confirmation/<int:booking_id>')
def confirmation(booking_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get booking details with movie information and seat numbers
        cur.execute('''
            SELECT 
                b.id,
                m.title,
                m.show_time,
                b.user_name,
                b.email,
                b.phone,
                b.payment_mode,
                array_agg(s.seat_number ORDER BY s.seat_number) as booked_seats
            FROM bookings b
            JOIN movies m ON b.movie_id = m.id
            JOIN booked_seats bs ON b.id = bs.booking_id
            JOIN seats s ON bs.seat_id = s.id
            WHERE b.id = %s
            GROUP BY b.id, m.title, m.show_time, b.user_name, b.email, b.phone, b.payment_mode
        ''', (booking_id,))
        
        booking = cur.fetchone()
        
        if booking:
            booking_details = {
                'id': booking[0],
                'movie': booking[1],
                'show_time': booking[2],
                'user_name': booking[3],
                'email': booking[4],
                'phone': booking[5],
                'payment_mode': booking[6],
                'seats': booking[7]
            }
            return render_template('confirmation.html', booking=booking_details)
        else:
            flash('Booking not found', 'error')
            return redirect(url_for('index'))
            
    except Exception as e:
        print(f"Error in confirmation: {str(e)}")
        flash('Error retrieving booking details', 'error')
        return redirect(url_for('index'))
        
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True) 
