CREATE TABLE IF NOT EXISTS Player (
    discord_id INTEGER NOT NULL,
    mmr INTEGER NOT NULL,
    PRIMARY KEY (discord_id)
);