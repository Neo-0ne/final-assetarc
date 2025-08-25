import sqlite3
import json
import os

# --- Configuration ---
DB_PATH = '/app/eng_lifecycle.db'
CONTENT_BASE_DIR = 'Services/eng-lifecycle/course_content'
COURSE_ID = 1

# --- Data Definition ---
COURSE_DATA = {
    "id": COURSE_ID,
    "title": "AssetArc Structuring Master Course",
    "description": "A comprehensive course on asset protection, strategic structuring, and legacy planning."
}

MODULES_DATA = [
    {"id": 1, "title": "The 'Why' of Structuring (Foundations)", "order": 1},
    {"id": 2, "title": "The Asset Protection Playbook", "order": 2},
    {"id": 3, "title": "The Scalable Business Blueprint", "order": 3},
    {"id": 4, "title": "Bulletproof Compliance", "order": 4},
    {"id": 5, "title": "Advanced Strategies & Legacy Planning", "order": 5},
    {"id": 6, "title": "Going Global", "order": 6},
]

LESSONS_DATA = {
    1: [ # Module 1
        {"id": 101, "title": "Why Bother With Structuring?", "order": 1},
        {"id": 102, "title": "The Building Blocks: Companies vs. Trusts", "order": 2},
        {"id": 103, "title": "Choosing Your First Structure", "order": 3},
    ],
    2: [ # Module 2
        {"id": 201, "title": "Mastering Control: It's Not Just About Ownership", "order": 1},
        {"id": 202, "title": "The 3 Pillars of Asset Protection", "order": 2},
        {"id": 203, "title": "Your First Line of Defense: The HoldCo-OpCo Stack", "order": 3},
    ],
    3: [ # Module 3
        {"id": 301, "title": "The 4-Structure Stack for Growth", "order": 1},
        {"id": 302, "title": "Sequencing Your Structure for Success", "order": 2},
        {"id": 303, "title": "Restructuring Without the Tax Hit", "order": 3},
    ],
    4: [ # Module 4
        {"id": 401, "title": "The New Reality: Transparency is Non-Negotiable", "order": 1},
        {"id": 402, "title": "What is a 'Beneficial Owner'?", "order": 2},
    ],
    5: [ # Module 5
        {"id": 501, "title": "The Trust-Company Combo: Your Governance Powerhouse", "order": 1},
        {"id": 502, "title": "Structuring for Your Legacy: Property & Estate Planning", "order": 2},
        {"id": 503, "title": "Engineering Your Continuity: Buy-Sell Agreements", "order": 3},
    ],
    6: [ # Module 6
        {"id": 601, "title": "Structuring for a Borderless World", "order": 1},
        {"id": 602, "title": "Planning Your Exit: Tax Emigration & Second Passports", "order": 2},
    ],
}

def seed_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    print("Seeding database...")

    # --- Seed Course ---
    cursor.execute("INSERT OR IGNORE INTO courses (id, title, description) VALUES (?, ?, ?)",
                   (COURSE_DATA['id'], COURSE_DATA['title'], COURSE_DATA['description']))
    print(f"Course '{COURSE_DATA['title']}' seeded.")

    # --- Seed Modules, Lessons, and Quizzes ---
    for module_info in MODULES_DATA:
        module_id = module_info['id']
        cursor.execute("INSERT OR IGNORE INTO modules (id, course_id, title, module_order) VALUES (?, ?, ?, ?)",
                       (module_id, COURSE_ID, module_info['title'], module_info['order']))
        print(f"  Module {module_id}: '{module_info['title']}' seeded.")

        if module_id in LESSONS_DATA:
            for i, lesson_info in enumerate(LESSONS_DATA[module_id]):
                lesson_id = lesson_info['id']
                lesson_filename = f"lesson_{i+1}.md"
                lesson_path = os.path.join(CONTENT_BASE_DIR, f"module_{module_id}", lesson_filename)

                try:
                    with open(lesson_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    cursor.execute("INSERT OR IGNORE INTO lessons (id, module_id, title, content, lesson_order) VALUES (?, ?, ?, ?, ?)",
                                   (lesson_id, module_id, lesson_info['title'], content, lesson_info['order']))
                    print(f"    Lesson {lesson_id}: '{lesson_info['title']}' seeded.")
                except FileNotFoundError:
                    print(f"    [ERROR] Lesson file not found: {lesson_path}")

            # Seed Quiz for the module
            quiz_filename = os.path.join(CONTENT_BASE_DIR, f"module_{module_id}", "quiz.json")
            try:
                with open(quiz_filename, 'r', encoding='utf-8') as f:
                    quiz_data = json.load(f)

                # Assuming one quiz per module, linked to the last lesson
                last_lesson_id = LESSONS_DATA[module_id][-1]['id']

                for quiz_item in quiz_data:
                    cursor.execute("INSERT OR IGNORE INTO quizzes (lesson_id, question) VALUES (?, ?)",
                                   (last_lesson_id, quiz_item['question']))
                    quiz_id = cursor.lastrowid

                    if quiz_id == 0: # It already exists, get the id
                        cursor.execute("SELECT id FROM quizzes WHERE lesson_id = ? AND question = ?", (last_lesson_id, quiz_item['question']))
                        quiz_id = cursor.fetchone()[0]

                    for j, option_text in enumerate(quiz_item['options']):
                        is_correct = (j == quiz_item['correct_option'])
                        cursor.execute("INSERT OR IGNORE INTO quiz_options (quiz_id, option_text, is_correct) VALUES (?, ?, ?)",
                                       (quiz_id, option_text, is_correct))
                print(f"    Quiz for module {module_id} seeded.")

            except FileNotFoundError:
                print(f"    [INFO] No quiz file found for module {module_id}")


    conn.commit()
    conn.close()
    print("Database seeding complete.")

if __name__ == '__main__':
    # We need to make sure the DB exists and has the tables.
    # This is normally handled by the app, but we can do it here for standalone execution.
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}. Please run the main application first to initialize it.")
    else:
        seed_database()
