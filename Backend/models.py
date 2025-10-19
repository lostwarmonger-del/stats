# models.py - Pydantic models for API requests/responses
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Authentication models
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict

class UserCreateRequest(BaseModel):
    username: str
    name: str
    password: str
    role: str = "user"

class UserResponse(BaseModel):
    id: int
    username: str
    name: str
    role: str
    is_active: bool

# Notification models
class NotificationCreateRequest(BaseModel):
    title: str
    message: str

class NotificationResponse(BaseModel):
    id: int
    title: str
    message: str
    created_at: datetime
    created_by: int
    created_by_name: str

# Program 404640723 models
class Program404640723Request(BaseModel):
    row_number: str = ""
    page_channel_address: str = ""
    news_subject: str = ""
    naba_code: int = 0  # Changed to int
    naba_code_review: str = ""
    naba_code_registration_date: str = ""  # Shamsi date as string
    suspicion_classification: int = 0  # Changed to int
    suspicion_registration_date: str = ""  # Shamsi date as string
    action_results: str = ""
    identified_military_count: int = 0  # Changed to int
    identified_military_dependents_count: int = 0  # Changed to int
    honorary_police: int = 0  # Changed to int

class Program404640723Response(BaseModel):
    id: int
    user_id: int
    row_number: Optional[str]
    page_channel_address: Optional[str]
    news_subject: Optional[str]
    naba_code: Optional[str]
    naba_code_review: Optional[str]
    naba_code_registration_date: Optional[str]
    suspicion_classification: Optional[str]
    suspicion_registration_date: Optional[str]
    action_results: Optional[str]
    identified_military_count: Optional[str]
    identified_military_dependents_count: Optional[str]
    honorary_police: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Program404640725Request(BaseModel):
    row_number: str = ""
    page_channel_address: str = ""
    news_subject: str = ""
    naba_code: int = 0  # Changed to int
    naba_code_review: str = ""
    naba_code_registration_date: str = ""  # Shamsi date as string
    suspicion_classification: int = 0  # Changed to int
    suspicion_registration_date: str = ""  # Shamsi date as string
    action_results: str = ""
    identified_military_count: int = 0  # Changed to int
    identified_military_dependents_count: int = 0  # Changed to int
    honorary_police: int = 0  # Changed to int

class Program404640725Response(BaseModel):
    id: int
    user_id: int
    row_number: Optional[str]
    page_channel_address: Optional[str]
    news_subject: Optional[str]
    naba_code: Optional[str]
    naba_code_review: Optional[str]
    naba_code_registration_date: Optional[str]
    suspicion_classification: Optional[str]
    suspicion_registration_date: Optional[str]
    action_results: Optional[str]
    identified_military_count: Optional[str]
    identified_military_dependents_count: Optional[str]
    honorary_police: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Program 404640758 models
class Program404640758Request(BaseModel):
    first_name: str = ""
    last_name: str = ""
    father_name: str = ""
    id_number: str = ""
    birth_date: str = ""  # Shamsi date as string
    national_id: str = ""
    id_issue_date: str = ""  # Shamsi date as string
    id_issue_place: str = ""
    religion: str = ""
    province: str = ""
    city: str = ""
    marital_status: str = ""
    military_service_status: str = ""
    physical_status: str = ""
    health_description: str = ""
    nationality: str = ""
    activity_field: str = ""
    educational_background: str = ""
    work_experience: str = ""
    foreign_languages: str = ""
    certificates: str = ""
    requested_cooperation: str = ""
    proposed_salary: str = ""
    scientific_activities: str = ""
    address: str = ""
    phone_number: str = ""

class Program404640758Response(BaseModel):
    id: int
    user_id: int
    first_name: Optional[str]
    last_name: Optional[str]
    father_name: Optional[str]
    id_number: Optional[str]
    birth_date: Optional[str]
    national_id: Optional[str]
    id_issue_date: Optional[str]
    id_issue_place: Optional[str]
    religion: Optional[str]
    province: Optional[str]
    city: Optional[str]
    marital_status: Optional[str]
    military_service_status: Optional[str]
    physical_status: Optional[str]
    health_description: Optional[str]
    nationality: Optional[str]
    activity_field: Optional[str]
    educational_background: Optional[str]
    work_experience: Optional[str]
    foreign_languages: Optional[str]
    certificates: Optional[str]
    requested_cooperation: Optional[str]
    proposed_salary: Optional[str]
    scientific_activities: Optional[str]
    address: Optional[str]
    phone_number: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Program 403640724 models
class Program403640724Request(BaseModel):
    row_number: str = ""
    category_name: str = ""
    phone_email_action: str = ""
    telegram_count: int = 0
    instagram_count: int = 0
    rubika_count: int = 0
    soroush_count: int = 0
    whatsapp_count: int = 0
    bale_count: int = 0
    igap_count: int = 0
    shad_count: int = 0
    eitaa_count: int = 0
    gap_count: int = 0
    other_virtual_networks_count: int = 0
    gmail_count: int = 0
    yahoo_count: int = 0
    microsoft_count: int = 0
    other_emails_count: int = 0
    registered_news_numbers: str = ""
    final_case_result: str = ""

class Program403640724Response(BaseModel):
    id: int
    user_id: int
    row_number: Optional[str]
    category_name: Optional[str]
    phone_email_action: Optional[str]
    telegram_count: Optional[int]
    instagram_count: Optional[int]
    rubika_count: Optional[int]
    soroush_count: Optional[int]
    whatsapp_count: Optional[int]
    bale_count: Optional[int]
    igap_count: Optional[int]
    shad_count: Optional[int]
    eitaa_count: Optional[int]
    gap_count: Optional[int]
    other_virtual_networks_count: Optional[int]
    gmail_count: Optional[int]
    yahoo_count: Optional[int]
    microsoft_count: Optional[int]
    other_emails_count: Optional[int]
    registered_news_numbers: Optional[str]
    final_case_result: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Token models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str = None
