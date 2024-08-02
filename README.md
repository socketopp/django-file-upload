# dbtune-code-assignment

This project consists of a Django server for image processing and a Svelte frontend application. It allows users to upload images, process them asynchronously, and view the uploaded images.

## Project Structure

- `django_server/`: Django backend application
- `svelte_app/`: Svelte frontend application
- `docker-compose.yml`: Docker Compose configuration file

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. Clone the repository:
   ```
   git clone https://github.com/socketopp/dbtune-code-assignment.git
   cd dbtune-code-assignment
   ```

2. Build and start the Docker containers:
   ```
   docker compose up --build
   ```

   This command will build the images and start the containers for the Django server, Svelte app, and PostgreSQL database.

3. Access the applications:
   - Django Admin: http://localhost:8000/admin
   - Svelte App: http://localhost:5173

## API Documentation

### Base URL
`http://localhost:8000/api`

### API Endpoints

1. **Upload Image (Synchronous)**
   - URL: `/upload`
   - Method: POST
   - Description: Upload a single image file
   - Request Body: Form-data with 'image' field
   - Response:
     ```json
     {
      "message": "Image uploaded successfully"
     }
     ```
   - Curl example:
     ```
      curl -X POST \
        -H "Accept: application/json" \
        -F "image=@./svelte-app/src/lib/assets/IMG_4841.webp" \
        http://localhost:8000/api/upload
     ```

2. **Upload Images (Asynchronous)**
   - URL: `/async/upload`
   - Method: POST
   - Description: Upload multiple image files for asynchronous processing
   - Request Body: Form-data with 'images' field (can contain multiple files)
   - Response:
     ```json
 
       {
        "message": "Images upload initiated"
       }

     ```
   - Curl example (multiple files):
     ```
      curl -X POST \
        -H "Accept: application/json" \
        -F "images=@./svelte-app/src/lib/assets/IMG_3284.jpg" \
        -F "images=@./svelte-app/src/lib/assets/IMG_4841.webp" \
        http://localhost:8000/api/async/upload
     ```

3. **List Images**
   - URL: `/list`
   - Method: GET
   - Description: Retrieve a list of all uploaded images
   - Response:
     ```json
     [
       {
         "id": "uuid",
         "name": "image1.jpg",
         "size": 12345,
         "uploaded_at": "2024-08-02T12:34:56Z",
         "status": "completed"
       },
       ...
     ]
     ```
   - Curl example:
     ```
     curl http://localhost:8000/api/list
     ```

  ### Error Codes
      - 400 Bad Request: Invalid input or missing required fields
      - 404 Not Found: Requested resource not found
      - 500 Internal Server Error: Server-side error occurred

      ### WebSocket Connection
      - URL: `ws://localhost:8000/ws/upload/`
      - Description: Provides real-time updates on asynchronous image uploads
      - Message format:
        ```json
        {
          "type": "send_upload_notification",
          "job_id": "uuid",
          "status": "completed",
          "image": "/media/images/processed_image.jpg"
        }
        ``` 

## Development

### Rebuilding and Restarting Containers

To rebuild and restart a specific container (e.g., svelte_app):

   ```
   docker compose stop svelte_app && docker compose rm -f svelte_app && docker compose build svelte_app && docker compose up -d svelte_app
   ```

### In case django_server experiences issues with daphne

If docker is not properly shut down, daphne doesn't release lock on /tmp/daphne.sock, you'll need to take down docker and remove orphans. 

`CRITICAL Listen failure: Couldn't listen on any:b'/tmp/daphne.sock': Cannot acquire lock.`
   ```
   docker-compose down --volumes --remove-orphans
   ```

### How to delete images?
   ```
   # connect to db
   docker exec -it db psql -U admin -d image-db
   # delete images
   DELETE FROM images;
   ```
