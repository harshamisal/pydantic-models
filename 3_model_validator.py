from pydantic import BaseModel, EmailStr, AnyUrl, Field, model_validator
from typing import List, Dict, Optional, Annotated

# ----------------------------------------------------
# BASIC VERSION → just type annotations
# ----------------------------------------------------

class PatientBasic(BaseModel):  # simple version with only types
    name: str
    email: EmailStr
    linkedin: AnyUrl
    age: int
    weight: float
    married: bool
    allergies: Optional[List[str]]
    contact_details: Dict[str, str]


# ----------------------------------------------------
# MODIFIED VERSION → types + validation + metadata
# ----------------------------------------------------

class Patient(BaseModel):  # Inherit from BaseModel → enables Pydantic validation

    # ---- FIELD DEFINITIONS ----
    name: Annotated[str, Field(
        max_length=50,
        title='Name of the patient',
        description='Give the name of the patient in less than 50 chars',
        examples=['Harsha', 'Pinku']
    )]

    email: EmailStr  # EmailStr → validates proper email format
    linkedin: AnyUrl  # AnyUrl → validates proper URL format

    age: int = Field(gt=0, lt=25)  # only accepts 1–24

    weight: Annotated[float, Field(gt=0, strict=True)]  # must be float, > 0, no coercion

    married: Annotated[bool, Field(
        default=None,
        description='Is the patient married or not'
    )]

    allergies: Annotated[Optional[List[str]], Field(
        default='No allergies',
        max_length=5  # at most 5 items
    )]

    contact_details: Dict[str, str]

    # ---- CUSTOM VALIDATOR ----

    @model_validator(mode='after')  # runs after full model is built
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError('patients older than 60 must have emergency contact')
        return model


# ----------------------------------------------------
# FUNCTIONS USING MODEL
# ----------------------------------------------------
def insert_patient_data(patient: Patient):
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
    print(patient.linkedin)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    print('updated')


# ----------------------------------------------------
# INPUT DATA
# ----------------------------------------------------
patient_info = {
    'name': 'harsha',
    'email': 'abc@hdfc.com',
    'linkedin': 'http://linkedin.com/',
    'age': '28',   # str → coerced into int
    'weight': 44.2,
    # 'married': True,
    # 'allergies': ['pollen', 'dust'],
    'contact_details': {'email': 'abc@gmail.com', 'phone': '12345'}
}

patient1 = Patient(**patient_info)  # dict unpacking + validation + coercion
insert_patient_data(patient1)
# update_patient_data(patient1)
