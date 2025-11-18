# Novellia Pets

This repository contains an extremely minimal proof of concept style implementation of Novellia Pets

## Getting started

To run the app you can run either `make dev` or `make run`, depending on whether or not you want to run it in dev mode. You should then be able to access the app at http://127.0.0.1:5000/

To run the tests run `make test`

## Implementation Notes

### Tech Stack

I've chosen to use python with flask for this exercise. Why flask? The short, honest, answer is nostalgia. This was one of the first tech stacks I ever learned and it's been a while since I worked in it and I thought it might be fun to revisit it. Another reason is that python with flask is a nice simple framework that makes it pretty easy to get something basic up and running with minimal fuss. I also considered using nextjs for this because it is similarly great for getting something basic up and running quickly, but I was in a python mood

### Login in

### Data store

## What I would change if this was a production app

- Django instead of Flask
- React with typescript instead of templates
- Use an actual database (I'm partial to postgres)

## What I would like to do with more time

- A lot of the styling, especially spacing, is pretty wonky. I would love to spend more time making it actually pretty to look at
- More tests
- There's quite a lot of code cleanup that could be done here. The create and edit pet forms should be combined into one, the models should have CRUD functions that the api layer calls, there's some inconsistencies in function structure that i'd like to fix, etc.
- More robust error handling with nicer error messages
- Success banners on successful changes
- Some actually pretty charts and graphs on the dashboard. i love making charts and graphs so I'm sad I didn't end up having time to really display that, but I prioritized hitting as many of the requirements as possible over making one feature really nice.
