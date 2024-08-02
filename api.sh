#!/bin/bash

# curl -X POST -H "Content-Type: multipart/form-data" \
#   -F "images=@./svelte-app/src/lib/assets/IMG_3284.jpg" \
#   -F "images=@./svelte-app/src/lib/assets/IMG_4841.webp" \
#   http://localhost:8000/api/async/upload

# curl -X POST \
#   -H "Accept: application/json" \
#   -F "images=@./svelte-app/src/lib/assets/IMG_3284.jpg" \
#   -F "images=@./svelte-app/src/lib/assets/IMG_4841.webp" \
#   http://localhost:8000/api/async/upload

curl -X POST \
  -H "Accept: application/json" \
  -F "image=@./svelte-app/src/lib/assets/IMG_4841.webp" \
  http://localhost:8000/api/upload