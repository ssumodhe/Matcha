import sqlite3

# Code qui s'execute a chaque reload de la page : 
# check si Matcha.db existe avant d'exec les requetes?

db = sqlite3.connect('Matcha.db')
cursor = db.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users 
    (id INTEGER PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    confirmed BOOLEAN DEFAULT 0,
    sex INTEGER,
    orientation INTEGER DEFAULT 2,
    bio VARCHAR(1024),
    interests INTEGER,
    main_picture INTEGER,
    pop_score INTEGER DEFAULT 0,
    created_at DATETIME NOT NULL,
    last_connexion DATETIME,
    connected INTEGER DEFAULT 0,
    FOREIGN KEY (main_picture) REFERENCES pictures(id)
    );''')

cursor.execute('''CREATE TABLE IF NOT EXISTS pictures 
    (id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    data TEXT,
    created_at DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
    );''')

cursor.execute('''CREATE TABLE IF NOT EXISTS likes
    (id INTEGER PRIMARY KEY,
    stalker_id INTEGER NOT NULL,
    victim_id INTEGER NOT NULL,
    created_at DATETIME NOT NULL,
    UNIQUE(stalker_id, victim_id),
    FOREIGN KEY (stalker_id) REFERENCES users(id),
    FOREIGN KEY (victim_id) REFERENCES users(id)
    );''')

cursor.execute('''CREATE TABLE IF NOT EXISTS dialogs
    (id INTEGER PRIMARY KEY,
    user1_id INTEGER NOT NULL,
    user2_id INTEGER NOT NULL,
    created_at DATETIME NOT NULL,
    UNIQUE(user1_id, user2_id)
    );''')

cursor.execute('''CREATE TABLE IF NOT EXISTS messages
    (id INTEGER PRIMARY KEY,
    dialog_id INTEGER NOT NULL,
    from_id INTEGER NOT NULL,
    content VARCHAR(255),
    created_at DATETIME NOT NULL
    );''')

cursor.execute('''CREATE TABLE IF NOT EXISTS views
    (id INTEGER PRIMARY KEY,
    stalker_id INTEGER NOT NULL,
    victim_id INTEGER NOT NULL,
    created_at DATETIME NOT NULL,
    FOREIGN KEY (stalker_id) REFERENCES users(id),
    FOREIGN KEY (victim_id) REFERENCES users(id)
    );''')

cursor.execute('''CREATE TABLE IF NOT EXISTS interests
    (id INTEGER PRIMARY KEY,
    value VARCHAR(255),
    created_at DATETIME NOT NULL
    );''')

cursor.execute('''CREATE TABLE IF NOT EXISTS users_interests
    (id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    interest_id INTEGER NOT NULL,
    created_at DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (interest_id) REFERENCES interests(id)
    );''')

# cursor.execute('''INSERT INTO users 
#     (username,
#     first_name,
#     last_name ,
#     email,
#     password,
#     created_at
#     ) 
#     VALUES
#     ('coco asticot',
#     'coco',
#     'channel',
#     'coco@channel.com',
#     'thomaiszebest',
#     '2005-06-15'
#     );''')

db.commit()
cursor.close()