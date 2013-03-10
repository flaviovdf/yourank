CREATE TABLE eval
(
    id INTEGER PRIMARY KEY,
    video_id1 TEXT,
    video_id2 TEXT,
    choice INTEGER,
    additional TEXT
);

CREATE TABLE sstate
(
    id INTEGER PRIMARY KEY,
    curr_pair INTEGER
);

CREATE TABLE pairs
(
    pair_num INTEGER PRIMARY KEY,
    video_id1 TEXT,
    video_id2 TEXT
);
