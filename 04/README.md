# Exercise 04 - Express Users API

This document describes how the solution for Exercise 04 can be tested.

All the commands described below must be executed within the folder with the source files (`04`).

----

## 1. Node version

The solution was developed using Node v16.17.0. If you're using [nvm](https://github.com/nvm-sh/nvm), the command below...

```
nvm use && nvm install
```
... ensures that you're using the proper version.

----
## 2. Installing dependencies

Using [npm](https://www.npmjs.com/), this command installs all the necessary dependencies:
```
npm i
```
----
## 3. Starting the server

The application server can be started by running:
```
npm start
```
By default, the application listens to requests made to port `3000` (e.g.: `http://localhost:3000/users`). This can be changed through the `PORT` environment variable. E.g.: In Linux:
```
PORT=2345 npm start
```
----
## 4. Testing through Postman

The project includes a [Postman](https://www.postman.com/) collection that describes each of the API endpoints and can be used to test them. It's located in `04/UsersApi.postman_collection.json`.