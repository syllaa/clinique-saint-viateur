from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.article import Article
from app.models.blog_category import BlogCategory
from app.models.specialty import Specialty
from app.utils import unique_slug

SEED_SERVICES = [
    ("🩺", "stethoscope", "Médecine Générale", "Consultation, suivi médical, bilan de santé et prise en charge des pathologies courantes."),
    ("🤱", "venus", "Gynécologie & Maternité", "Suivi prénatal, accouchement médicalisé, consultation gynécologique et soins de maternité."),
    ("🔪", "scissors", "Chirurgie", "Interventions chirurgicales programmées et d'urgence avec bloc opératoire moderne."),
    ("🫀", "heart-pulse", "Cardiologie", "Diagnostic, ECG, suivi et traitement des affections cardiaques et vasculaires."),
    ("🧒", "baby", "Pédiatrie", "Consultations enfants, vaccinations, suivi de croissance et soins spécialisés."),
    ("🔬", "flask-conical", "Laboratoire d'Analyses", "Bilan sanguin, sérologie, parasitologie, microbiologie et examens spéciaux."),
    ("📡", "scan", "Échographie & Imagerie", "Échographies obstétricales, abdominales, pelviennes et cardiaques."),
    ("🦷", "smile", "Cabinet Dentaire", "Soins dentaires, extraction, détartrage, prothèses et chirurgie buccale."),
    ("🚑", "ambulance", "Urgences & Réanimation", "Prise en charge immédiate des urgences médicales, disponible 24h/24, 7j/7."),
]

SEED_ARTICLES = [
    (
        "Campagne de dépistage cardiovasculaire gratuit",
        "À l'occasion de la Journée mondiale du cœur, bénéficiez d'un bilan cardiovasculaire offert à la clinique.",
        "Événement",
        "🫀",
    ),
    (
        "Se protéger du paludisme en saison des pluies",
        "Le paludisme reste la première cause de consultation. Voici nos recommandations essentielles pour vous et votre famille.",
        "Prévention",
        "🦟",
    ),
    (
        "Nouveau service : consultations en nutrition et diététique",
        "La clinique renforce son offre avec des consultations spécialisées en nutrition et diététique.",
        "Services",
        "🥗",
    ),
    (
        "Vos résultats d'analyses maintenant accessibles en ligne",
        "Accédez facilement à vos résultats de laboratoire via notre portail sécurisé, à tout moment.",
        "Actualité",
        "🔬",
    ),
]


def _get_or_create_category(db: Session, name: str) -> BlogCategory:
    category = db.query(BlogCategory).filter(BlogCategory.name == name).first()
    if category is None:
        slug = unique_slug(
            name, exists=lambda s: db.query(BlogCategory).filter(BlogCategory.slug == s).first() is not None
        )
        category = BlogCategory(name=name, slug=slug)
        db.add(category)
        db.flush()
    return category


def ensure_seed_content(db: Session) -> None:
    """Populate specialties and articles from the original site content, once."""
    if db.query(Specialty).first() is None:
        for position, (icon, icon_name, name, description) in enumerate(SEED_SERVICES):
            slug = unique_slug(
                name, exists=lambda s: db.query(Specialty).filter(Specialty.slug == s).first() is not None
            )
            db.add(
                Specialty(
                    icon=icon,
                    media_type="icon",
                    icon_name=icon_name,
                    name=name,
                    description=description,
                    position=position,
                    slug=slug,
                )
            )

    if db.query(Article).first() is None:
        for title, excerpt, category_name, icon in SEED_ARTICLES:
            category = _get_or_create_category(db, category_name)
            slug = unique_slug(
                title, exists=lambda s: db.query(Article).filter(Article.slug == s).first() is not None
            )
            db.add(
                Article(
                    title=title,
                    slug=slug,
                    excerpt=excerpt,
                    category_id=category.id,
                    icon=icon,
                    status="published",
                    published_at=datetime.now(timezone.utc),
                )
            )

    db.commit()
