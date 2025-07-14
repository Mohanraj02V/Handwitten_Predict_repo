# Handwritten Digit Prediction API (Handwritten_Predict_Repo)
1. This repository contains the backend code and documentation for a Handwritten Digit Recognition API, built using Django REST Framework and deployed on Render.
2. # 🌐 Hosted API:
   The project is deployed using Render's free tier.
    API Base URL:
    # https://handwitten-predict-repo.onrender.com/api/
    
   ⚠️ Note: Since this project is hosted on Render's free tier, the server may go to sleep when inactive. The first request after a period of inactivity may take 1–2 minutes to respond. Please be patient and refresh the page if needed.
   
4. # 🚀 How to Use the API
1️⃣ Register a New User
  Use Postman or any REST client to register a user.
  Endpoint:
  # POST https://handwitten-predict-repo.onrender.com/api/register/
  Request Body (JSON):
   {
      "username": "mohanraj",
      "email": "mohanraj@gmail.com",
      "password": "Mohan@10fatedestiny"
   }
   
4. # 2️⃣ Login to Get Authentication Token
    Endpoint:
    # POST https://handwitten-predict-repo.onrender.com/api/login/
    Request Body (JSON):
      {
        "username": "mohanraj",  // required
        "email": "mohanraj@gmail.com",  // optional
        "password": "Mohan@10fatedestiny"  // required
     }
Response:
  You'll receive an authentication token in the response. Copy it for use in the next steps.
  
5. # 3️⃣ Authorize Your Requests
  In Postman:
  1. Go to the Authorization tab
  
  2. Set Type to No Auth
  
  3. Go to the Headers tab
  
  4. Add a new key-value pair:
  
  5. Key: Authorization
  
  6. Value: Token 'your_token_here'
5. # 4️⃣ Predict Handwritten Digit
  # POST https://handwitten-predict-repo.onrender.com/api/predict/
  Instructions:
  
  1. Go to the Body tab in Postman
  
  2. Choose form-data
  
  3. Add a key:
  
  4. Key: image
  
  5. Type: File
  
  6. Value: upload a grayscale image (MNIST-style: black background with white digit)
  
  7. Click Send
6. # 5️⃣ View Prediction History
All Predictions:
  # GET https://handwitten-predict-repo.onrender.com/api/history/
  
  Specific Prediction by ID:
  # GET https://handwitten-predict-repo.onrender.com/api/history/<id>/
  
  Example:
  # GET https://handwitten-predict-repo.onrender.com/api/history/2/
  
## 🧠 Notes
  Only grayscale images similar to MNIST format are supported for accurate predictions.
  
  Ensure correct field names (e.g., image) are used in the request.
  
  API built using PyTorch (CNN), Django REST Framework, and hosted on Render.
