-- Makes sure the CASCADE works
PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS Child;
DROP TABLE IF EXISTS Children;
DROP TABLE IF EXISTS Toy;
DROP TABLE IF EXISTS Toys;

CREATE TABLE `Children` (
    `ChildId`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `Name`    TEXT NOT NULL,
    `Delivered`    BIT NOT NULL DEFAULT 0
);

INSERT INTO Children VALUES (null, 'Kiwi', 1);
INSERT INTO Children VALUES (null, 'Olive', 1);
INSERT INTO Children VALUES (null, 'Marcy', 0);

CREATE TABLE `Toys` (
    `ToyId`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `Name`    TEXT NOT NULL,
    'ChildId' INTEGER NOT NULL,
    FOREIGN KEY(`ChildId`) REFERENCES `Children`(`ChildId`)
    ON DELETE cascade
);

INSERT INTO Toys VALUES (null, 'TV Remote', 1);
INSERT INTO Toys VALUES (null, 'Blue Crab', 1);
INSERT INTO Toys VALUES (null, 'Leftover Pizza', 2);
INSERT INTO Toys VALUES (null, 'Dirty Socks', 2);