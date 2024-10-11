# django-file-upload

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
   git clone https://github.com/socketopp/django-file-upload.git
   cd django-file-upload
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
   - URL: `/api/upload`
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
   - URL: `/api/async/upload`
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

3. **Upload Images (Batch)**
   - URL: `/api/async/batch/upload`
   - Method: POST
   - Description: Upload multiple image files for batch processing
   - Request Body: Form-data with 'images' field (can contain multiple files)
   - Response:
     ```json
     {
      "message": "Batch upload of N images initiated"
     }
     ```
   - Curl example (multiple files):
     ```
     curl -X POST \
       -H "Accept: application/json" \
       -F "images=@./svelte-app/src/lib/assets/IMG_3284.jpg" \
       -F "images=@./svelte-app/src/lib/assets/IMG_4841.webp" \
       http://localhost:8000/api/async/batch/upload
     ```

4. **List Images**
   - URL: `/api/list`
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
       ...,N
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


# Improvements from Batch Processing and Bulk Database Operations

The improvement from implementing batch processing and bulk database operations can be significant, especially as the number of concurrent uploads increases. Let's break down the potential improvements:

## Database Operations

## Before:
- For N images, we're performing N individual INSERT operations and N individual UPDATE operations.

## After:
- 1 bulk INSERT operation for N images
- 1 bulk UPDATE operation for N images

**Improvement:** This could reduce database write operations by up to 2N-2 for N images. For example, with 100 images, we go from 200 database operations to just 2.

## Task Processing

### Before:
- N separate Celery tasks were created and processed for N images.

### After:
- 1 Celery task processing N images.

**Improvement:** This reduces the overhead of task creation, queuing, and worker assignment by a factor of N. It also allows for more efficient use of worker resources.

## Memory Usage

While processing images in batches might use more memory per task, it reduces the overall memory footprint across multiple workers. This can lead to better resource utilization, especially on systems with limited memory.

## Network Traffic

Reduced network traffic between application server, task queue, and database due to fewer individual operations.

## Quantitative Estimates

While exact improvements depend on specific hardware, network, and database configuration, here are some rough estimates:

- For small batches (5-10 images): We might see a 20-40% improvement in processing time.
- For medium batches (20-50 images): Improvements could range from 40-60%.
- For large batches (100+ images): We could see improvements of 60-80% or more.

## Real-world Example

Let's consider a scenario with 100 image uploads:

### Before optimization:
- 100 database INSERTs + 100 database UPDATEs = 200 database operations
- 100 Celery tasks created and processed

### After optimization:
- 1 bulk INSERT + 1 bulk UPDATE = 2 database operations
- 1 Celery task processing all 100 images

In this case, we've reduced database operations by 99% and Celery task overhead by 99%. The actual time savings would depend on our system's bottlenecks, but it's not uncommon to see processing time reduced by 70-80% in such scenarios.

## Additional Benefits

1. **Scalability:** This approach scales much better as the number of concurrent uploads increases.
2. **Reduced Server Load:** Fewer individual operations mean less CPU and I/O overhead on our servers.
3. **Improved Responsiveness:** By reducing the overall system load, our application can remain more responsive to other requests.

## Caveats

1. **Very Large Batches:** If batches become too large, we might need to implement pagination or chunking to avoid memory issues.
2. **Error Handling:** With batch processing, we'll need robust error handling to manage partial failures within a batch.
3. **Real-time Updates:** While this approach still allows for real-time updates via WebSockets, the updates for individual images within a large batch might be slightly delayed.


## Experiments

    ```
    200 pictures:
    async-log: 7.030s
    async-log-batch: 1.987s

    300 pictures
    async-log: 6.906s
    async-log-batch: 2.590s

    1000 pictures:
    async-log: 24.677s
    async-log-batch: 10.489s
    ```

# Additional possible improvements

-  Implement database connection pooling, such as PgBouncer for PostgreSQL connection pooling

-  Implement message queuing for WebSocket broadcasts, use Redis as a message queue for WebSocket broadcasts

- Implement a load balancer for distributing incoming request, use Nginx as a simple load balance for multiple django instances.

- Implement horizontal scaling for Celery, besides Django, we can run multiple Celery worker and then test with a lot of images with similar script:

  ```
    import asyncio
    import aiohttp

    async def upload_image(session, url, image_path):
        async with session.post(url, data={'image': open(image_path, 'rb')}) as response:
            return await response.json()

    async def main():
        url = 'http://localhost/api/upload'  # Your upload endpoint
        image_path = 'path/to/test/image.jpg'
        
        async with aiohttp.ClientSession() as session:
            tasks = [upload_image(session, url, image_path) for _ in range(1000)]
            results = await asyncio.gather(*tasks)
        
        print(f"Uploaded {len(results)} images")

    if __name__ == '__main__':
        asyncio.run(main())
  ```

