# Database

FROM postgres:15

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=taller3

COPY init.sql /docker-entrypoint-initdb.d/
COPY schema.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
