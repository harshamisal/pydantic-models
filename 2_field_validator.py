from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Optional, Annotated

# Patient model using Pydantic
class Patient(BaseModel):  # BaseModel → enables validation, serialization, type coercion

    # -------------------------------
    # BASIC way to declare datatypes
    # -------------------------------

    name: str                     # simple string
    email: str                    # simple string (no format check)
    linkedin: str                 # simple string
    age: int                      # integer (coercion if input is string → int)
    weight: float                 # float (any number, no restrictions)
    married: bool = False         # boolean with default value
    allergies: List[str]          # list of strings
    contact_details: Dict[str, str]   # dictionary with string keys & values

    # -------------------------------
    # MODIFIED way (with validation)
    # -------------------------------

    # Annotated → combines type + validation rules + metadata (title, description, examples)
    name: Annotated[str, Field(
        max_length=50,
        title='Name of the patient',
        description='Give the name of the patient in less than 50 chars',
        examples=['Harsha', 'Pinku']
    )]

    # EmailStr → enforces valid email format
    email: EmailStr

    # AnyUrl → ensures linkedin is a valid URL
    linkedin: AnyUrl
    
    # stricter version with conditions:
    age: int = Field(gt=0, lt=25)   # restricts to 0 < age < 25

    # weight: float = Field(gt=0)     # weight must be > 0
    weight: Annotated[float, Field(gt=0, strict=True)]  
    # strict=True → prevents type coercion (e.g., '44.2' string won't auto-convert to float)

    # Boolean with metadata & default
    married: Annotated[bool, Field(
        default=None,
        description='Is the patient married or not'
    )]

    # Optional → can be None, default set to "No allergies"
    # max_length=5 → max 5 allergy items allowed
    allergies: Annotated[Optional[List[str]], Field(
        default='No allergies',
        max_length=5
    )]

    # Dictionary is still enforced but validated more strictly
    contact_details: Dict[str, str]


    # -------------------------------
    # FIELD VALIDATORS
    # -------------------------------

    @field_validator('email')  # runs only on email field
    @classmethod
    def email_validator(cls, value):
        valid_domains = ['hdfc.com', 'icici.com']
        domain_name = value.split('@')[-1]

        # Custom rule: only allow hdfc.com or icici.com domains
        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')
        return value  # return validated email

    @field_validator('name')  # runs only on name field
    @classmethod
    def transform_name(cls, value):
        # Automatically transforms name to uppercase
        return value.upper()

    @field_validator('age', mode='before')  
    # mode='before' → validation happens before type coercion
    @classmethod
    def validate_age(cls, value):
        # Custom rule: age must be between 0 and 50
        if 0 < value < 50:
            return value
        else:
            raise ValueError('Age should be in between 0 and 50')


# -------------------------------
# FUNCTIONS USING MODEL
# -------------------------------
def insert_patient_data(patient: Patient):  # accepts validated Patient model
    print(patient.name)
    print(patient.email)
    print(patient.linkedin)
    print(patient.age)
    print(patient.weight) 
    print(patient.married) 
    print(patient.allergies) 
    print(patient.contact_details) 
    print('inserted')

def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.email)
    print(patient.age)
    print(patient.weight) 
    print(patient.married) 
    print(patient.allergies) 
    print(patient.contact_details) 
    print('updated')


# -------------------------------
# INPUT DATA
# -------------------------------
patient_info = {
    'name': 'harsha',
    'email': 'abc@hdfc.com',    # passes custom domain validator
    'linkedin': 'http://linkedin.com/',
    'age': 28,                  # int is fine, validator checks range
    'weight': 44.2,             # valid float
    # 'married': True,           # optional
    # 'allergies': ['pollen', 'dust'],
    'contact_details': {'email':'abc@gmail.com', 'phone': '12345'}
}

# Unpack dict into Patient model → validation + type coercion happen here
patient1 = Patient(**patient_info)

# Insert validated patient data
insert_patient_data(patient1)
# update_patient_data(patient1)