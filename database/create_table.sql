-- Creating the Users table 
CREATE TABLE Users (
     User_ID INT IDENTITY(1,1) PRIMARY KEY, -- Auto-incrementing User ID
    First_Name VARCHAR(50) NOT NULL,             -- First name of the user
    Email VARCHAR(50),                      -- User email
    Created_at DATETIME DEFAULT GETDATE()    -- The date and time the user profile was created 
);


-- Creating the Habits table
CREATE TABLE Habits (
    Habit_ID INT PRIMARY KEY IDENTITY(1,1), -- Habit ID 
    User_ID INT NOT NULL, -- Foreign key that links from the Users table
    Habit_Name_ VARCHAR(100), -- Name of the habit
    Description_ TEXT -- Description of the habit 
	Category VARCHAR(50) -- What category the habit falls in to 
	Frequency VARCHAR(20) -- Frequency the habit is done
	StartDate DATE -- The date the habit started 
	CreatedAt DATETIME DEFAULT GETDATE()-- The date and time that the habit was created within the application 
);


-- Creating the Habit Logs Table
CREATE TABLE Habit_Logs (
    Log_ID INT IDENTITY(1,1) PRIMARY KEY, -- Auto-incrementing Log ID
    Habit_ID VARCHAR(100),             -- Foreign ID to link to Habits table
    Log_Date DATE,                      -- Log date of the Habit
    Habit_Status BIT,                     -- Status code of the Habit
	Note TEXT,                         -- Optional note each time a habit is logged
	logged_At DATETIME DEFAULT GETDATE()-- Example with a default value
);


-- Inserting a test user to check that the Users table is working as it should 
INSERT INTO Users (First_Name, Email)
VALUES ('testuser', 'test@example.com');

--Checking to see if the user has been inputted correctly
SELECT * FROM Users;

-- Inserting a test habit to check that the Habits table is working as it should 
INSERT INTO Habits (User_ID, Habit_Name_, Description_, Category, Frequency, StartDate)
VALUES (1, 'Drink Water', 'Test habit', 'Health', 'Daily', '2025-05-01');

-- Inserting a test Habit Log to check if the Habit log table is working as it should 
SELECT * FROM Habits; -- Finding the Habit ID 

INSERT INTO Habit_Logs (Habit_ID, Log_Date, Habit_Status, Note) -- Inserting test Habit log 
VALUES (1, '2025-05-28', 1, 'Stayed hydrated 💧');

-- Testing JOIN Query 
SELECT u.First_Name, h.Habit_Name_, l.Log_Date, l.Habit_Status
FROM Users u
JOIN Habits h ON u.User_ID = h.User_ID
JOIN Habit_Logs l ON h.Habit_ID = l.Habit_ID;

