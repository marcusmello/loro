## Unreleased

### Refactor

- **docker**: transform into a docker cluster
- **architecture**: reshape in order to implement docker
- **chatbot**: finish the bare ground objects
- **chatbot**: rebuild routes and add default choices
- **chatbot**: create default 'welcome' and 'exit' answers
- **namespace**: rename all 'dialog*' to 'answer*' and delete 'return*' stuff
- **web-templating**: add updates variables context, add error cases and do formatting
- **web-templating**: add tag to confirm delete modal body
- **web-routing**: add 'update_error' path
- **presentation**: delete useless template
- **web**: rename 'routes' to 'pages'
- **web**: rename 'routes' package to 'pages' package
- **web**: add 'dialogs' routes CORS
- **presentation**: add 'new_return' to the template context in order to correctly render the existing tag scenario
- **presentation**: add 'new_return' to the template context in order to correctly render the existing tag scenario
- **CRUD**: pass creation attributes through a dictionary packing
- **database**: transform 'choices' Dialog attribute into array, instead of a related entity
- **schemas**: add 'invalid none' protection on Choice and Dialog 'leads_to' attribute
- **API**: add a nonexistent tag protection on 'delete' and 'update' methods
- **presentation**: format html code style and add defaults values to form, instead placeholders
- **presentation**: format html code style and add defaults values to form, instead placeholders
- **presentation**: format html code layout and add form placeholders
- **presentation**: in case of existent tag, show tag and content newly typed
- **presentation**: sort returns alphabetically by tags
- **web-routing**: unify the routes to the pages in a single module
- **lib**: remove the 'lib' package from .gitignore
- **web-routing**: delete useless 'items' testing route
- **database**: transform into anemic models, transferring the 'crud' methods to the 'crud' module
- **api-routing**: move 'db_session' to 'crud' and finalize necessary routes
- **web-routing**: add 'domain' variable in order to adjust the relative routes
- **database-mapping**: add pony ORM as a development dependency
- **database-mapping**: add pony ORM as a development dependency
- **environment-variables**: add 'environs' lib to handle environment variables
- **environment-variables**: add 'environs' lib to handle environment variables
- **web-routing**: add 'domain' variable and 'home' path
- **web-routing**: add 'domain' variable in order to adjust the relative routes
- **Architecture**: make html base template and some pages; also the first schemas
- **Architecture**: build routes and poetry entrypoint command
- **Architecture**: reshape to a monolith
- **Architecture**: implement flutter bare ground
- **architecture**: Splits the application into frontend and backend

### Fix

- **web**: delete useless leads_to" Tag in answer
- **web**: delete useless 'leads_to' tag in answers
- **crud**: return None instead empty answer. Empty answer was breaking the 'nonexistent' tag template logic
- **cleanup**: delete useless print
- **API**: fix route variable

### Feat

- **chatbot**: create useful choices indexes list
- **web-templating**: create a delete confirmation modal
- **web-routing**: add update routes
- **web-templating**: add update contexts
- **CRUD**: create 'dialogs' CRUD basic functions
- **API**: create 'dialogs' function endpoints
- **API**: add 'dialogs' route
- **database-mapping**: add database providers credentials info
- **database-mapping**: create the basic models
