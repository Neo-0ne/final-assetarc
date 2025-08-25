"""
This file contains the business logic for the lifecycle engine's modules.
"""
from sqlalchemy import text

# This is a simplified representation of which templates are needed for which structure.
# In a real system, this might be more complex or stored in a database.
STRUCTURE_TEMPLATE_MAP = {
    "za_pty_ltd": {
        "name": "Private Company (Pty) Ltd",
        "description": "A standard limited liability company in South Africa, good for general business operations and liability protection.",
        "required_templates": [
            "company.incorp_checklist.za.v1",
            "company.board_resolution.za.v1",
            "company.share_certificate.za.v1"
        ]
    },
    "za_trust": {
        "name": "Inter-Vivos Trust",
        "description": "An entity created during one's lifetime to hold assets for beneficiaries. Excellent for asset protection and estate planning.",
        "required_templates": [
            "trust.deed.za.v1",
            "trust.letter_of_wishes.za.v1",
            "trustee.resolution.za.v1"
        ]
    },
    "mu_ibc": {
        "name": "Mauritius GBC (International Business Company)",
        "description": "An offshore company in Mauritius, ideal for international trade, investment holding, and tax optimization.",
        "required_templates": [
            "ibc.moa.v1",
            "ibc.nominee_agreement.v1",
            "ibc.kyc_checklist.v1"
        ]
    }
}


def design_corporate_structure(goals: list[str], jurisdiction: str) -> dict:
    """
    Proposes a corporate structure based on goals and jurisdiction.
    This is a simple rule-based implementation.
    """

    # Normalize inputs
    goals = [goal.lower() for goal in goals]
    jurisdiction = jurisdiction.lower()

    proposed_structures = []

    # --- Rule Engine ---
    if "liability_protection" in goals and jurisdiction == "za":
        if "za_pty_ltd" not in [p['id'] for p in proposed_structures]:
            proposed_structures.append({
                "id": "za_pty_ltd",
                **STRUCTURE_TEMPLATE_MAP["za_pty_ltd"]
            })

    if "asset_protection" in goals and jurisdiction == "za":
        if "za_trust" not in [p['id'] for p in proposed_structures]:
            proposed_structures.append({
                "id": "za_trust",
                **STRUCTURE_TEMPLATE_MAP["za_trust"]
            })

    if "international_trade" in goals or "tax_efficiency" in goals:
        # Suggesting Mauritius as a default for international goals
        if "mu_ibc" not in [p['id'] for p in proposed_structures]:
            proposed_structures.append({
                "id": "mu_ibc",
                **STRUCTURE_TEMPLATE_MAP["mu_ibc"]
            })

    # --- Fallback/Default ---
    if not proposed_structures:
        if jurisdiction == "za":
            proposed_structures.append({
                "id": "za_pty_ltd",
                **STRUCTURE_TEMPLATE_MAP["za_pty_ltd"]
            })
        else:
            # Default international suggestion
            proposed_structures.append({
                "id": "mu_ibc",
                **STRUCTURE_TEMPLATE_MAP["mu_ibc"]
            })

    return {
        "proposed_structures": proposed_structures,
        "inputs": {
            "goals": goals,
            "jurisdiction": jurisdiction
        }
    }

# --- Course Management Logic ---

def get_course_structure(engine, course_id: int):
    """Fetches the full structure of a course, including modules and lessons."""
    with engine.connect() as conn:
        # Fetch course details
        course = conn.execute(text("SELECT id, title, description FROM courses WHERE id = :id"), {"id": course_id}).first()
        if not course:
            return None

        # Fetch modules and lessons
        modules_query = text("""
            SELECT id, title, module_order
            FROM modules
            WHERE course_id = :course_id
            ORDER BY module_order
        """)
        modules_result = conn.execute(modules_query, {"course_id": course_id}).fetchall()

        modules = []
        for mod in modules_result:
            lessons_query = text("""
                SELECT id, title, lesson_order
                FROM lessons
                WHERE module_id = :module_id
                ORDER BY lesson_order
            """)
            lessons_result = conn.execute(lessons_query, {"module_id": mod.id}).fetchall()
            lessons = [{"id": l.id, "title": l.title, "order": l.lesson_order} for l in lessons_result]
            modules.append({"id": mod.id, "title": mod.title, "order": mod.module_order, "lessons": lessons})

    return {"id": course.id, "title": course.title, "description": course.description, "modules": modules}

def get_lesson_content(engine, lesson_id: int):
    """Fetches the content for a single lesson, including its quiz."""
    with engine.connect() as conn:
        lesson = conn.execute(text("SELECT id, title, content FROM lessons WHERE id = :id"), {"id": lesson_id}).first()
        if not lesson:
            return None

        quiz_query = text("SELECT id, question FROM quizzes WHERE lesson_id = :lesson_id")
        quiz = conn.execute(quiz_query, {"lesson_id": lesson_id}).first()

        options = []
        if quiz:
            options_query = text("SELECT id, option_text, is_correct FROM quiz_options WHERE quiz_id = :quiz_id")
            options_result = conn.execute(options_query, {"quiz_id": quiz.id}).fetchall()
            options = [{"id": o.id, "text": o.option_text, "is_correct": o.is_correct} for o in options_result]

        quiz_data = {"id": quiz.id, "question": quiz.question, "options": options} if quiz else None

    return {"id": lesson.id, "title": lesson.title, "content": lesson.content, "quiz": quiz_data}


def mark_lesson_complete(engine, user_email: str, lesson_id: int):
    """Marks a lesson as complete for a given user."""
    from datetime import datetime, timezone
    with engine.begin() as conn:
        query = text("""
            INSERT OR IGNORE INTO user_progress (user_email, lesson_id, completed_at)
            VALUES (:email, :lesson, :now)
        """)
        conn.execute(query, {"email": user_email, "lesson": lesson_id, "now": datetime.now(timezone.utc)})
    return True

def get_user_progress(engine, user_email: str, course_id: int):
    """Retrieves a list of completed lesson IDs for a user in a specific course."""
    with engine.connect() as conn:
        query = text("""
            SELECT up.lesson_id
            FROM user_progress up
            JOIN lessons l ON up.lesson_id = l.id
            JOIN modules m ON l.module_id = m.id
            WHERE up.user_email = :email AND m.course_id = :course_id
        """)
        result = conn.execute(query, {"email": user_email, "course_id": course_id}).fetchall()
        return [row.lesson_id for row in result]

def is_user_enrolled(engine, user_email: str, course_id: int) -> bool:
    """Checks if a user is enrolled in a specific course."""
    with engine.connect() as conn:
        query = text("SELECT 1 FROM course_enrollments WHERE user_email = :email AND course_id = :course_id")
        return conn.execute(query, {"email": user_email, "course_id": course_id}).scalar() == 1

def enroll_user_in_course(engine, user_email: str, course_id: int):
    """Enrolls a user in a course."""
    from datetime import datetime, timezone
    with engine.begin() as conn:
        query = text("""
            INSERT OR IGNORE INTO course_enrollments (user_email, course_id, enrolled_at)
            VALUES (:email, :course, :now)
        """)
        conn.execute(query, {"email": user_email, "course": course_id, "now": datetime.now(timezone.utc)})
    return True
