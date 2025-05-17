# Sampader — Backend Refactor (Service Layer + Async)

This branch is a major restructuring of the backend of the **Sampader** social network project.

The goal is to refactor the architecture to be **modular**, **asynchronous**, and **scalable** by moving from a traditional Flask-based structure to a more robust **Service Layer Architecture** using the **Quart** framework.

---

## What's different in this branch?

- **Asynchronous Framework**: Replacing Flask with [Quart](https://pgjones.gitlab.io/quart/) for native async/await support.
- **Service Layer Architecture**: Business logic is moved to separate service modules, making the codebase more modular and easier to test and maintain.
- **Cleaner Separation of Concerns**: Routes (controllers), services (logic), and data models (SQLAlchemy) are clearly separated.
- **Improved Scalability**: Laying the foundation for future improvements like background tasks, async DB access, WebSocket support, etc.

---

## Project Structure

```
Sampader/
├── app/
│    ├── api/
│    ├── core/
│    ├── models/
│    ├── repositories/
│    ├── schemas/
│    ├── services/
│    ├── main.py
├── log/
├── uploads/
├── requirements.txt
├── README.md
```

---

## Getting Started

.

---

## Current Status

This branch is **under active development**. It is not yet stable or feature-complete. Expect frequent structural changes.

If you're looking for the previous stable version, check the [`main`](https://github.com/ah-afshin/Sampader/tree/main) branch.

---

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
