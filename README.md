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
$ ./run_prod.sh ./ssh-key-authority.sock # Starts a Hypercorn instance listening at unix:./ssh-key-authority.sock
$ # Set up nginx to proxy into the unix socket
```

## Details

Without authentication, keys are publicised without comment fields, à la GitHub's `https://github.com/<user>.keys` route.

With authentication, it is possible to access the keys with the comment field intact.