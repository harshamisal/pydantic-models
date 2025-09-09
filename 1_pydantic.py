from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated

# Patient model using Pydantic
class Patient(BaseModel):

    # -------------------------------
    # BASIC way to declare datatypes
    # -------------------------------
    name: str                # simple string
    email: str               # simple string (no format check)
    linkedin: str            # simple string
    age: int                 # integer (no restrictions)
    weight: float            # float (any number)
    married: bool = False    # boolean with default value
    allergies: List[str]     # list of strings
    contact_details: Dict[str, str]   # dictionary with key/value as strings

    # -------------------------------
    # MODIFIED way (with validation)
    # -------------------------------
    
    # Adds max length, title, description, and example usage
    name: Annotated[str, Field(max_length=50, title='Name of the patient',
                               description='Give the name of the patient in less than 50 chars',
                               examples=['Harsha', 'Pinku'])]

    # Validates email format automatically
    email: EmailStr

    # Ensures it is a valid URL
    linkedin: AnyUrl

    # Age must be >0 and <25 (with type coercion from str → int)
    age: int = Field(gt=0, lt=25)

    # Weight must be >0, strict=True means no type coercion (str → float not allowed)
    weight: Annotated[float, Field(gt=0, strict=True)]

    # Boolean field with default and description
    married: Annotated[bool, Field(default=None, description='Is the patient married or not')]

    # Optional list of allergies with default value and max length restriction
    allergies: Annotated[Optional[List[str]], Field(default='No allergies', max_length=5)]

    # Contact details remain dictionary but validated strictly
    contact_details: Dict[str, str]


# Example function to insert patient data
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


# Sample patient data
patient_info = {
    'name': 'harsha',
    'email': 'abc@gmail.com',
    'linkedin': 'http://linkedin.com/',
    'age': '22',        # type coercion str → int
    'weight': 44.2,     # valid float
    'contact_details': {'email': 'abc@gmail.com', 'phone': '12345'}
}

# Validation + coercion happens here
patient1 = Patient(**patient_info)

# Insert data
insert_patient_data(patient1)