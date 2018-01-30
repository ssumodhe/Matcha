# Matcha
Find your soul_match ! ;)

# Usage 
Python 3.6

### Routes
- `/signup-in`
- `/logout`
- `/messenger`
- `/profile`
- `/home`
- `/search`

#### QST?
- "faire des fonctions genre: `def get + "getName": return self. + "getname"`" ??
- "dans la methode 'modif' on doit save?"
- "on est obligé de faire des getQQCHO si on a deja search(QQCH)? Idem pour setQQCHO avec modif(QQCH)?"

- Executer le setup_db.py
- Framework Frontend

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
> - password (*string*) [8, 24]chars with lower/capital/digit
> - confirmed (*boolean*) 0: NotConfirmed 1:Confirmed
<!-- > - token (*string*) -->
<!-- > - expired_at (*date*) -->
> - age (*integer*)
> - sex (*integer*) 1:homme 2:femme
> - orientation (*integer*) 0:homo 1:hetero 2:bi
> - bio (*string*)
> - interests (*id*)
> - main_picture (*id*)
> - pop_score (*integer*)
> - location (*string*)
> - created_at (*date*)
> - last_connexion (*date*)
> - status (*integer*) 0:offline 1:online
 
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

> **Match**
> - id (*integer*) -> unique
> - user1_id (*string*)
> - user2_id (*string*)
> - user1_id X user2_id -> unique
> - created_at (*date*)

<!-- > **Dialog**
> - id (*integer*) -> unique
> - user1_id (*string*)
> - user2_id (*string*)
> - user1_id X user2_id -> unique
> - created_at (*date*) -->

> **Message**
> - id (*integer*) -> unique
> - match_id (*id*)
> - from (*id*)
> - content (*string*)
> - created_at (*date*)

> **View**
> - id (*integer*) -> unique
> - stalker_id (*id*)
> - victim_id (*id*)
> - created_at (*date*)

> **Interest**
> - id (*integer*)
> - value (*string*)
> - created_at (*date*)

> **Interest / User**
> - id (*integer*)
> - user_id (*id*)
> - interest_id (*id*)
> - created_at (*date*)

> **Block**
> - id (*integer*) -> unique
> - by_id (*id*)
> - blocked_id (*id*)
> - created_at (*date*)
> - by_id X blocked_id -> unique

> **Notification**
> - id (*integer*) -> unique
> - user_id (*id*)
> - message (*string*)
> - seen (*boolean*) 0: unseen; 1: seen
> - created_at (*date*)

#### Sources
Python
- https://www.youtube.com/watch?v=ajrfDEi8F7Y (FR - base)
- https://www.youtube.com/watch?v=ZVGwqnjOKjk (EN - base)
- https://www.youtube.com/watch?v=KfBiTR_w_Ic (FR - complet)

HTML CSS
- Emoji : https://afeld.github.io/emoji-css/
- Normalized Css : <\link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/5.0.0/normalize.min.css"/>
- Color in Hex : https://www.w3schools.com/colors/colors_picker.asp

SQLITE
- DB Browser (Myadmin for sqlite) : http://sqlitebrowser.org/

Bootstrap (Framework Frontend) http://getbootstrap.com/
- Bootstrap Tutoriels : https://www.youtube.com/watch?v=qIULMnbH2-o