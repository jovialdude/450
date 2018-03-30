---
title: Homework 2
description: A Barebones HTTP/1.1 Client
due: Wednesday, February 7 
assigned: Friday, February 16
additional_css: [syntax.css]
---

## {{ page.title }}: {{ page.description }}

##### **This assignment is due at 11:59 pm on February 16, 2018.**

##### **You can download the homework zip archive [here]({{ site.url }}{{ site.baseurl }}/downloads/hw2.zip).**

##### **Make sure to read the homework before starting There are updated Autograder sumbission instructions.**


# Homework 2: A Barebones HTTP/1.1 Client

In this programming exercise, you will create a barebones web client. While
python includes a basic http client module `http.client`, this assignment will
serve as a learning experience for translating a protocol into an
implementation. Your deliverable will be a client which only implements the
`GET` method and follows the basics of the HTTP/1.1 specification, enough to
download files as one would with the command line program `curl`. In addition to 
this you are also required to verify the certificate of pages that you connect
https.

## HTTP/1.1 Features

[HTTP/1.0](https://tools.ietf.org/search/rfc1945) describes the most basic
functionality that an HTTP client is required to do. HTTP/1.1 includes several
new features that extend the protocol. For this assignment, you will only be
required to implement these additional features:

  * Include a `Host:` header
  * Correctly interpret `Transfer-encoding: chunked`
  * Include a `Connection: close` header, or handle persistent connections

These new features are described in James Marshall's excellent [HTTP Made Really Easy](https://www.jmarshall.com/easy/http/#http1.1clients) under the HTTP/1.1
clients subsection.

Note that the RFCs are your friends: if you're having trouble with
`Transfer-encoding`, check [the RFC][http] for hints!


## Basic HTTP functionality

As seen in class, HTTP is a stateless request-response protocol that consists
of an initial line, zero or more headers, and zero or more bytes of content.
Your program will implement a function, `retrieve_url`, which takes a url (as
a `str`) as its only argument, and uses the HTTP protocol to retrieve and
return the body's bytes (do not decode those bytes into a string). Consult
the book or your class notes for the basics of the HTTP protocol.

You may assume that the URL will not include a fragment, query string, or
authentication credentials. You are not required to follow any redirects -
only return bytes when receiving a `200 OK` response from the server. If for
any reason your program cannot retrieve the resource correctly, `retrieve_url`
should return `None`.

## Validating HTTPS
Within the `retrieve_url` you will also be required to ensure that when connecting
to a HTTPS based website, your client ensures a valid certificate is provided by the server. The `ssl` library in Python will do this for you by default.
If the returned certificate is invalid (expired, wrong host etc) and cannot be validated `retrieve_url` returns `None`. To test your code in addition to the provided tests, there are examples available at [badssl.com](https://badssl.com/).

## Template
A trivial template is provided in this repository, as `hw2.py`. This contains
the necessary modules you need to complete this homework. If you would like import any additional modules, make sure to ask on Piazza. 

## Testing and Grading
For this homework we will be using a server-side autogorader provided by OK to grade your work.
Like before, you can create as many backups as you like using `python3 ok`, however, for this homework each
time you provide the `--submit` flag will also send your submission to the autograder. The results of your 
code will be sent out to you on your UIC email address (the one you use to login to the OK Web UI). 

Importantly, to ensure some load balancing os the server autograder, we have also enforced a ***12 hour time*** window in which
you can submit your results once to the serverside autograger. If you attempt to make multiple submissions in the period, you will receive 
a limit exceeded email, it is recommended to use the autograder wisely. Like mentioned above, you can self verify your code
by comparing responses using the `requests` module and `curl`.

There is a total of **12 main points**, and **3 bonus points** on this
assignment, for a grand total of **15 possible points**.

  * **9 points** for correctly handling each of the **9** HTTP URLs.
  * **3 points** for correctly handling HTTPS based requests.
  * **3 bonus point** for taking care of URL redirects 

## Submission
You will be making the submission for this homework through the OK client. When you first download 
the homework, make sure you authenticate using `python3 ok --authenticate`. To save your work, feel 
free to create as many backups as you like.

The files which will be submitted by the ok client:
* `hw2.py`: This file will contain your version of the `retrieve_url`


To submit your work, run `python3 ok --submit`. Like previously, you are allowed to make multiple submissions 
but you have limited attempts with the grader.

## Due Date and Logistics

* This assignment is due at the at 11:59 pm on February 16, 2018.

* If you have any questions please use the [Piazza](https://piazza.com/class/j9oqs0y7d01k0) discussion forum.
