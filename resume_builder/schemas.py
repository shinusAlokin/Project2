from pydantic import BaseModel, Field, validator, ValidationError, constr
#from pydantic import EmailStr
from pydantic import schema, root_validator
from typing import Annotated, Optional
from datetime import date, datetime
import re

class BasicDetailsSchema(BaseModel):
    name:str
    email_address: str
    phone_number:  str
    image_url: str
    summary: str

    class Config:
        orm_mode = True

    @validator('*', pre=True)
    def val_all(cls, val):
        if val == '':
            raise ValueError(f"You should enter value for  ")
        return val

    @validator('name')
    def name_val(cls, val):
        if len(val) < 3:
            raise ValueError('Name should be more than 2 characters')

    @validator('email_address')
    def is_valid_email(cls, val):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(regex, val):
            raise ValueError("Email is not valid")
        else: 
            return val.title()
            

    # @validator('phone_number')
    # def is_valid_phone_number(cls, val):
    #     pattern = r"0|1|91?[6-9][0-9]{9}"
    #     if not re.match(pattern, val):
    #         raise ValueError("Invalid phone number")
    #     else:
    #         return val.title()



class LocationDetailsSchema(BaseModel):
    address_line: Annotated[str, Field(min_length=3)]
    street_name: Annotated[str, Field(min_length=3)]
    city: Annotated[str, Field(min_length=3)]
    country: Annotated[str, Field(min_length=3)]
    zip_code: Annotated[str, Field(min_length=3)]

    class Config:
        orm_mode = True


class SkillsSchema(BaseModel):
    skill: Annotated[str, Field(min_length=2)]
    rating: str

    class Config:
        orm_mode = True

    @validator('rating')
    def is_valid_rating(cls, val):
        if not val:
            raise ValueError('You should enter a value for rating')
        try:
            float(val)
        except ValueError:
            raise ValueError('You should enter a number for rating')
        if float(val) > 10:
                raise ValueError('Rating should be between 1 and 10')

        return val.title()


class EducationSchema(BaseModel):
    qualification: Annotated[str, Field(min_length=2)]
    course_name: Annotated[str, Field(min_length=2)]
    location: Annotated[str, Field(min_length=2)]
    institute_name: Annotated[str, Field(min_length=2)]
    start_date: date
    end_date: date

    class Config:
        orm_mode = True

    @root_validator
    def check_dates(cls, values):
        start = datetime.strftime(values.get('start_date'), '%Y-%m-%d')
        end =  datetime.strftime(values.get('end_date'), '%Y-%m-%d')
        if int(end.split('-')[0]) - int(start.split('-')[0]) < 0:
            raise ValueError('Start date of education should come before end date')
        return values
        

class WorkSchema(BaseModel):
    organisation: Annotated[str, Field(min_length=3)]
    job_role: Annotated[str, Field(min_length=3)]
    key_roles: Annotated[str, Field(min_length=3)]
    start_date: date
    end_date: date

    class Config:
        orm_mode = True

    @root_validator
    def check_dates(cls, values):
        start = datetime.strftime(values.get('start_date'), '%Y-%m-%d')
        end =  datetime.strftime(values.get('end_date'), '%Y-%m-%d')
        if int(end.split('-')[0]) - int(start.split('-')[0]) < 0:
            raise ValueError('Start date of work should come before end date')
        return values

class ProjectSchema(BaseModel):
    project_title: Annotated[str, Field(min_length=2)]
    skills: Annotated[str, Field(min_length=2)]
    description: Annotated[str, Field(min_length=10)]

    class Config:
        orm_mode = True

class SocialMediaSchema(BaseModel):
    network: Annotated[str, Field(min_length=2)]
    url: Annotated[str, Field(min_length=2)]
    user_name: Annotated[str, Field(min_length=2)]

    class Config:
        orm_mode = True
