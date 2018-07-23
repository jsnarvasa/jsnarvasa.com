CREATE TABLE Photos (
    PhotoID INT NOT NULL AUTO_INCREMENT,
    FileName VARCHAR(100) NOT NULL,
    Caption VARCHAR(5000) NOT NULL,
    Upload_Date DATE NOT NULL,
    Capture_Date DATE,
    Place VARCHAR(150),
    City VARCHAR(150),
    Country VARCHAR(150),
    PRIMARY KEY (PhotoID)
);