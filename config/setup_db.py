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
    age INTEGER,
    sex INTEGER,
    orientation INTEGER DEFAULT 2,
    bio VARCHAR(1024),
    main_picture INTEGER,
    pop_score INTEGER DEFAULT 0,
    location VARCHAR(255),
    lat REAL,
    long REAL,
    created_at DATETIME NOT NULL,
    last_connexion DATETIME,
    status INTEGER DEFAULT 0,
    fake INTEGER DEFAULT 0,
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

cursor.execute('''CREATE TABLE IF NOT EXISTS matchs
    (id INTEGER PRIMARY KEY,
    user1_id INTEGER NOT NULL,
    user2_id INTEGER NOT NULL,
    created_at DATETIME NOT NULL,
    UNIQUE(user1_id, user2_id)
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
    match_id INTEGER NOT NULL,
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

cursor.execute('''CREATE TABLE IF NOT EXISTS usersinterests
    (id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    interest_id INTEGER NOT NULL,
    created_at DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (interest_id) REFERENCES interests(id)
    );''')

cursor.execute('''CREATE TABLE IF NOT EXISTS blocks
    (id INTEGER PRIMARY KEY,
    by_id INTEGER NOT NULL,
    blocked_id INTEGER NOT NULL,
    created_at DATETIME NOT NULL,
    UNIQUE(by_id, blocked_id),
    FOREIGN KEY (by_id) REFERENCES users(id),
    FOREIGN KEY (blocked_id) REFERENCES users(id)
    );''')

cursor.execute('''CREATE TABLE IF NOT EXISTS notifications
    (id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    message VARCHAR(1024) NOT NULL,
    seen BOOLEAN NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
    );''')

db.commit()
cursor.close()