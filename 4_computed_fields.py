from pydantic import BaseModel, EmailStr, AnyUrl, Field, computed_field
from typing import List, Dict, Optional, Annotated

# ----------------------------------------------------
# BASIC VERSION → only type annotations
# ----------------------------------------------------
class PatientBasic(BaseModel):
    name: str
    email: EmailStr
    linkedin: AnyUrl
    age: int
    weight: float  # in kg
    height: float  # in meters
    married: bool = False
    allergies: List[str]
    contact_details: Dict[str, str]


# ----------------------------------------------------
# MODIFIED VERSION → with validation, metadata & computed field
# ----------------------------------------------------
class Patient(BaseModel):

    # ---- FIELD DEFINITIONS ----
    name: Annotated[str, Field(
        max_length=50,
        title="Patient's Name",
        description="Enter full name of the patient (≤ 50 characters)",
        examples=["Harsha", "Pinku"]
    )]

    email: EmailStr  # ensures correct email format
    linkedin: AnyUrl  # validates proper URL

    age: Annotated[int, Field(gt=0, lt=120)]  # realistic age check
    weight: Annotated[float, Field(gt=0)]  # must be > 0
    height: Annotated[float, Field(gt=0)]  # must be > 0

    married: Annotated[bool, Field(
        default=False,
        description="Is the patient married?"
    )]

    allergies: Annotated[List[str], Field(
        default_factory=list,
        max_length=10,  # at most 10 allergies
        description="List of patient allergies"
    )]

    contact_details: Dict[str, str]  # dictionary of contact info

    # ---- COMPUTED FIELD ----
    @computed_field  # automatically computed field
    @property
    def calculate_bmi(self) -> float:
        """Auto-calculated Body Mass Index (BMI)."""
        return round(self.weight / (self.height ** 2), 2)


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
    print('BMI:', patient.calculate_bmi)
    print('updated')


# ----------------------------------------------------
# INPUT DATA
# ----------------------------------------------------
patient_info = {
    'name': 'harsha',
    'email': 'abc@hdfc.com',
    'linkedin': 'http://linkedin.com/',
    'age': '28',  # string → coerced into int
    'weight': 75.2,
    'height': 1.72,
    'married': True,
    'allergies': ['pollen', 'dust'],
    'contact_details': {'email': 'abc@gmail.com', 'phone': '12345'}
}

patient1 = Patient(**patient_info)  # dict unpacking + validation
# insert_patient_data(patient1)
update_patient_data(patient1)