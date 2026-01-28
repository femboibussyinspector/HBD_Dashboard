from flask import Blueprint, request, jsonify, current_app
from extensions import db
from model.user import User
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from utils.validators import is_valid_email, is_valid_password
from extensions import mail
from flask_mail import Message
import random
from datetime import datetime, timedelta

auth_bp = Blueprint("auth", __name__)


# Signup
@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.json or {}
    email = data.get("email", "").strip()
    password = data.get("password", "")

    # Validate required fields
    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    # Validate email format
    if not is_valid_email(email):
        return jsonify({"message": "Invalid email format"}), 400

    # Validate password strength
    is_valid, error_message = is_valid_password(password)
    if not is_valid:
        return jsonify({"message": error_message}), 400

    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "User already exists"}), 400

    try:
        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        # Auto-login: Generate token after successful signup
        token = create_access_token(identity=str(user.id))
        return jsonify({
            "message": "User created successfully",
            "token": token  # User is now logged in automatically
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while creating user"}), 500


# Login
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json or {}
    email = data.get("email", "").strip()
    password = data.get("password", "")

    # Validate required fields
    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"message": "Invalid credentials"}), 401

    token = create_access_token(identity=str(user.id))
    return jsonify({"token": token}), 200


    return jsonify(message=f"Welcome {current_user}, you have accessed a protected route!"), 200


# Forgot Password - Step 1: Send OTP
@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.json or {}
    email = data.get("email", "").strip()

    if not email:
        return jsonify({"message": "Email is required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Generate 6-digit OTP
    otp = str(random.randint(100000, 999999))
    otp_expiry = datetime.utcnow() + timedelta(minutes=15)

    try:
        # Save OTP to DB
        user.reset_otp = otp
        user.reset_otp_expiry = otp_expiry
        db.session.commit()

        # Send Email
        msg = Message("Password Reset OTP", 
                      sender=current_app.config.get("MAIL_USERNAME"), 
                      recipients=[email])
        msg.body = f"Your Password Reset OTP is: {otp}\n\nThis OTP is valid for 15 minutes."
        mail.send(msg)

        return jsonify({"message": "OTP sent to your email"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to send OTP", "error": str(e)}), 500


# Forgot Password - Step 2: Verify OTP
@auth_bp.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.json or {}
    email = data.get("email", "").strip()
    otp = data.get("otp", "").strip()

    if not email or not otp:
        return jsonify({"message": "Email and OTP are required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Check OTP and Expiry
    if user.reset_otp != otp:
        return jsonify({"message": "Invalid OTP"}), 400
    
    if user.reset_otp_expiry and datetime.utcnow() > user.reset_otp_expiry:
        return jsonify({"message": "OTP has expired"}), 400

    return jsonify({"message": "OTP verified successfully"}), 200


# Forgot Password - Step 3: Reset Password
@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.json or {}
    email = data.get("email", "").strip()
    otp = data.get("otp", "").strip()
    new_password = data.get("new_password", "")

    if not email or not otp or not new_password:
        return jsonify({"message": "Email, OTP and new password are required"}), 400

    # Validate password strength
    is_valid, error_message = is_valid_password(new_password)
    if not is_valid:
        return jsonify({"message": error_message}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Verify OTP again to be safe
    if user.reset_otp != otp or (user.reset_otp_expiry and datetime.utcnow() > user.reset_otp_expiry):
        return jsonify({"message": "Invalid or expired OTP"}), 400

    try:
        # Reset Password
        user.set_password(new_password)
        # Clear OTP
        user.reset_otp = None
        user.reset_otp_expiry = None
        
        db.session.commit()
        return jsonify({"message": "Password reset successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to reset password", "error": str(e)}), 500


# Logout (Basic)
@auth_bp.route("/logout", methods=["POST"])
def logout():
    # Since we are not using blacklisting, the server just returns success.
    # The frontend MUST delete the token from storage (localStorage/cookies).
    return jsonify({"message": "Logged out successfully"}), 200