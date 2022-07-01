<h1>
	Currency Converter REST API.
</h1>

## What is this about?
A minimal REST API that helps you figure out how much  let's say a dollar is worth in naira at the moment or at some date in the past.

## Getting Started Locally
The easiest way to get this project up and running locally is with Docker. You can get it [here](https://www.docker.com/products/docker-desktop/). With Docker setup on your PC, take the following steps to run this application locally:
- Clone this repo to your local machine
- Create a `.env` file in the root directory of this project.
- Copy the content of `.env-example` and paste it in your newly created `.env` file.

**make sure to replace the value of `API_KEY` with a valid key.** I've emailed a valid api-key that you could use to test things out.

- Run the command `docker build -t c-converter-image .` in the root directory of this project to build your docker image
- Run the command `docker run -p 80:80 --name c-converter-container c-converter-image` in the root directory of this project to spin up your container

## Acessing the Docs
Once your Docker Container is fired up, point your browser to `http://localhost:80/docs`.
You'd be greeted with a nice auto-generated docs. 

There are three endpoints there that you could play around with:
- `/supported-currencies`-- to see a list of all the currencies supported
- `/currency-converter` -- for doing the main conversion
- `/historical-data`-- for getting past and current exchange rates between currencies. For this endpoint, `date` query param should be in this format: `year-month-day: 2020-01-20`

## Running Tests
Take the following steps to run the tests cases:
- Install `pytest` -- `pip install pytest`
- Strangely, I couldn't get Pytest to work without requests, so install it too-- `pip install requests`
- Then run the command `pytest` in your root directory of this project. That would then run the test cases

## Author
Yours truly :)