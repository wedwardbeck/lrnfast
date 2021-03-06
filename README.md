# FastAPI CRUD using Async, Alembic & Postgresql

<p>
  <img alt="Version" src="https://img.shields.io/badge/version-0.3.0-blue.svg?cacheSeconds=2592000" />
</p>

> Example Async CRUD API using FastAPI

This repository is the result of wading through how to use async CRUD operations 
using the backend core from the excellent generator template by Sebastián Ramírez, 
[Full Stack FastAPI and PostgreSQL - Base Project Generator][tiangolo/fullstack].

In reviewing [the FastAPI docs][fastapidocs], the [encode/databases docs][databases-queries]
on queries, and the gitter channels, there seemed to be only the basic 
information on using databases with SQL Alchemy and data table 
definitions that would not work well with Alembic autogenerate - as least in 
my case using the generator template.  This repository is the working result
of my tests and learning to use FastAPU with async, asycnpg, databases, and Alembic 
autogenerated migrations with declarative base model.  Hopefully it will be useful 
to others looking for some examples of using databases, asyncpg and Alembic with FastAPI.

## Updates
**Version 0.3.0** Dockerfiles & Docker-Compose ready containing two services, PSQL & APP.
* **PSQL** - Postgresql 12-alpine image.
* **APP** - ClearLinux/Python3.8 image with custom build.
* **Auto Migrations** - Migrations including creation of stored procedures in APP image.
* **.env Sample** - Change to .env and provide desired values.

## Details

* **Uses version 0.4.0 of the [Fullstack generator][tiangolo/fullstack-v4]**: 
before current changes in structure of the project were made.
* **[encode/databases][databases-queries]**: To simplify managing connections, pooling, etc.   
* **asyncpg with Posgresql**: Built using a Postgresql 12 database, but can be altered to use SQLite.
* **[Alembic][alembic]**: Using autogenerate to create migrations. 
* **Version 0.1.0**: Uses raw SQL in CRUD functions.  See tag v0.1.0.
* **Version 0.2.0**: Uses functions (reads) and procedures (write).  ***Procedures require Posgresql Version 11 or higher.***
* **Version 0.3.0**: Uses Docker-Compose to spin up services and run migrations.

### Critical Notes
* PyCharm (or other IDE) may complain about the PSQL Procedures using "CALL" - I just injected SQL lanuage on the query text to eliminate the errors.  
* Some CRUD functions utilize `databases.fetch_val()` and require using the latest master branch of databases from the repo.  The version on PyPi is not correct, and is missing the April 30 commit with the required changes to use this.  See [this commit](https://github.com/encode/databases/commit/25e65edc369f6f016fab9e4156bdbf628a107fa7).
* Clone the [encode/databases] repo into the "backend" folder before running docker-compose up --build. 
* If not patching or using the current repo from PyPi (says 0.3.2 but really is <=0.3.1)- `databases.fetch_one()` needs to be used or the get by ID and create routes will fail.  

## Installation Instructions 
* Clone the repo.
* Clone the [encode/databases] repo into the "backend" folder.
* Change the sample.env file to .env and enter your preferred values.  
* Run Docker Compose (with -d for detached, or omit to run in foreground):
```
$ docker-compose up --build
```
* In the browser, go to localhost:8000/docs
* Login using the super user email and password supplied in the .env file.  
* Test routes. 
* When done:
```
$ docker-compose down
```
You can rerun the docker-compose up and the datbase data will be persistent.  

You can also remove the named volume where the database data resides by adding the -v flag:
```
$ docker-compoise down -v
```

## To Do

Tests, deployment via docker, and other changes to come, time permitting.
Want to see these sooner - see below in [Contributing][learnfast-contrib].

## Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/wedwardbeck/lrnfast/issues).
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/YourFeature`)
3. Commit your Changes (`git commit -m 'Add My Feature'`)
4. Push to the Branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

## Contact

#### Edward Beck

- Twitter: [@wedwardbeck](https://twitter.com/wedwardbeck)
- Github: [@wedwardbeck](https://github.com/wedwardbeck)

## License

This project is licensed under the terms of the MIT license.

---
[tiangolo/fullstack]: https://github.com/tiangolo/full-stack-fastapi-postgresql
[tiangolo/fullstack-v4]: https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/0.4.0
[fastapidocs]: https://fastapi.tiangolo.com/
[databases-queries]: https://www.encode.io/databases/database_queries/#queries
[databases]: https://www.encode.io/databases/database_queries/#queries
[alembic]: https://github.com/sqlalchemy/alembic
[learnfast]: https://github.com/wedwardbeck/lrnfast
[learnfast-contrib]: https://github.com/wedwardbeck/lrnfast#contributing
