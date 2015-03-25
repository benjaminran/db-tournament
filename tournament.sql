-- Table definitions for the tournament project.
--
-- usage: psql <tournament.sql
--

create database tournaments;
\c tournaments

create table if not exists rounds (id serial primary key, round smallint, mid integer);
create table if not exists matches (mid serial primary key, pid1 integer, pid2 integer, winner integer);
create table if not exists players (pid serial primary key, name text, wins smallint, losses smallint, matches integer);
