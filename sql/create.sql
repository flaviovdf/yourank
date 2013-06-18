CREATE TABLE eval
(
    session_id INTEGER,
    pair_num INTEGER,
    video_id1 TEXT,
    video_id2 TEXT,
    like_choice INTEGER,
    share_choice INTEGER,
    pop_choice INTEGER,
    additional TEXT,
    dateof DATETIME,
    PRIMARY KEY(session_id, pair_num)
);

CREATE TABLE pageloads
(
    session_id INTEGER,
    pair_num INTEGER,
    dateof DATETIME,
    PRIMARY KEY(session_id, pair_num)
);

CREATE TABLE sstate
(
    session_id INTEGER,
    round_rbn INTEGER,
    curr_pair INTEGER,
    PRIMARY KEY(session_id, round_rbn)
);

CREATE TABLE roundrobin
(
    current_round INTEGER,
    total_rounds INTEGER,
    PRIMARY KEY(current_round)
);

CREATE TABLE pairs
(
    round_rbn INTEGER,
    pair_num INTEGER,
    video_id1 TEXT,
    video_id2 TEXT,
    PRIMARY KEY(round_rbn, pair_num)
);

CREATE TABLE userdetails
(
    session_id INTEGER,
    age INTEGER,
    gender INTEGER,
    country TEXT,
    watch_videos INTEGER,
    share_videos INTEGER,
    share_content INTEGER,
    dateof DATETIME,
    PRIMARY KEY(session_id)
);
