-- Table: user
CREATE TABLE "user" (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    gender CHAR(1) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone CHAR(10) NOT NULL UNIQUE,
    password VARCHAR(75) NOT NULL
);

-- Table: shelter (without foreign key constraint to employee)
CREATE TABLE shelter (
    shelter_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    address VARCHAR(50) NOT NULL,
    phone CHAR(10) NOT NULL,
    capacity INT NOT NULL,
    manager_id INT -- Removed NOT NULL constraint for now
    -- Foreign key constraint will be added later
);

-- Table: employee (without foreign key constraint to shelter)
CREATE TABLE employee (
    employee_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    gender CHAR NOT NULL,
    position VARCHAR(50),
    phone CHAR(10),
    password VARCHAR(75),
    shelter_id INT
    -- Foreign key constraint will be added later
);

-- Table: animal
CREATE TABLE animal (
    animal_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    species VARCHAR(50) NOT NULL,
    breed VARCHAR(50),
    size CHAR(2),
    death_time TIMESTAMP,
    adoption_status CHAR(50) NOT NULL,
    leave_at TIMESTAMP,
    arrived_at TIMESTAMP,
    is_sterilized BOOLEAN,
    sex CHAR,
    shelter_id INT NOT NULL,
    CONSTRAINT fk_shelter FOREIGN KEY (shelter_id)
        REFERENCES shelter(shelter_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- Table: activity
CREATE TABLE activity (
    activity_id SERIAL PRIMARY KEY,
    time TIMESTAMP,
    location VARCHAR(255),
    activity_type CHAR(1) NOT NULL,
    capacity INT,
    shelter_id INT NOT NULL,
    CONSTRAINT fk_shelter_activity FOREIGN KEY (shelter_id)
        REFERENCES shelter(shelter_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- Table: application
CREATE TABLE application (
    application_id SERIAL PRIMARY KEY,
    update_at TIMESTAMP NOT NULL,
    status CHAR(1) NOT NULL,
    user_id INT NOT NULL,
    animal_id INT NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY (user_id)
        REFERENCES "user"(user_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    CONSTRAINT fk_animal_application FOREIGN KEY (animal_id)
        REFERENCES animal(animal_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- Table: care_record
CREATE TABLE care_record (
    animal_id INT NOT NULL,
    employee_id INT NOT NULL,
    care_type CHAR(1) NOT NULL,
    start_at TIMESTAMP NOT NULL,
    end_at TIMESTAMP,
    PRIMARY KEY (animal_id, employee_id, start_at),
    CONSTRAINT fk_animal_care FOREIGN KEY (animal_id)
        REFERENCES animal(animal_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- Table: medical_record
CREATE TABLE medical_record (
    animal_id INT NOT NULL,
    employee_id INT NOT NULL,
    time TIMESTAMP NOT NULL,
    hospital VARCHAR(50),
    reason TEXT,
    item TEXT NOT NULL,
    cost INT,
    PRIMARY KEY (animal_id, employee_id, time),
    CONSTRAINT fk_animal FOREIGN KEY (animal_id)
        REFERENCES animal(animal_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
    -- Foreign key constraint for employee will be added later
);

-- Table: punch
CREATE TABLE punch (
    employee_id INT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    punch_type CHAR NOT NULL,
    PRIMARY KEY (employee_id, created_at)
    -- Foreign key constraint will be added later
);

-- Table: registration
CREATE TABLE registration (
    user_id INT NOT NULL,
    activity_id INT NOT NULL,
    status CHAR NOT NULL,
    PRIMARY KEY (user_id, activity_id),
    CONSTRAINT fk_user_registration FOREIGN KEY (user_id)
        REFERENCES "user"(user_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    CONSTRAINT fk_activity FOREIGN KEY (activity_id)
        REFERENCES activity(activity_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);


-- Add foreign key constraint to employee for shelter_id
ALTER TABLE employee
ADD CONSTRAINT fk_shelter_employee FOREIGN KEY (shelter_id)
    REFERENCES shelter(shelter_id)
    ON DELETE SET NULL
    ON UPDATE CASCADE;

-- Add foreign key constraint to shelter for manager_id
ALTER TABLE shelter
ADD CONSTRAINT fk_manager FOREIGN KEY (manager_id)
    REFERENCES employee(employee_id)
    ON DELETE SET NULL
    ON UPDATE CASCADE;

-- Add foreign key constraint to care_record for employee_id
ALTER TABLE care_record
ADD CONSTRAINT fk_employee_care FOREIGN KEY (employee_id)
    REFERENCES employee(employee_id)
    ON DELETE SET NULL
    ON UPDATE CASCADE;

-- Add foreign key constraint to medical_record for employee_id
ALTER TABLE medical_record
ADD CONSTRAINT fk_employee FOREIGN KEY (employee_id)
    REFERENCES employee(employee_id)
    ON DELETE SET NULL
    ON UPDATE CASCADE;

-- Add foreign key constraint to punch for employee_id
ALTER TABLE punch
ADD CONSTRAINT fk_employee_punch FOREIGN KEY (employee_id)
    REFERENCES employee(employee_id)
    ON DELETE SET NULL
    ON UPDATE CASCADE;
