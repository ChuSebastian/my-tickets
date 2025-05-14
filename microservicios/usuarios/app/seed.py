from sqlalchemy.orm import Session
from app.models import User, Role, UserRole
import random

def seed_roles(db: Session):
    if db.query(Role).count() == 0:
        role_names = ['admin', 'editor', 'viewer']
        roles = [Role(nombre_rol=name) for name in role_names]
        db.add_all(roles)
        db.commit()

def seed_users(db: Session, total_users=20000, batch_size=1000):
    roles = db.query(Role).all()
    role_ids = [role.id for role in roles]
    base_names = ["sam", "john", "emma", "lisa", "mike", "anna", "tom", "kate"]
    total_base_names = len(base_names)
    counter = 1
    name_index = 0

    for batch_start in range(0, total_users, batch_size):
        users = []
        user_roles = []

        for _ in range(batch_size):
            base_name = base_names[name_index]
            username = f"{base_name}{counter}"
            email = f"{username}@email.com"
            password = username

            users.append(User(username=username, email=email, password=password))

            name_index = (name_index + 1) % total_base_names
            if name_index == 0:
                counter += 1

        db.bulk_save_objects(users)
        db.commit()

        inserted_users = db.query(User).order_by(User.id.desc()).limit(batch_size).all()
        for user in inserted_users:
            assigned_roles = random.sample(role_ids, k=random.randint(1, 2))
            for role_id in assigned_roles:
                user_roles.append(UserRole(usuario_id=user.id, rol_id=role_id))

        db.bulk_save_objects(user_roles)
        db.commit()

def run_seed(db: Session):
    if db.query(User).first() is None:
        print("Seeding initial data...")
        seed_roles(db)
        seed_users(db)
        print("Seeding complete.")
    else:
        print("Skipping seeding: data already exists.")
