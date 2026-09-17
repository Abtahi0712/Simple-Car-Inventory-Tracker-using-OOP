# Simple Car Inventory Tracker

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![OOP](https://img.shields.io/badge/Paradigm-OOP-blueviolet)
![License](https://img.shields.io/badge/License-MIT-green)

A command-line car inventory management system built as a demonstration of core **Object-Oriented Programming** principles in Python — encapsulation, abstraction, inheritance, and polymorphism.

---

## 🎯 Purpose

This project applies OOP design to a real-world problem: managing a car dealership's vehicle stock. Each concept is implemented deliberately so the codebase can serve as a reference for OOP patterns in Python.

---

## 🏗️ OOP Concepts Demonstrated

### 1. Classes & Objects
The `Car` class models a real-world vehicle with attributes and behaviours. Each car in the inventory is an **instance** (object) of this class.

```python
car = Car(make="Toyota", model="Corolla", year=2020, price=18500, mileage=32000)
print(car)  # Toyota Corolla (2020) — $18,500 | 32,000 km
```

### 2. Encapsulation
Attributes are kept private (`_price`, `_mileage`) and accessed through **properties**, preventing invalid data from entering the system.

```python
car.price = -500   # ❌ Raises ValueError — price cannot be negative
car.price = 16000  # ✅ Valid update via setter
```

### 3. Abstraction
The `Inventory` class hides the complexity of how cars are stored and searched. Users call simple methods like `add()`, `remove()`, and `search_by_make()` without knowing the internal data structure.

```python
inventory = Inventory()
inventory.add(car)
results = inventory.search_by_make("Toyota")
```

### 4. Inheritance
`ElectricCar` and `PetrolCar` extend the base `Car` class, adding fuel-specific attributes while reusing all shared logic.

```python
ev = ElectricCar(make="Tesla", model="Model 3", year=2022,
                 price=42000, mileage=15000, range_km=560)
```

### 5. Polymorphism
Both `Car` subclasses override `__str__()` to display their own formatted summary, while the inventory treats them identically as `Car` objects.

```python
for car in inventory.get_all():
    print(car)  # Each subclass prints its own format
```

### 6. Dunder / Magic Methods
`__str__`, `__repr__`, `__eq__`, and `__len__` are implemented to make objects behave naturally in Python contexts (printing, comparison, `len(inventory)`).

---

## ✨ Features

- Add, remove, and list vehicles
- Search by make, model, or year range
- Filter by price range or fuel type
- Sort inventory by price, year, or mileage
- Input validation on all fields
- Persistent storage via JSON file

---

## 📁 Project Structure

```
Simple-Car-Inventory-Tracker-using-OOP/
├── models/
│   ├── car.py           # Base Car class with encapsulated attributes
│   ├── electric_car.py  # ElectricCar subclass (range, charge time)
│   └── petrol_car.py    # PetrolCar subclass (fuel efficiency)
├── inventory.py         # Inventory class — manages the car collection
├── storage.py           # JSON persistence layer
├── cli.py               # Command-line interface / menu system
├── main.py              # Entry point
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+

### Run the program

```bash
git clone https://github.com/Abtahi0712/Simple-Car-Inventory-Tracker-using-OOP.git
cd Simple-Car-Inventory-Tracker-using-OOP
python main.py
```

No external dependencies — uses only the Python standard library.

### Menu options

```
=== Car Inventory Tracker ===
1. Add a car
2. Remove a car
3. View all cars
4. Search by make / model
5. Filter by price range
6. Sort inventory
7. Exit
```

---

## 💡 Key Design Decisions

**Why private attributes with properties?** Raw attribute access (e.g. `car.price = -100`) would allow corrupt data. Properties enforce business rules at the point of assignment without the caller needing to call a validation function manually.

**Why a separate `Inventory` class instead of a plain list?** Bundling the collection with its operations (search, sort, filter) keeps related logic together and makes the interface predictable — a core principle of encapsulation.

**Why subclasses for Electric vs Petrol?** Fuel type affects which attributes make sense (`range_km` vs `fuel_efficiency_L100km`). Inheritance avoids `if fuel_type == "electric"` branches scattered throughout the codebase.

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.
