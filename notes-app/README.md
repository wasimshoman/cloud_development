# Notes App

A serverless REST API for managing notes, built with AWS Lambda, API Gateway, DynamoDB, and EventBridge.

## Tech Stack

- **AWS Lambda** — Python 3.9 functions, one per route
- **API Gateway** — HTTP API that routes requests to the right function
- **DynamoDB** — persistent storage for notes
- **EventBridge** — event-driven logging triggered automatically in the background
- **Serverless Framework** — deploys all infrastructure with a single command

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/notes` | Create a new note |
| GET | `/notes` | Get all notes |
| GET | `/notes/{id}` | Get a single note |
| PUT | `/notes/{id}` | Update a note |
| DELETE | `/notes/{id}` | Delete a note |

## Deploy

```bash
serverless deploy
```

## Remove

```bash
serverless remove
```

## Example Request

Create a note:
```json
POST /notes
{
  "title": "My Note",
  "content": "This is the note content"
}
```

Response:
```json
{
  "message": "Note created",
  "id": "abc-123"
}
```
