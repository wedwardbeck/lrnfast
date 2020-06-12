SELECT 'CREATE DATABASE lrnfast'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'lrnfast')\gexec