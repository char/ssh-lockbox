#!/usr/bin/env python3

import uvicorn

if __name__ == "__main__":
    uvicorn.run("ssh_key_authority.debug:app", host="127.0.0.1", port=5000, reload=True)
