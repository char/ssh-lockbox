# ssh-key-authority

A centralised location for your personal SSH keys.

Supports:

- [GitHub](https://github.com/)
- [GitLab](https://gitlab.com/)
- [Gogs](https://gogs.io/) and [Gitea](https://gitea.io/)
- Any `sshd` with an `AuthorizedKeysCommand` configuration directive

## Usage

```
$ # set up a virtualenv, or don't, your choice. then:
$ pip install -r requirements.txt
$ cp .env.schema .env; $EDITOR .env # Set up the DATABASE_URL value
$ alembic upgrade head # Run migrations to initialise the database
$ ./run_prod.sh ./ssh-key-authority.sock # Starts a gunicorn instance (with a uvicorn worker) listening at unix:./ssh-key-authority.sock
$ # Use nginx to proxy into the socket
```

## Details

Without authentication, keys are publicised without comment fields, à la GitHub's `https://github.com/<user>.keys` route.

With authentication, it is possible to access the keys with the comment field intact.

## Configuration

Configuration can be achieved via a `.env` file or through environment variables.

The configuration entries are as follows:

- `DATABASE_URL`: A connection URL for the application's database. A configuration (using SQLite) for development is included in `.env.schema`.
- `SESSION_SECRET_KEY`: The secret key to sign session information with. This should be a randomly generated blob of data.
- `REGISTRATION_ENABLED`: Whether to permit arbitrary user registration.
