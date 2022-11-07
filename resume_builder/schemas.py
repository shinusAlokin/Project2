from pydantic import BaseModel, Field, validator, ValidationError
from pydantic import EmailStr
from pydantic import schema
import re

class BasicDetailsSchema(BaseModel):
    name: str
    email_address: EmailStr
    phone_number: str 
    image_url: str
    summary: str

    class Config:
        orm_mode = True

    @validator('email_address')
    def is_valid_email(cls, val):
        email_pattern = "^[a-z]([\w-]*[a-z]|[\w-.]*[a-z]{2,}|[a-z])*@[a-z]([\w-]*[a-z]|[\w-.]*[a-z]{2,}|[a-z]){4,}?\.[a-z]{2,}$"
        if not re.match(email_pattern, val):
            raise ValidationError("Invalid Email Address")
        return val.title()

    @validator('phone_number')
    def is_valid_phone_number(cls, val):
        pass


class LocationDetailsSchema(BaseModel):
    address_line: str
    street_name: str
    city: str
    country: str
    zip_code: str

    @validator('zip_code')
    def validate_zip_code(cls, val):
        pass


class SkillsSchema(BaseModel):
    pass

class EducationSchema(BaseModel):
    pass

class WorkSchema(BaseModel):
    pass

class ProjectSchema(BaseModel):
    pass

class SocialMediaSchema(BaseModel):
    pass
