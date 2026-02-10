import javaobj.v2 as javaobj

with open('../../Surplus/person.ser', 'rb') as f:
    serialized_data = f.read()

person_obj = javaobj.loads(serialized_data)

print("Desirialized Java Object in Python:")
print(f"Name: {person_obj.name}")
print(f"Age: {person_obj.age}")

