-- noinspection SqlNoDataSourceInspectionForFile

CREATE TABLE IF NOT EXISTS player (
    discord_id INTEGER PRIMARY KEY,
    mmr INTEGER NOT NULL
);