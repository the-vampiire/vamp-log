# Daily Log Project

A dual-build project to learn the similarities between Python and Javascript. Each using analogous technologies.

## Project Goal
#### A daily log system to keep track of and promote coding progress in a consistent, measurable and easy to use application.

### MVP user stories
  1) I can create a persistent daily log with the following fields
  
[ACCOMPLISHMENT] 
- What I learned today 
  - [140 char or less]

[CHALLENGE]
- What I am stuck on or would like to learn tomorrow
  - [140 char or less]

[PATH]
- A resource URL to guide me through what I am stuck on or want to learn 
  - [1+ links]

[RECOGNITION]
- A piece of code that I am proud of from today 
  - [embedded in the page and collapsible]

2) I can view my previous logs in a continuous timeline
- The first item in the timeline will display the log from the previous day

3) I can mark a "stuck on / learn" field from a previous day "completed"

4) I can view and interact with my log on any device (full responsiveness)

### Bonus user stories
  1) I can view a "completed" counter that logs how many challenges I have overcome (marked "completed")

  2) I can add a comment to an item when I mark it "completed"

  3) I can view a streak counter to keep track of how many days in a row I have completed a log

## Technologies

### Python Build
Modules 
  - Flask (server)
  - Jinja2 (templating) 
  - MySQL (data persistence)
  - SQLAlchemy (ORM - interacting with MySQL)

Hosting 
  - https://www.pythonanywhere.com/

### Javascript (Node) Build
 Packages 
   - Express (server)
   - Mustache (templating)
   - MySQL (data persistence) 
   - Sequelize (ORM - interacting with MySQL)

 Hosting
   - https://heroku.com

## Database Structure [MySQL]
- Daily Logs have a one-to-many relationship with Paths
  - each [one] daily log can have multiple [many] paths (urls)
- `created_at` stored in 'Month[name] Day, Year' string format

### Tables [generated using https://www.tablesgenerator.com/markdown_tables#]
#### daily_logs
| column | id                | accomplishment | challenge     | recognition | notes | created_at   |
|-------:|-------------------|----------------|---------------|-------------|-------|--------------|
|   type | INT [primary key] | VARCHAR [140]  | VARCHAR [140] | TEXT        | TEXT  | VARCHAR [25] |
|        |                   |                |               |             |       |              |

#### paths
| column | id                | daily_log_id      | reference_url |
|-------:|-------------------|-------------------|---------------|
|   type | INT [primary key] | INT [foreign key] | TEXT |
|        |                   |                   |               |