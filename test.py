from browser import *
test = browser()
content = test.post("https://blablaland.co/site/connexion.php", {
    'con_pseudo': 'zagicien',
    'con_password': 'assddd123'
})
content = test.get("https://blablaland.co")