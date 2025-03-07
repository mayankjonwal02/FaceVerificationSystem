### API Documentation

#### Base URL
- **Base URL**: `http://yourdomain.com/`
- **Port**: `8003`

#### Endpoints

1. **Register User**
   - **URL**: `/register/`
   - **Method**: `POST`
   - **Description**: Registers a new user with an image.
   - **Request Body**:
     ```json
     {
       "id": "string",  // User ID
       "image": "file", // Image file
       "imagetype": "string" // "clicked" or "scanned"
     }
     ```
   - **Response**:
     - **Success**: 
       ```json
       {
         "message": "Data inserted successfully"
       }
       ```
     - **Error**:
       ```json
       {
         "error": "string"
       }
       ```

2. **Verify User**
   - **URL**: `/verify/`
   - **Method**: `POST`
   - **Description**: Verifies a user by checking the uploaded image.
   - **Request Body**:
     ```json
     {
       "image": "file" // Image file
     }
     ```
   - **Response**:
     - **Success**:
       ```json
       {
         "message": "Image received successfully!",
         "recognition": "string",
         "verified": true
       }
       ```
     - **Error**:
       ```json
       {
         "error": "string",
         "verified": false
       }
       ```

3. **Delete User**
   - **URL**: `/register/`
   - **Method**: `DELETE`
   - **Description**: Deletes a user and associated images.
   - **Request Body**:
     ```json
     {
       "id": "string" // User ID
     }
     ```
   - **Response**:
     - **Success**:
       ```json
       {
         "message": "Data deleted successfully",
         "files_deleted": ["string"]
       }
       ```
     - **Error**:
       ```json
       {
         "error": "string"
       }
       ```

4. **Developed By Page**
   - **URL**: `/developedby/`
   - **Method**: `GET`
   - **Description**: Displays the "Developed By" page.
   - **Response**: HTML page

5. **Registration Page**
   - **URL**: `/registerPage/`
   - **Method**: `GET`
   - **Description**: Displays the registration page.
   - **Response**: HTML page

6. **Verification Page**
   - **URL**: `/verifyPage/`
   - **Method**: `GET`
   - **Description**: Displays the verification page.
   - **Response**: HTML page

### Notes
- Ensure that the `Content-Type` for file uploads is set to `multipart/form-data`.
- The `imagetype` field in the registration endpoint should be either `"clicked"` or `"scanned"`.
- The `id` field is required for both registration and deletion of users.

