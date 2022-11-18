# AMDA-Orchestra

Orchestra is a collection of tools for managing the backend part of AMDA's machine learning pipeline. Orchestra uses Flask to expose a REST API used by AMDA's internal components to retrieve
information about the modules that are installed, create new prediction and more.

Each machine learning model is implemented as a `python module` that is installed with all its requirements in a dedictated docker container.

## Installation

### Docker

Orchestra uses docker to run predictions of eahc module in an isolated container, so in order to use it you should have installed docker in your machine.

### Run Orchestra

#### Dev Mode

To Run Orchestra in dev mode you just need to run:

<ul>
<li>`docker-compose build`
</li>
<li>`docker-compose up`
</li>
</ul>
#### Production Mode
To Run Orchestra in prod mode you just need to run:
<ul>
<li>`docker-compose -f docker-compose.prod.yml build`
</li>
<li>`docker-compose -f docker-compose.prod.yml up`
</li>
</ul>

## REST API endpoints

List of endpoints exposed by the REST API :

- `/modules` : retrieve a list of modules and assiciated metadata
- `/modules/<int:id>` : specific module metadata
- `/modules/<int:id>/run [args]` : request executing specified model with arguments supplied by user
- `/tasks` : retrieve list of tasks and associated metadata
- `/tasks/<int:id>` : specific task metadata (status, errors, output, ...)
- `/tasks/<int:id>/output` : download task output

## Monitoring Orchestra
To monitor Orchestra you just need to open http://localhost:3000/ :

<ul>
<li>
Installing a new module
</li>
<li>
Rebuilding a module
</li>
<li>
Trucking a running module for predictions
</li>
</ul>
