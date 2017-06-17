# API
---
### Contents:
1. API Documentation
1.1 API call "requirements"
2. CURL examples
3. POSTMAN examples

---
## API Documentation:

The best visual analytic way to understand this API is to paste `api.swagger`'s content into `http://editor.swagger.io`.

You can test reaching our API by hitting `http://localhost:8000/api/v1/health`. Remember to have your test server running.

#### API call requirements:
- Authorization token.
  *This token must be unique for each integrator entity (customer or partner or internal area...)*
- HTTP Requests must be in JSON format.


## CURL examples

List all departments:
```
$ curl -i -X GET -H "Content-Type: application/json" http://localhost:8000/api/v1/department
```

Add new department:
```
$ curl -i -X POST -H "Accept: application/json" -H "Authorization: 00123456789ABCDEF" --data-raw '("department_name":"Financial"}' http://localhost:8000/api/v1/department
```

Update department:
```
$ curl -i -X PUT -H "Accept: application/json" --data-raw '{"id": 2, "department_name":"MobileNEW"}' http://localhost:8000/api/v1/department
```


Delete department:
```
$ curl -i -X DELETE -H "Accept: application/json" --data-raw '{"department_name":"HR"}' http://localhost:8000/api/v1/department
```

## POSTMAN examples
Postman examples are stored in the folder: `backend_experiment/docs/postman/`. Import theses files to your Postman app.
