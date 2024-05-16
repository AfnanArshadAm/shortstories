# FastAPI, Supabase, and OpenAI Integration

This project demonstrates a simple FastAPI application that integrates with Supabase for database operations and OpenAI for generating short stories based on character details.

* Create a Character

Endpoint**: `/api/create_character`

Method**: `POST`

Description**: Create a new character.

Request:
`curl -X POST "http://localhost:8000/api/create_character" \
     -H "Content-Type: application/json" \
     -d '{"name": "Bilbo Baggins", "detail": "A hobbit who lives in the Shire and owns a magic ring"}'`

* Generate a Story

Endpoint: `/api/generate_story`

Method: `POST`

Description: Generate a story based on a character.

Request:
`curl -X POST "http://localhost:8000/api/generate_story" \
     -H "Content-Type: application/json" \
     -d '{"character_name": "Bilbo Baggins"}'`
