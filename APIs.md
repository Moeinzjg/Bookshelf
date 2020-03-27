/submit/booksread
    POST, returns a JSON
    input: title, author, publisher, genre, token
    output: status:ok

/submit/books2read
    POST, returns a JSON
    input: title, author, publisher, genre, token
    output: status:ok

/account/register/
step1:
    POST
    input: username, email, password
    output: status:ok
step2: # click on the link with the code in email
    GET
    input: email, code
    output: status:ok (shows the token)

/query/generalstat/
    POST, returns a json
    input: fromdata(optional), todate(optional), token
    output: JSON of some general stats for this user