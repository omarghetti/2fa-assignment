## 2FA AUTHENTICATION

This is a demo project of an implementation of a 2FA Authentication Flow

To run the project, build the .Dockerfile in the repository and then run the command

      docker run --name [container_name]  -p 80:80  2faassignment:latest

## PROJECT STRUCTURE
The API has 3 Different Endpoints:

  /register: with this endpoint it's is possibile to register a user into the database. if the flag for 2FA is enabled, 
  an otp_secret is created via the pyOTP library. password is hashed
  
  /login: this endpoint authenticate the user checking if email and password are correct, rasing an exception with HTTP401 status if there are 
  incongruences in those values. if the values are correct and the user has the enable_2fa flag on FALSE, the endpoint return a JWT token followed by an expiration date
  
  /verify: if the user has enable_2fa flag on TRUE, the /login endpoint produces an otp code that, for experimental reasons, is printed out on the stdout.
  this endpoint enables to check the otp and to then get back a JWT followed by an expiration date
  
