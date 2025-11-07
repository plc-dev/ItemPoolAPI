# Item Pool API

## Dev-Setup

1. **Install dependencies**

   - [Python Installation Guide](https://wiki.python.org/moin/BeginnersGuide/Download)
   - [uv Installation Guide](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer)
   - [Docker Installation Guide](https://docs.docker.com/engine/install/)

2. **Start mongoDB via Docker**
   Start docker daemon if not already started. Then run the following cmd in a shell.

   ```bash
   docker-compose up
   ```

3. **Start API**
   Run this cmd in a shell in the project root repository:
   ```bash
   uv run fastapi dev src/main.py
   ```

## **Tests**

### **Manual API Tests**

    Manual API tests are implemented via HTTP Files in the "tests" directory.
    When using VSCode as an IDE, the REST Client extension is recommended.

### **Unit Tests**

TBD

## Feature-List

See this [wiki-entry](https://github.com/plc-dev/ItemPoolAPI/wiki/ToDo%E2%80%90List).
