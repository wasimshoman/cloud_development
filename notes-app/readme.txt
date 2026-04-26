
how to run this api
  ---
  Step 1 — Open Thunder Client
  Click the lightning bolt icon on the left sidebar in VS Code.

  Step 2 — Create your first note
  1. Click New Request
  2. Change the method from GET to POST (dropdown on the left)
  3. Paste this URL:
  https://vg3pvmuaoc.execute-api.us-east-1.amazonaws.com/notes
  4. Click the Body tab → select JSON
  5. Paste this in the box:
  {
    "title": "My First Note",
    "content": "Hello from the notes app!"
  }
  6. Click Send

  You should get back a response with your note and an id. Copy that id — you'll need it for the other requests.

  ---
  Step 3 — Get all notes
  1. New Request → method GET
  2. Same URL: https://vg3pvmuaoc.execute-api.us-east-1.amazonaws.com/notes
  3. Click Send — you'll see all your notes listed

  ---
  Step 4 — Get, Update, or Delete one note

  Use the same URL but add the id at the end:
  https://vg3pvmuaoc.execute-api.us-east-1.amazonaws.com/notes/PASTE-ID-HERE
  - GET → fetch that note
  - PUT + Body JSON → update it
  - DELETE → delete it




    1. Serverless app deployed to AWS

  Configured in serverless.yml:
  service: notes-app
  provider:
    name: aws
    runtime: python3.9
    region: us-east-1
  Deployed and live at https://vg3pvmuaoc.execute-api.us-east-1.amazonaws.com


  2. API Gateway with 5 routes

  From serverless.yml:
  POST   /notes        ← create a note
  GET    /notes        ← get all notes
  GET    /notes/{id}   ← get one note
  PUT    /notes/{id}   ← update a note
  DELETE /notes/{id}   ← delete a note


  3. Each route has its own Lambda function

  ┌────────────────────┬──────────────────────────┐
  │       Route        │      Function file       │
  ├────────────────────┼──────────────────────────┤
  │ POST /notes        │ functions/createNote.py  │
  ├────────────────────┼──────────────────────────┤
  │ GET /notes         │ functions/getAllNotes.py  │
  ├────────────────────┼──────────────────────────┤
  │ GET /notes/{id}    │ functions/getNote.py      │
  ├────────────────────┼──────────────────────────┤
  │ PUT /notes/{id}    │ functions/updateNote.py  │
  ├────────────────────┼──────────────────────────┤
  │ DELETE /notes/{id} │ functions/deleteNote.py  │
  └────────────────────┴──────────────────────────┘


  4. Persistent data in DynamoDB

  Every function reads/writes to notes-table. Example from createNote.py:
  table.put_item(Item={
      'id': note_id,
      'title': body['title'],
      'content': body['content'],
      'createdAt': datetime.utcnow().isoformat()
  })


-
  5. Event-driven function with EventBridge ✅

  functions/logEvent.py is triggered automatically by EventBridge whenever something happens in your app:
  def handler(event, context):
      print("Event received from EventBridge:")
      print(json.dumps(event, indent=2))
  Configured in serverless.yml:
  logEvent:
    handler: functions/logEvent.handler
    events:
      - eventBridge:
          eventBus: default
          pattern:
            source:
              - notes-app




The Serverless Framework read your serverless.yml and automatically created everything in AWS for you.

  It did this using something called AWS CloudFormation — a service that reads a config file and builds AWS resources automatically. You never had to click anything in AWS.

  Here's what got created:

  ---
  1. AWS Lambda — your functions

  Each .py file became a Lambda function in AWS. You can see them here:

  ▎ AWS Console → Lambda → Functions

  You'll see: notes-app-dev-createNote, notes-app-dev-getAllNotes, etc.

  ---
  2. API Gateway — your URL

  Serverless created an HTTP API in API Gateway and connected each route (/notes, /notes/{id}) to the matching Lambda function.

  AWS then automatically generated that URL for you:
  https://vg3pvmuaoc.execute-api.us-east-1.amazonaws.com
  The vg3pvmuaoc part is a random ID AWS assigns. You can see it here:

  ▎ AWS Console → API Gateway → notes-app-dev

  ---
  3. DynamoDB — your database

  Serverless created the notes-table table. You can see it here:

  ▎ AWS Console → DynamoDB → Tables → notes-table

  Every note you create gets stored as a row there.

  ---
  4. EventBridge — your log trigger

  Serverless created a rule on EventBridge that watches for events from source notes-app and triggers your logEvent Lambda automatically.

  ▎ AWS Console → EventBridge → Rules

  ---
  In short: you wrote serverless.yml, ran one command, and Serverless Framework built all of this in AWS automatically. That's the whole point of serverless — no manual setup.
