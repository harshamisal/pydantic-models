
# ----------------------------------------------------
# NESTED MODELS
# Better organization of related data(e.g. vitals, address, insurance)
# Reusability: use vitals in multiple models(e.g. Patient, MedicalRecord)
# Readability: easier for developers and API consumer to understand
# Automatic validation: nested models are validated automatically - no extra work needed
# ----------------------------------------------------

from pydantic import BaseModel, Field
from typing import Annotated


# ----------------------------------------------------
# BASIC VERSION → only type annotations
# ----------------------------------------------------
class AddressBasic(BaseModel):
    city: str
    state: str
    pin: int


class PatientBasic(BaseModel):
    name: str
    gender: str
    age: int
    address: AddressBasic  # Nested model


# ----------------------------------------------------
# ENHANCED VERSION → with validation + metadata
# ----------------------------------------------------
class Address(BaseModel):
    city: Annotated[str, Field(
        min_length=2,
        description="City name (at least 2 characters)",
        examples=["Pune", "Mumbai"]
    )]
    state: Annotated[str, Field(
        min_length=2,
        description="State code or name",
        examples=["MH", "KA"]
    )]
    pin: Annotated[int, Field(
        ge=100000, le=999999,
        description="6-digit postal PIN code"
    )]


class Patient(BaseModel):
    name: Annotated[str, Field(
        max_length=50,
        description="Patient's full name"
    )]
    gender: Annotated[str, Field(
        pattern="^(male|female|other)$",
        description="Gender of the patient (male/female/other)"
    )]
    age: Annotated[int, Field(
        gt=0, lt=120,
        description="Age of the patient (0 < age < 120)"
    )]
    address: Address  # Nested model → auto-validates Address fields


# ----------------------------------------------------
# SAMPLE DATA
# ----------------------------------------------------
address_dict = {
    'city': 'Pune',
    'state': 'MH',
    'pin': '411014'  # str → coerced into int
}
address1 = Address(**address_dict)

patient_dict = {
    'name': 'Harsha',
    'gender': 'female',
    'age': '28',  # str → coerced into int
    'address': address1  # can pass model instance or dict
}
patient1 = Patient(**patient_dict)


# ----------------------------------------------------
# OUTPUTS
# ----------------------------------------------------
print(patient1)                # full model
print("Age:", patient1.age)    # validated int
print("PIN:", patient1.address.pin)  # nested model field access