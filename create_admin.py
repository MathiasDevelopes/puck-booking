#!/usr/bin/env python3
"""
Script to create an admin user for the Hockey Booking API.
Run this script to create the first admin user.

Usage:
    python create_admin.py
"""

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, init_db
from app.crud.user import create_user, get_user_by_username
from app.schemas.user import UserCreate
import getpass


def main():
    print("Hockey Booking API - Admin User Creation")
    print("=" * 50)
    
    # Initialize database
    init_db()
    db = SessionLocal()
    
    try:
        # Get admin details
        email = input("Enter admin email: ").strip()
        username = input("Enter admin username: ").strip()
        
        # Check if username already exists
        existing_user = get_user_by_username(db, username)
        if existing_user:
            print(f"\nError: User '{username}' already exists!")
            
            # Offer to make them admin if they aren't
            if not existing_user.is_admin:
                make_admin = input("Would you like to make this user an admin? (yes/no): ").strip().lower()
                if make_admin in ['yes', 'y']:
                    existing_user.is_admin = True
                    db.commit()
                    print(f"\n✓ User '{username}' is now an admin!")
                else:
                    print("\nOperation cancelled.")
            else:
                print(f"\nUser '{username}' is already an admin.")
            return
        
        password = getpass.getpass("Enter admin password: ")
        password_confirm = getpass.getpass("Confirm admin password: ")
        
        if password != password_confirm:
            print("\nError: Passwords do not match!")
            return
        
        if len(password) < 6:
            print("\nError: Password must be at least 6 characters long!")
            return
        
        # Create admin user
        admin = UserCreate(
            email=email,
            username=username,
            password=password
        )
        
        db_admin = create_user(db, admin)
        db_admin.is_admin = True
        db.commit()
        
        print("\n" + "=" * 50)
        print("✓ Admin user created successfully!")
        print("=" * 50)
        print(f"Username: {username}")
        print(f"Email: {email}")
        print(f"Admin: Yes")
        print("\nYou can now login with these credentials.")
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\n\nError: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
