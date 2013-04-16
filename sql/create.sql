CREATE TABLE eval
(
    id INTEGER PRIMARY KEY,
    session_id INTEGER,
    pair_id INTEGER,
    video_id1 TEXT,
    video_id2 TEXT,
    like_choice INTEGER,
    share_choice INTEGER,
    pop_choice INTEGER,
    additional TEXT,
    dateof DATETIME
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

CREATE TABLE userdetails;
(
    id INTEGER PRIMARY KEY,
    age INTEGER,
    gender INTEGER,
    country TEXT,
    watch_videos INTEGER,
    share_videos INTEGER,
    share_content INTEGER,
    dateof DATETIME
);
