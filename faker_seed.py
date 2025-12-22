import os
import django

# --------------------------------------------------
# DJANGO BOOTSTRAP (REQUIRED FOR ROOT SCRIPTS)
# --------------------------------------------------
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio_site.settings")
django.setup()

# --------------------------------------------------
# IMPORTS (SAFE AFTER django.setup())
# --------------------------------------------------
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from faker import Faker
import random
from decimal import Decimal

# BLOG
from blog.models import Post, Category, Tag

# CONTACT
from contact.models import Message

# CORE
from core.models import SiteSettings

# PORTFOLIO
from projects.models import (
    Skill, Client, Project, ProjectSection, ProjectImage
)

# SERVICES
from services.models import Service, Deliverable, ProcessStep

# TESTIMONIALS
from testimonials.models import Testimonial


def run():

    if not settings.DEBUG:
        raise Exception("❌ Seeding blocked outside DEBUG mode")

    fake = Faker()
    Faker.seed(2024)

    User = get_user_model()

    print("🧹 Clearing old data...")

    # --- DELETE ORDER (IMPORTANT) ---
    Message.objects.all().delete()
    Testimonial.objects.all().delete()
    ProjectImage.objects.all().delete()
    ProjectSection.objects.all().delete()
    Project.objects.all().delete()
    Client.objects.all().delete()
    Skill.objects.all().delete()

    Deliverable.objects.all().delete()
    ProcessStep.objects.all().delete()
    Service.objects.all().delete()

    Post.objects.all().delete()
    Category.objects.all().delete()
    Tag.objects.all().delete()

    User.objects.all().delete()
    SiteSettings.objects.all().delete()

    # -------------------------------
    # USER (YOU)
    # -------------------------------
    user = User.objects.create_user(
        username="osama",
        email="osama2kabdullah@gmail.com",
        password="123123",
        first_name="Osama",
        last_name="Abdullah",
    )

    # -------------------------------
    # SITE SETTINGS
    # -------------------------------
    SiteSettings.objects.create(
        site_title="Osama Abdullah — Shopify Theme Developer",
        tagline="High-performance Shopify themes & custom storefronts",
        about=(
            "I am Osama Abdullah, a Shopify Theme Developer with over 3 years "
            "of experience building fast, conversion-focused Shopify stores. "
            "I specialize in Liquid, Dawn theme customization, and scalable UI systems."
        ),
        contact_email="abdullah21673@hotmail.com",
        github="https://github.com/osama2kabdullah",
        linkedin="https://www.linkedin.com/in/md-abdullah-9121b5228",
    )

    # -------------------------------
    # SKILLS
    # -------------------------------
    skill_names = [
        "Shopify Theme Development",
        "Liquid",
        "HTML5",
        "CSS3",
        "JavaScript",
        "Tailwind CSS",
        "Shopify CLI",
        "Performance Optimization",
        "Storefront API",
        "Git & GitHub",
        "Shopify App Development",
        "Python",
        "Django",
        "Flask",
        "Node.js",
        "SQL",
        "PostgreSQL",
    ]

    skills = []
    for i, name in enumerate(skill_names):
        skills.append(
            Skill.objects.create(
                name=name,
                level=random.randint(75, 95),
                order=i,
            )
        )

    # -------------------------------
    # SERVICES
    # -------------------------------
    service_titles = [
        "Custom Shopify Theme Development",
        "Shopify Theme Customization",
        "Shopify Theme Update",
        "Store Speed Optimization",
        "Custom Website Build",
        "Web Application Development",
    ]

    services = []
    for i, title in enumerate(service_titles):
        service = Service.objects.create(
            title=title,
            slug=slugify(title),
            description=fake.paragraph(nb_sentences=4),
            icon="shopify",
            order=i,
            published=True,
        )
        services.append(service)

        for j in range(3):
            Deliverable.objects.create(
                service=service,
                name=fake.sentence(nb_words=4),
                order=j,
            )

        for j in range(3):
            ProcessStep.objects.create(
                service=service,
                title=fake.sentence(nb_words=3),
                description=fake.paragraph(nb_sentences=3),
                order=j,
            )

    # -------------------------------
    # CLIENTS
    # -------------------------------
    clients = []
    for _ in range(8):
        clients.append(
            Client.objects.create(
                name=fake.name(),
                company_name=fake.company(),
                email=fake.email(),
                whatsapp=f"+1{fake.msisdn()[:10]}",
                website=f"https://{fake.domain_name()}",
            )
        )

    # -------------------------------
    # PROJECTS
    # -------------------------------
    projects = []
    for i in range(12):
        title = fake.catch_phrase()
        project = Project.objects.create(
            title=title,
            slug=slugify(f"{title}-{i}"),
            client=random.choice(clients),
            excerpt=fake.paragraph(nb_sentences=2),
            hero_description=fake.paragraph(nb_sentences=4),
            live_url=f"https://{fake.domain_name()}",
            repo_url="",
            featured=i < 3,
            published=True,
            timeline=f"{random.randint(3,8)} weeks",
            year=random.randint(2021, 2024),
        )

        project.technologies.set(random.sample(skills, k=5))
        project.services.set(random.sample(services, k=2))

        projects.append(project)

        for j in range(3):
            ProjectSection.objects.create(
                project=project,
                heading=fake.sentence(nb_words=4),
                subheading=fake.sentence(nb_words=6),
                body=fake.paragraph(nb_sentences=5),
                order=j,
                is_highlight=j == 1,
            )

    # -------------------------------
    # BLOG
    # -------------------------------
    categories = []
    for name in ["Shopify", "Themes", "Performance", "Development"]:
        categories.append(
            Category.objects.create(
                name=name,
                slug=slugify(name),
            )
        )

    tags = []
    for name in ["shopify", "liquid", "themes", "dawn", "performance"]:
        tags.append(Tag.objects.create(name=name))

    for i in range(10):
        title = fake.sentence(nb_words=6)
        post = Post.objects.create(
            title=title,
            slug=slugify(f"{title}-{i}"),
            author=user,
            content=fake.paragraph(nb_sentences=10),
            excerpt=fake.paragraph(nb_sentences=2),
            published=True,
        )
        post.categories.set(random.sample(categories, k=2))
        post.tags.set(random.sample(tags, k=3))

    # -------------------------------
    # TESTIMONIALS
    # -------------------------------
    for i in range(8):
        Testimonial.objects.create(
            client=random.choice(clients),
            project=random.choice(projects),
            name=fake.name(),
            role=random.choice(["Founder", "E-commerce Manager", "CTO"]),
            company=fake.company(),
            body=(
                "Osama delivered a high-quality Shopify theme with excellent "
                "performance and clean code. Communication was clear and timely."
            ),
            email=fake.email(),
            featured=i < 3,
            approved=True,
            order=i,
        )

    # -------------------------------
    # CONTACT MESSAGES
    # -------------------------------
    for _ in range(6):
        Message.objects.create(
            name=fake.name(),
            email=fake.email(),
            service=random.choice(services),
            budget=Decimal(random.randint(500, 5000)),
            body=fake.paragraph(nb_sentences=4),
            is_read=random.choice([True, False]),
        )

    print("✅ FULL PROJECT SEEDED SUCCESSFULLY")


if __name__ == "__main__":
    run()
