CREATE TABLE IF NOT EXISTS messages (
 message_id integer PRIMARY KEY AUTOINCREMENT,
 timestamp long,
 message text NOT NULL
);
