#!/usr/bin/env python3

import uvicorn

if __name__ == "__main__":
    uvicorn.run("lockbox.debug:app", host="127.0.0.1", port=5000, reload=True)
