# ----------------------------------------------------
# SERIALIZATION EXAMPLE WITH PYDANTIC
# ----------------------------------------------------
# Serialization = converting model → dict / JSON for APIs, DB storage, etc.
# Useful for:
# Sending model data in API responses
# Excluding optional/unset/default fields
# Including/excluding specific fields
# ----------------------------------------------------

from pydantic import BaseModel, Field
from typing import Annotated


# ----------------------------------------------------
# BASIC VERSION → just plain models
# ----------------------------------------------------
class AddressBasic(BaseModel):
    city: str
    state: str
    pin: int


class PatientBasic(BaseModel):
    name: str = 'User'   # default value if not provided
    gender: str
    age: int
    address: AddressBasic


# ----------------------------------------------------
# ENHANCED VERSION → with serialization options
# ----------------------------------------------------
class Address(BaseModel):
    city: Annotated[str, Field(description="City name")]
    state: Annotated[str, Field(description="State code")]
    pin: Annotated[int, Field(description="Postal code (6 digits)")]


class Patient(BaseModel):
    name: Annotated[str, Field(default='User', description="Default = 'User' if not provided")]
    gender: str
    age: int
    address: Address


# ----------------------------------------------------
# SAMPLE DATA
# ----------------------------------------------------
address_dict = {
    'city': 'Pune',
    'state': 'MH',
    'pin': '414001'  # str → coerced into int
}
address1 = Address(**address_dict)

patient_dict = {
    # 'name': 'Harsha',   # excluded → will use default "User"
    'gender': 'female',
    'age': '28',         # str → coerced into int
    'address': address1
}
patient1 = Patient(**patient_dict)


# ----------------------------------------------------
# SERIALIZATION DEMOS
# ----------------------------------------------------
# Default: full dict
print("\ Full dict:")
print(patient1.model_dump())

# Exclude default/unset fields (here "name" was not provided → excluded)
print("\ Exclude unset (exclude_unset=True):")
print(patient1.model_dump(exclude_unset=True))

# Only include specific fields
print("\ Only include ['name', 'age']:")
print(patient1.model_dump(include=['name', 'age']))

# Exclude specific fields
print("\ Exclude ['name', 'age']:")
print(patient1.model_dump(exclude=['name', 'age']))

# JSON serialization (string format, ready for APIs)
print("\ JSON output:")
print(patient1.model_dump_json())


# ----------------------------------------------------
# OUTPUT TYPES
# ----------------------------------------------------
print("\nType of model_dump →", type(patient1.model_dump()))
print("Type of model_dump_json →", type(patient1.model_dump_json()))