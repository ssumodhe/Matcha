# Matcha
Find your soul_match ! ;)

### Routes
- `/signup-in`
- `/logout`
- `/messenger`
- `/profil`
- `/home`
- `/search`

#### TODO
All has been done ! :muscle::skin-tone-4:

#### DB Models
> **User**
> - id (*integer*) -> unique
> - username (*string*) -> unique
> - first_name (*string*) -> unique
> - last_name (*string*) -> unique
> - email (*string*) -> unique
> - password (*string*)
> - confirmed (*boolean*)
<!-- > - token (*string*) -->
<!-- > - expired_at (*date*) -->
> - sex (*string*)
> - orientation (*string*)
> - bio (*string*)
> - interests (*id*)
> - main_picture (*string*)
> - pop_score (*string*)
> - last_connexion (*date*)
> - created_at (*date*)
 
> **Picture**
> - id (*integer*) -> unique
> - user_id (*string*) -> unique
> - data (*string*)
> - created_at (*date*)

> **Like**
> - id (*integer*) -> unique
> - user_id (*integer*)
> - picture_id (*integer*)
> - user_id X picture_id -> unique
> - created_at (*date*)

> **Dialog**
> - id (*integer*) -> unique
> - user_1 (*string*)
> - user_2 (*string*)
> - user_1 X user_2 -> unique
> - created_at (*date*)

> **Message**
> - id (*integer*) -> unique
> - dialog_id (*integer*)
> - from (*string*)
> - content (*string*)
> - created_at (*date*)

> **Vue**
> - id (*integer*) -> unique
> - stalker (*id*)
> - victim (*id*)

> **Interest**
> - id (*integer*)
> - value (*string*)

