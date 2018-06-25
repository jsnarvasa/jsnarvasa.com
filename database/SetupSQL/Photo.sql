CREATE TABLE Photo(
    PhotoID INT NOT NULL AUTO_INCREMENT,
    PhotoFilename VARCHAR(100) NOT NULL,
    PhotoTitle VARCHAR(100) NOT NULL,
    PhotoDescription VARCHAR(3000),
    PhotoUploadDate DATE,
    PhotoDateTaken DATE,
    PRIMARY KEY (PhotoID)
);