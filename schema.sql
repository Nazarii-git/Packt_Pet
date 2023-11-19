

-- Users Table
CREATE TABLE IF NOT EXISTS Users (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT,
    Email TEXT,
    Password TEXT
);

-- Activities or Tasks Table
CREATE TABLE IF NOT EXISTS Activities (
    ActivityID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID INTEGER,
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
    LogID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID INTEGER,
    Date TIMESTAMP,
    DailyPerformanceMetrics DECIMAL(5, 2),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- Activity Log Table (Linking Activities to Daily Logs)
CREATE TABLE IF NOT EXISTS ActivityLog (
    LogID INTEGER,
    ActivityID INTEGER,
    TimeSpent DECIMAL(5, 2),
    FOREIGN KEY (LogID) REFERENCES DailyLogs(LogID),
    FOREIGN KEY (ActivityID) REFERENCES Activities(ActivityID)
);
