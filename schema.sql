

-- Users Table
CREATE TABLE IF NOT EXISTS Users (
    UserID TEXT PRIMARY KEY,
    Username TEXT,
    Email TEXT,
    Password TEXT
);

-- Activities or Tasks Table
CREATE TABLE IF NOT EXISTS Activities (
    ActivityID TEXT PRIMARY KEY,
    UserID TEXT,
    ActivityName TEXT,
    Description TEXT,
    Category TEXT,
    Repeats INTEGER,
    Points INTEGER,
    Time TIMESTAMP,
    Duration INTEGER,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- Daily Logs Table
CREATE TABLE IF NOT EXISTS DailyLogs (
    LogID TEXT PRIMARY KEY,
    UserID TEXT,
    Date TIMESTAMP,
    DailyPerformanceMetrics DECIMAL(5, 2),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- Activity Log Table (Linking Activities to Daily Logs)
CREATE TABLE IF NOT EXISTS ActivityLog (
    LogID TEXT PRIMARY KEY,
    DailyLogID TIMESTAMP,
    ActivityID TEXT,
    Time TIMESTAMP,
    TimeSpent DECIMAL(5, 2),
    FOREIGN KEY (DailyLogID) REFERENCES DailyLogs(Date),
    FOREIGN KEY (ActivityID) REFERENCES Activities(ActivityID)

);
