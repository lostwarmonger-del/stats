# database.py - Database configuration and models
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# Database setup with concurrent support
DATABASE_URL = "sqlite:///./users.db"

# Configure SQLite for concurrent operations
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
        "timeout": 30,  # Wait up to 30 seconds for locks
        "isolation_level": None  # Autocommit mode for better concurrency
    },
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False  # Set to True for SQL debugging
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# User model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="user", nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relationships to program data tables
    program_404640723_data = relationship("Program404640723Data", back_populates="user")
    program_404640758_data = relationship("Program404640758Data", back_populates="user")
    program_403640724_data = relationship("Program403640724Data", back_populates="user")

# Notification model
class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    message = Column(String(1000), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, nullable=False)  # User ID who created the notification

# Program 404640723 Data Model - Security Intelligence Form
class Program404640723Data(Base):
    __tablename__ = "program_404640723_data"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Form fields based on Excel schema - all as strings for Shamsi dates
    row_number = Column(String(10))  # ردیف
    page_channel_address = Column(String(500))  # آدرس پیج یا کانال
    news_subject = Column(String(200))  # موضوع خبر
    naba_code = Column(String(50))  # کد نبا
    naba_code_review = Column(String(100))  # بررسی کد نباء
    naba_code_registration_date = Column(String(20))  # تاریخ ثبت کد نباء (Shamsi)
    suspicion_classification = Column(String(100))  # کلاسه مظنونیت
    suspicion_registration_date = Column(String(20))  # تاریخ ثبت کلاسه مظنونیت (Shamsi)
    action_results = Column(Text)  # نتیجه اقدامات
    identified_military_count = Column(String(10))  # تعداد نظامی شناسایی شده
    identified_military_dependents_count = Column(String(10))  # تعداد وابستگان نظامی شناسایی شده
    honorary_police = Column(String(100))  # پلیس افتخاری
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="program_404640723_data")

# Program 404640758 Data Model - Personal Information Form
class Program404640758Data(Base):
    __tablename__ = "program_404640758_data"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Personal Information
    first_name = Column(String(100))  # نام
    last_name = Column(String(100))  # نام خانوادگی
    father_name = Column(String(100))  # نام پدر
    id_number = Column(String(20))  # شماره شناسنامه
    birth_date = Column(String(20))  # تاریخ تولد (Shamsi)
    national_id = Column(String(20))  # کد ملی
    
    # ID Card Information
    id_issue_date = Column(String(20))  # تاریخ صدور شناسنامه (Shamsi)
    id_issue_place = Column(String(100))  # محل صدور شناسنامه
    religion = Column(String(50))  # دین (مذهب)
    
    # Location Information
    province = Column(String(100))  # استان
    city = Column(String(100))  # شهر
    address = Column(Text)  # آدرس محل سکونت
    phone_number = Column(String(20))  # شماره تماس
    
    # Personal Status
    marital_status = Column(String(50))  # وضعیت تأهل
    military_service_status = Column(String(50))  # وضعیت خدمت وظیفه
    physical_status = Column(String(50))  # وضعیت جسمانی
    health_description = Column(Text)  # توضیح سطح سلامت
    nationality = Column(String(50))  # ملیت
    
    # Professional Information
    activity_field = Column(String(100))  # حوزه فعالیت
    educational_background = Column(Text)  # سوابق تحصیلی
    work_experience = Column(Text)  # تجربیات شغلی
    foreign_languages = Column(Text)  # زبان های خارجی
    certificates = Column(Text)  # گواهینامه دوره های گذرانده شده
    requested_cooperation = Column(Text)  # همکاری پیشنهادی مورد درخواست
    proposed_salary = Column(String(20))  # حقوق پیشنهادی
    scientific_activities = Column(Text)  # فعالیت های علمی
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="program_404640758_data")

# Program 403640724 Data Model - Cyber Hidden Monitoring Actions
class Program403640724Data(Base):
    __tablename__ = "program_403640724_data"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Basic Information
    row_number = Column(String(10))  # ردیف
    category_name = Column(String(200))  # نام رده
    phone_email_action = Column(String(200))  # شماره تلفن / ایمیل / تحت اقدام
    
    # Virtual Networks Monitoring (شبکه های مجازی)
    telegram_count = Column(Integer, default=0)  # تلگرام
    instagram_count = Column(Integer, default=0)  # اینستاگرام
    rubika_count = Column(Integer, default=0)  # روبیکا
    soroush_count = Column(Integer, default=0)  # سروش
    whatsapp_count = Column(Integer, default=0)  # واتس اپ
    bale_count = Column(Integer, default=0)  # بله
    igap_count = Column(Integer, default=0)  # آی گپ
    shad_count = Column(Integer, default=0)  # شاد
    eitaa_count = Column(Integer, default=0)  # ایتا
    gap_count = Column(Integer, default=0)  # گپ
    other_virtual_networks_count = Column(Integer, default=0)  # سایر شبکه های مجازی
    
    # Email Monitoring (پست های الکترونیکی)
    gmail_count = Column(Integer, default=0)  # Gmail
    yahoo_count = Column(Integer, default=0)  # Yahoo
    microsoft_count = Column(Integer, default=0)  # Microsoft
    other_emails_count = Column(Integer, default=0)  # سایر پست های الکترونیکی
    
    # News Registration (اخبار ثبت شده در سامانه نباء)
    registered_news_numbers = Column(String(500))  # شماره خبر های ثبت شده
    final_case_result = Column(String(500))  # نتیجه نهایی پرونده
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="program_403640724_data")

# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
