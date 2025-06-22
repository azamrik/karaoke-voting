CREATE TABLE IF NOT EXISTS EVENT (
    id serial,
    event_name VARCHAR(255) UNIQUE,
    event_date DATE,
    nomination_end_timestamp TIMESTAMP,
    voting_end_timestamp TIMESTAMP,
    song_nomination_limit INT,
    lock_voter_domain BOOLEAN,
    required_domain VARCHAR(255),
    song_delay TIME
);

CREATE TABLE IF NOT EXISTS event_admins (
    id serial,
    event_id int,
    user_id varchar(1000),
    -- TODO: Consider making permission an enum
    user_permission varchar(255)
);

