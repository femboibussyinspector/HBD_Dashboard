# model/master_model.py

from sqlalchemy import Column, Integer, String, Float, Text, JSON, TIMESTAMP, Index
from sqlalchemy.sql import func
from extensions import db

class MasterTable(db.Model):
    __tablename__ = "master_table"

    id = Column(Integer, primary_key=True, autoincrement=True)
    global_business_id = Column(String(100), index=True, unique=True, nullable=False)
    business_id = Column(String(100), index=True, nullable=False)
    business_name= Column(String(255), nullable=False)
    business_category= Column(String(100), index=True, nullable=True)
    business_subcategory= Column(String(100), nullable=True)
    ratings= Column(Float, nullable= True)
    primary_phone = Column(String(20), nullable=False) #
    secondary_phone= Column(String(20), nullable=True)
    other_phones= Column(String(20), nullable=True)
    virtual_phone= Column(String(20), nullable=True)
    whatsapp_phone= Column(String(20), nullable=True)
    email= Column(String(255), index=True, nullable=False)  #
    website_url= Column(String(255), nullable=True) #
    facebook_url=Column(String(255), nullable=True)
    linkedin_url=Column(String(255), nullable=True)
    twitter_url=Column(String(255), nullable=True)
    address=Column(String(255), nullable=False)
    area=Column(String(100),index=True, nullable=True)
    city=Column(String(50),index=True, nullable=False)
    state=Column(String(50), nullable=False)
    pincode= Column(String(10), nullable=False)
    country= Column(String(50), nullable=False, default='India') 
    latitude= Column(Float, nullable=True)
    longitude= Column(Float, nullable=True)
    avg_fees= Column(Float, nullable=True)   #
    course_details= Column(Text, nullable=True)
    duration= Column(String(100), nullable=True)
    requirement= Column(Text, nullable=True)
    avg_spent= Column(Float, nullable=True)
    cost_for_two= Column(Float, nullable=True)
    reviews= Column(Integer, nullable=True)  #
    description= Column(Text, nullable=True)
    data_source= Column(String(255), index=True, nullable=True)
    avg_salary= Column(Float, nullable=True)
    admission_req_list= Column(Text, nullable=True)
    courses= Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), index=True)
    # ---- SERIALIZERS ----
    def to_dict_basic(self):
        return {
            "id": self.id,
            "business_name": self.business_name,
            "business_category": self.business_category,
            "city": self.city,
            "area": self.area,
            "ratings": self.ratings,
            "data_source": self.data_source,
        }
    def to_dict(self):
        return {
            "id": self.id,
            "global_business_id": self.global_business_id,
            "business_id": self.business_id,
            "business_name": self.business_name,
            "business_category": self.business_category,
            "business_subcategory": self.business_subcategory,
            "ratings": self.ratings,
            "primary_phone": self.primary_phone,
            "secondary_phone": self.secondary_phone,
            "other_phones": self.other_phones,
            "virtual_phone": self.virtual_phone,
            "whatsapp_phone": self.whatsapp_phone,
            "email": self.email,
            "website_url": self.website_url,
            "facebook_url": self.facebook_url,
            "linkedin_url": self.linkedin_url,
            "twitter_url": self.twitter_url,
            "address": self.address,
            "area": self.area,
            "city": self.city,
            "state": self.state,
            "pincode": self.pincode,
            "country": self.country,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "avg_fees": self.avg_fees,
            "course_details": self.course_details,
            "duration": self.duration,
            "requirement": self.requirement,
            "avg_spent": self.avg_spent,
            "cost_for_two": self.cost_for_two,
            "reviews": self.reviews,
            "description": self.description,
            "data_source": self.data_source,
            "avg_salary": self.avg_salary,
            "admission_req_list": self.admission_req_list,
            "courses": self.courses,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
