import sqlite3
import pandas as pd

# Connect to SQLite database (creates a new database if it doesn't exist)
conn = sqlite3.connect('cleaning_service.db')
cursor = conn.cursor()

# Execute

# Create Employee Table
cursor.execute('''
    CREATE TABLE Employee (
        staffNo INTEGER PRIMARY KEY,
        staffFName TEXT,
        staffLName TEXT,
        staffAddress TEXT,
        staffSalary INTEGER,
        staffTelNo TEXT UNIQUE NOT NULL
    )
''')

# Insert tuples into the Employee table
employee_data = [
    (1, 'Oscar', 'Arana', '123 Main St', 100000, '954-1234'),
    (2, 'Zubaer', 'Chowdhury', '123 Amaro Dr', 75000, '303-1234'),
    (3, 'Justin', 'Prince', '500 Ponce De Leon Blvd', 75000, '219-1234'),
    (4, 'John', 'Doe', '1300 Memorial Drive', 50000, '555-1234'), 
    (5, 'Jane', 'Smith', '456 Elm St', 60000, '555-5678')
]

cursor.executemany('''
    INSERT INTO Employee (staffNo, staffFName, staffLName, staffAddress, staffSalary, staffTelNo)
    VALUES (?, ?, ?, ?, ?, ?)
''', employee_data)

# Create Client Table
cursor.execute('''
    CREATE TABLE Client (
        clientNo INTEGER PRIMARY KEY,
        clientFName TEXT,
        clientLName TEXT,
        clientAddress TEXT,
        clientTelNo TEXT UNIQUE NOT NULL
    )
''')

# Insert tuples into the Client table
client_data = [
    (1, 'Carol', 'Clark', '333 Maple St', '555-1111'),
    (2, 'David', 'Lee', '777 Birch St', '555-2222'),
    (3, 'Frank', 'Garcia', '888 Walnut St', '555-3333'),
    (4, 'Grace', 'Martinez', '999 Cherry St', '555-4444'),
    (5, 'Henry', 'Nguyen', '222 Chestnut St', '555-5555')
]

cursor.executemany('''
    INSERT INTO Client (clientNo, clientFName, clientLName, clientAddress, clientTelNo)
    VALUES (?, ?, ?, ?, ?)
''', client_data)

# Create Request Table
cursor.execute('''
    CREATE TABLE Request (
        requestID INTEGER PRIMARY KEY,
        startDate TEXT,
        startTime TEXT,
        duration INTEGER,
        comments TEXT,
        clientNo INTEGER,
        FOREIGN KEY(clientNo) REFERENCES Client(clientNo) ON UPDATE CASCADE ON DELETE CASCADE
    )
''')

# Insert tuples into the Request table
request_data = [
    (1, '2023-01-15', '08:00:00', 2, 'Need cleaning service', 1),
    (2, '2023-02-20', '10:30:00', 3, 'Deep cleaning required', 2),
    (3, '2023-03-10', '09:45:00', 1, 'Regular cleaning', 3),
    (4, '2023-04-05', '12:00:00', 4, 'Urgent cleaning needed', 4),
    (5, '2023-05-18', '14:15:00', 2, 'Specialized cleaning requested', 5)
]

cursor.executemany('''
    INSERT INTO Request (requestID, startDate, startTime, duration, comments, clientNo)
    VALUES (?, ?, ?, ?, ?, ?)
''', request_data)

# Create Equipment Table
cursor.execute('''
    CREATE TABLE Equipment (
        equipmentID INTEGER PRIMARY KEY,
        description TEXT,
        usage TEXT,
        cost INTEGER
    )
''')

# Insert tuples into the Equipment table
equipment_data = [
    (1, 'Vacuum Cleaner', 'Household', 200),
    (2, 'Mop and Bucket', 'Floor Cleaning', 50),
    (3, 'Dustpan and Brush', 'Cleaning Tools', 20),
    (4, 'Steam Cleaner', 'Deep Cleaning', 300),
    (5, 'Scrubbing Brushes', 'Surface Cleaning', 30)
]

cursor.executemany('''
    INSERT INTO Equipment (equipmentID, description, usage, cost)
    VALUES (?, ?, ?, ?)
''', equipment_data)

# Create RequestEquipmentAssignment table
cursor.execute('''
    CREATE TABLE RequestEquipmentAssignment (
        requestID INTEGER,
        equipmentID INTEGER,
        quantity INTEGER,
        FOREIGN KEY(requestID) REFERENCES Request(requestID) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY(equipmentID) REFERENCES Equipment(equipmentID) ON UPDATE CASCADE ON DELETE SET NULL
    )
''')

# Insert tuples into the RequestEquipmentAssignment table
request_equipment_data = [
    (1, 1, 1),
    (2, 2, 2),
    (3, 3, 1),
    (4, 4, 3),
    (5, 5, 2)
]

cursor.executemany('''
    INSERT INTO RequestEquipmentAssignment (requestID, equipmentID, quantity)
    VALUES (?, ?, ?)
''', request_equipment_data)

# Create EmployeeRequestAssignment table
cursor.execute('''
    CREATE TABLE EmployeeRequestAssignment (
        staffNo INTEGER,
        requestID INTEGER,
        assignmentDate TEXT,
        FOREIGN KEY(staffNo) REFERENCES Employee(staffNo) ON UPDATE CASCADE ON DELETE SET NULL,
        FOREIGN KEY(requestID) REFERENCES Request(requestID) ON UPDATE CASCADE ON DELETE CASCADE
    )
''')

# Insert tuples into the EmployeeRequestAssignment table
employee_request_data = [
    (1, 1, '2023-01-10'),
    (2, 2, '2023-02-15'),
    (3, 3, '2023-03-05'),
    (4, 4, '2023-04-01'),
    (5, 5, '2023-05-10')
]

cursor.executemany('''
    INSERT INTO EmployeeRequestAssignment (staffNo, requestID, assignmentDate)
    VALUES (?, ?, ?)
''', employee_request_data)

# Queries
queries = [
    "SELECT staffFName, staffLName FROM Employee;",
    "SELECT clientFName, clientLName, clientAddress FROM Client;",
    "SELECT Request.requestID, Request.startDate, Request.startTime, Request.duration, Request.comments, Client.clientFName, Client.clientLName "
    "FROM Request INNER JOIN Client ON Request.clientNo = Client.clientNo;",
    "SELECT RequestEquipmentAssignment.requestID, Equipment.description, Equipment.cost "
    "FROM RequestEquipmentAssignment INNER JOIN Equipment ON RequestEquipmentAssignment.equipmentID = Equipment.equipmentID;",
    "SELECT Employee.staffFName, Employee.staffLName, EmployeeRequestAssignment.assignmentDate "
    "FROM EmployeeRequestAssignment INNER JOIN Employee ON EmployeeRequestAssignment.staffNo = Employee.staffNo;"
]

# Execute and print queries
for index, query in enumerate(queries, 1):
    print(f"Query {index}: {query}")
    cursor.execute(query)
    result = cursor.fetchall()
    print(f"Results {index}:")
    for row in result:
        print(row)
    print("\n")

# Commit changes and close connection
conn.commit()
conn.close()