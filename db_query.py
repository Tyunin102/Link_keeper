CREATE_TABLE = '''CREATE TABLE IF NOT EXISTS links
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, chat_id TEXT, link TEXT)'''

SELECT_LINK = '''SELECT link FROM links WHERE chat_id = ? ORDER BY RANDOM() LIMIT 1'''

DELETE_LINK = '''DELETE FROM links WHERE link = ? AND chat_id = ?'''

INSERT_LINK = '''INSERT INTO links (chat_id, link) VALUES (?, ?)'''
