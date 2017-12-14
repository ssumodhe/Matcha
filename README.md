# Matcha
Find your soul_match ! ;)

# Usage 
Python 3.6

### Routes
- `/signup-in`
- `/logout`
- `/messenger`
- `/profil`
- `/home`
- `/search`

#### QST?
- "faire des fonctions genre: `def get + "getName": return self. + "getname"`" ??
- "dans la methode 'modif' on doit save?"
- "on est obligé de faire des getQQCHO si on a deja search(QQCH)? Idem pour setQQCHO avec modif(QQCH)?" 

#### TODO
- Everything! :scream:
- Geoloc
- Instant Notif

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
> - sex (*integer*)
> - orientation (*integer*)
> - bio (*string*)
> - interests (*id*)
> - main_picture (*id*)
> - pop_score (*integer*)
> - created_at (*date*)
> - last_connexion (*date*)
 
> **Picture**
> - id (*integer*) -> unique
> - user_id (*id*) -> unique
> - data (*string*)
> - created_at (*date*)

> **Like**
> - id (*integer*) -> unique
> - stalker_id (*id*)
> - victim_id (*id*)
> - created_at (*date*)
> - stalker_id X victime_id -> unique

> **Dialog**
> - id (*integer*) -> unique
> - user_1 (*string*)
> - user_2 (*string*)
> - user_1 X user_2 -> unique
> - created_at (*date*)

> **Message**
> - id (*integer*) -> unique
> - dialog_id (*id*)
> - from (*id*)
> - content (*string*)
> - created_at (*date*)

> **View**
> - id (*integer*) -> unique
> - stalker (*id*)
> - victim (*id*)

> **Interest**
> - id (*integer*)
> - value (*string*)

> **Interest / User**
> - id (*integer*)
> - user_id (*id*)
> - interest_id (*id*)
