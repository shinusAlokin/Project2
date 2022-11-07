
### code refactoring
    - Make Email unique (one person should only create one resume he/she can edit the resume)
    - Try methods to input image
    - Add aditional Phone number field or make phonenumber field an Array with 2 characters
    - url names according to REST principles
    - make more utils
    - Change get basic details to get resume
    - Make an endpoint for basic details
    - Test resume edit more
    - Make delete entity at one time

### Database migrations
    - Use alembic

### Pydantic schema validation
    - Email
    - Phone
    - End date - Start Date should be positive value
    - Character length using Field(..., minlength, maxlength)
    - 
