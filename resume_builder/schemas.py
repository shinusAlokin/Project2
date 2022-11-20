from pydantic import BaseModel, Field, validator, ValidationError, constr
#from pydantic import EmailStr
from pydantic import schema, root_validator
from typing import Annotated, Optional, Any
from datetime import date, datetime
import re

class BasicDetailsSchema(BaseModel):
    name:str 
    email_address: str
    phone_number:  str
    summary: str


    class Config:
        orm_mode = True

    @validator('*', pre=True)
    def val_all(cls, val):
        if val == '':
            raise ValueError(f"You should enter value for all of the required fields")
        return val

    @validator('name')
    def name_val(cls, val):
        name_regex = r"[A-Za-z]\s?"
        if len(val) < 3:
            raise ValueError('Name must be atleast 3 characters')
        if not re.match(name_regex, val):
            raise ValueError('Invlid Name')
        return val

    @validator('email_address')
    def is_valid_email(cls, val):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(regex, val):
            raise ValueError("Email is not valid")
        return val
            

    @validator('phone_number')
    def is_valid_phone_number(cls, val):
        pattern = r"^((\+1|1)?(\d{3}))?[- ]?(\d{3})[- ]?(\d{4})$"
        if not re.match(pattern, val):
            raise ValueError("Invalid phone number")
        return val


class LocationDetailsSchema(BaseModel):
    address_line: Annotated[str, Field(min_length=3)]
    street_name: Annotated[str, Field(min_length=3)]
    city: Annotated[str, Field(min_length=3)]
    country: Annotated[str, Field(min_length=2)]
    zip_code: str

    class Config:
        orm_mode = True

    @root_validator
    def is_valid_zip_code(cls, values):
        country, zip_code = values.get('country'), values.get('zip_code')
        us_pattern = r"^[0-9]{5}(-[0-9]{4})?$"
        indian_pattern = r"^[1-9]{1}[0-9]{2}\s{0,1}[0-9]{3}$"
        if country == 'India':
            if not re.match(indian_pattern,zip_code):
                raise ValueError("Invalid Pin Code for India")
            return values
        elif country == 'US':
            if not re.match(us_pattern,zip_code):
                raise ValueError("Invalid Zip Code for US")
            return values
        return values


class SkillsSchema(BaseModel):
    skill: Annotated[str, Field(min_length=2)]
    rating: str

    class Config:
        orm_mode = True

    @validator('*', pre=True)
    def val_all(cls, val):
        if val == '':
            raise ValueError(f"You should enter value for all the required fields of skill")
        return val


class EducationSchema(BaseModel):
    qualification: Annotated[str, Field(min_length=2)]
    course_name: Annotated[str, Field(min_length=2)]
    location: Annotated[str, Field(min_length=2)]
    institute_name: Annotated[str, Field(min_length=2)]
    start_date: date
    end_date: date

    class Config:
        orm_mode = True

    @validator('*', pre=True)
    def val_all(cls, val):
        if val == '':
            raise ValueError(f"You should enter value for all the fields of Education")
        return val

    @root_validator
    def check_dates(cls, values):
        start = datetime.strftime(values.get('start_date'), '%Y-%m-%d')
        end =  datetime.strftime(values.get('end_date'), '%Y-%m-%d')
        if int(end.split('-')[0]) - int(start.split('-')[0]) < 0:
            raise ValueError('Start date of education should come before end date')
        return values
        

class WorkSchema(BaseModel):
    organisation: Optional[str]
    job_role: Optional[str]
    key_roles: Optional[str]
    start_date: date
    end_date: date

    class Config:
        orm_mode = True
    
    # @validator('*', pre=True)
    # def val_all(cls, val):
    #     if val == '':
    #         raise ValueError(f"You should enter value for all the required fields of Work experience")
    #     return val

    @root_validator
    def check_dates(cls, values):
        start = datetime.strftime(values.get('start_date'), '%Y-%m-%d')
        end =  datetime.strftime(values.get('end_date'), '%Y-%m-%d')
        if (int(end.split('-')[0]) - int(start.split('-')[0])) < 0:
            raise ValueError('Start date of work should come before end date')
        return values


class ProjectSchema(BaseModel):
    project_title: str #Annotated[str, Field(min_length=2)]
    skills: str #Annotated[str, Field(min_length=2)]
    description: str #Annotated[str, Field(min_length=10)]

    class Config:
        orm_mode = True


class SocialMediaSchema(BaseModel):
    network: str 
    url: str 
    user_name: str 

    class Config:
        orm_mode = True

