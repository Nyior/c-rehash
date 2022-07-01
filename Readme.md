<h1>
	Currency Converter REST API.
</h1>


## Getting Started Locally
The easiest way to run this project locally is with [Docker](https://www.docker.com/products/docker-desktop/). With Docker setup, take the following steps:

- Clone this repo to your local machine
- Create a `.env` file in the root directory of this project.
- Copy the content of `.env-example` and paste it in your newly created `.env` file.

**Make sure to replace the value of `API_KEY` with a valid key.** I've emailed a valid api-key that you could use to test things out. Also update `ACCESS_TOKEN` with the one generated for you after login or signup

- Run the command `docker build -t c-converter-image .` in the root directory of this project to build your docker image
- Run the command `docker run -p 80:80 --name c-converter-container c-converter-image` in the root directory of this project to spin up your container

## Acessing the Docs
Point your browser to `http://localhost:80/docs` to access the docs. 

To test things out on the docs page:
- First, go to `/user/signup` to create an account. An `access_token` would be returned.
- Already have an account?, go to `/user/login` to sign in. An `access_token` would be returned.

- Grab your `access_token`, and click on the `Authorize` button on the docs page. After submitting a valid `access_token`, you'd have access to the endpoints.

## Running Tests
Take the following steps to run the tests cases:
- Install `pytest` -- `pip install pytest`
- Also install requests `pip install requests`
- Then run the command `pytest` in the root directory of this project. That would then run the test cases

## Nice-toHaves
Because this was a quick task, a couple of things had to be left out:

- A caching mechanism just so we don't connect to the external API each time there's a request. [Redis](https://redis.io/docs/) would work great here.
- Adding refresh tokens to automatically issue new JWTs when they expire.
- Using [Alembic](https://alembic.sqlalchemy.org/en/latest/) to manage our database
- Connecting to a more robust RDBMS like MYSQL or PostgreSQL