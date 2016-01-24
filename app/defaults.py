from app import db
from app.models import Role, User
import utilities

#db.drop_all()
#db.create_all()

admin_role = Role(name='Admin')
user_role = Role(name='User')
user_flo = User(name='Florian Einfalt',
                email='florian.einfalt@me.com',
                password=utilities.hash_password('password123'),
                role=admin_role,
                is_live=True)
user_olly = User(name='Oliver Longworth',
                 email='whateverthe@email.com',
                 password=utilities.hash_password('password123'),
                 role=admin_role,
                 is_live=True)

db.session.add_all([admin_role, user_role, user_flo, user_olly])
db.session.commit()