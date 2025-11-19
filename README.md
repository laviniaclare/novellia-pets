# Novellia Pets

This repository contains an extremely minimal proof of concept style implementation of Novellia Pets

## Getting started

To run the app you can run either `make dev` or `make run`, depending on whether or not you want to run it in dev mode. You should then be able to access the app at http://127.0.0.1:5000/

To run the tests run `make test`

To see the regular customer view select any of the names from. See the admin view select the "Admin" user from the same dropdown.

## Implementation Notes

### Tech Stack

I've chosen to use python with flask for this exercise. Why flask? The short, honest, answer is nostalgia. This was one of the first tech stacks I ever learned and it's been a while since I worked in it and I thought it might be fun to revisit it. Another reason is that python with flask is a nice simple framework that makes it pretty easy to get something basic up and running with minimal fuss. I also considered using nextjs for this because it is similarly great for getting something basic up and running quickly, but I was in a python mood

### Login in

For the purposes of this exercise I have implemented a drop-down with a list of users that you can select to see how these users would see the app. In a production system we would obviously want real oath but I figured this was a simple way to make it easy to poke around as different personas.

### Data store

I opted to use an in-memory data store with some hard-coded data. Generally, the database is one of my favorite parts of a codebase to interact with, but there were a lot of features to implement in very little time, so cut out the db set-up for now, since it was not a hard requirement. This means some of the methods are not as elegant as they could be.

## What I would change if this was a production app

- Django instead of Flask
- React with typescript instead of templates -- honestly, I would probably just do this from the start if I was to do this over again. As much fun as it was to get back to basics with html, I did miss a lot of reacts features, especially when implementing the admin dashboard.
- Use an actual database (I'm partial to postgres)
- Add a little more security around pet profiles and such. Only the owner or an admin should be able to view a pet's profile.

## What I would like to do with more time

- A lot of the styling, especially spacing, is pretty wonky. I would love to spend more time making it actually pretty to look at
- More tests
- Use a real database!!
- There's quite a lot of code cleanup that could be done here. The create and edit pet forms should be combined into one, the models should have CRUD functions that the api layer calls, there's some inconsistencies in function structure that i'd like to fix, etc.
- More robust error handling with nicer error messages
- Success banners on successful changes
- Some actually pretty charts and graphs on the dashboard. i love making charts and graphs so I'm sad I didn't end up having time to really display that, but I prioritized hitting as many of the requirements as possible over making one feature really nice.

# Closing Thoughts

This was overall a pretty fun exercise, although I did find the scope a little intimidating for the amount of time suggested. I'd rather be able to implement fewer features with more polish than a lot of features with very little polish. I think if I had chosen a different tech stack for this exercise some aspects would have been a little easier though.
