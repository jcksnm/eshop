from main import db, User, Item

db.create_all()

test_user = User("testuser@test.com", "test_user", "password",0, 1)
test_user2 = User("testuser@test.com2", "test_user2", "password2", 0, 0)

Galaxy = Item("Galaxy", "$700", "5")
Beats = Item("Beats", "$600", "8")
Arduino = Item("Arduino", "$300", "3")

print(test_user.id)
print(test_user2.id)

db.session.add_all([test_user, test_user2])
db.session.add_all([Galaxy, Beats, Arduino])
db.session.commit()

print(test_user.id)
print(test_user2.id)
print(Galaxy.item_price)
