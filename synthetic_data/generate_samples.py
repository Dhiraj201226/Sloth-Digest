"""
Sloth Digest — Synthetic Sample Chat Generator
Produces realistic, strictly synthetic WhatsApp chat exports for evaluation,
benchmarking, and testing. Never uses real conversations.
"""

import random
from pathlib import Path

SYNTHETIC_DIR = Path(__file__).resolve().parent

def generate_hackathon_sample():
    """Generates a ~70-message hackathon squad chat."""
    lines = [
        "[24/10/2026, 19:00:12] Maya Chen: Hey team! Welcome to the Hacktoberfest 48h sprint channel.",
        "[24/10/2026, 19:01:05] David K.: Super excited! Did we decide on our database?",
        "[24/10/2026, 19:01:40] Sarah P.: I vote SQLite + local-first. We don't want cloud bills or API latency.",
        "[24/10/2026, 19:02:15] Maya Chen: Agreed. Let's make sure our offline privacy story is rock solid.",
        "[24/10/2026, 19:05:00] Leo M.: Has anyone seen the pizza delivery downstairs? 🍕",
        "[24/10/2026, 19:05:22] Sarah P.: Leo, focus! We haven't even written the API contract yet haha.",
        "[24/10/2026, 19:06:10] Leo M.: Going to grab pizza anyway. Back in 10.",
        "[24/10/2026, 19:12:45] Maya Chen: Action item: Sarah, can you please finalize the OpenAPI specification by Friday 11:00 PM?",
        "[24/10/2026, 19:13:20] Sarah P.: Yes, on it. Assigning myself to the OpenAPI spec.",
        "[24/10/2026, 19:15:30] David K.: What about the frontend? Are we using Tailwind?",
        "[24/10/2026, 19:16:00] Maya Chen: Yes, Vite + React + Tailwind. David, need you to set up the accessible components.",
        "[24/10/2026, 19:17:15] David K.: Sounds good, I'll build the component library by Saturday 10:00 AM.",
        "[24/10/2026, 19:22:00] Leo M.: The pizza was amazing guys.",
        "[24/10/2026, 19:23:10] Leo M.: Meme time: [image omitted]",
        "[24/10/2026, 19:24:00] Sarah P.: Lol that's so accurate.",
        "[24/10/2026, 19:25:12] Maya Chen: Important deadline: Final demo video must be submitted by Sunday at 4:00 PM sharp.",
        "[24/10/2026, 19:26:00] David K.: Got it on my calendar: Sunday 4 PM deadline.",
        "[24/10/2026, 19:30:15] Leo M.: Who has the HDMI adapter for the presentation podium?",
        "[24/10/2026, 19:31:00] Maya Chen: I have it in my backpack. Remind me before the pitch.",
        "[24/10/2026, 20:00:00] Sarah P.: Drafting the backend routes now. Looks very smooth.",
        "[24/10/2026, 20:15:20] David K.: I'll take a quick 20 min nap, don't wake me up unless the server crashes.",
        "[24/10/2026, 20:16:00] Maya Chen: Haha sleep well David, Sloth Digest will read our messages for you.",
        "[24/10/2026, 20:30:00] Leo M.: Another coffee round anyone?",
        "[24/10/2026, 20:31:10] Sarah P.: Double espresso please!",
        "[24/10/2026, 20:32:00] Maya Chen: Black coffee for me.",
    ]
    # Add some banter lines
    for i in range(1, 35):
        sender = random.choice(["Leo M.", "Sarah P.", "David K.", "Maya Chen"])
        banter = random.choice([
            "typing...",
            "testing test case " + str(i),
            "css is so tricky with vertical alignment",
            "check out this icon",
            "nice work team",
            "thumbs up 👍",
            "commit pushed to main branch",
            "checking build status",
            "clean build passed!",
        ])
        lines.append(f"[24/10/2026, 21:{i:02d}:15] {sender}: {banter}")

    out_file = SYNTHETIC_DIR / "sample_hackathon_team.txt"
    out_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated {out_file.name} ({len(lines)} messages)")


def generate_family_sample():
    """Generates a ~80-message family reunion chat."""
    lines = [
        "10/22/26, 09:15 - Evelyn Davies: Good morning family! Thanksgiving is approaching fast.",
        "10/22/26, 09:16 - Aunt Susan: Good morning Evelyn! So happy we can all gather this year.",
        "10/22/26, 09:18 - Uncle Bob: Has anyone ordered the turkey yet?",
        "10/22/26, 09:20 - Evelyn Davies: Bob, can you please pick up the 18-pound turkey from Miller's Farm by Wednesday Nov 25?",
        "10/22/26, 09:22 - Uncle Bob: On it Evelyn! Picking up the turkey Wednesday Nov 25.",
        "10/22/26, 09:25 - Cousin Clara: I am flying into JFK on Thursday Nov 26 at 11:30 AM. Who can pick me up?",
        "10/22/26, 09:28 - Michael Davies: I'm off work that morning Clara, I will pick you up at JFK terminal 4.",
        "10/22/26, 09:30 - Evelyn Davies: Wonderful! Michael is picking up Clara on Nov 26.",
        "10/22/26, 09:35 - Aunt Susan: I will bake the pumpkin pie and the apple tart 🥧",
        "10/22/26, 09:36 - Cousin Clara: Yay! Susan's famous apple pie!",
        "10/22/26, 09:40 - Uncle Bob: <Media omitted>",
        "10/22/26, 09:41 - Evelyn Davies: Look at the puppy! So cute.",
        "10/22/26, 09:45 - Michael Davies: Can someone bring extra folding chairs?",
        "10/22/26, 09:46 - Aunt Susan: We have 6 chairs in our garage, we'll bring them.",
        "10/22/26, 10:00 - Evelyn Davies: Don't forget: Family dinner starts promptly at 5:00 PM on Thursday Nov 26.",
    ]
    for i in range(1, 50):
        sender = random.choice(["Evelyn Davies", "Uncle Bob", "Aunt Susan", "Cousin Clara", "Michael Davies"])
        banter = random.choice([
            "Sounds delightful!",
            "Can't wait to see the kids.",
            "Weather forecast says sunny and crisp.",
            "Grandma sends her love to everyone ❤️",
            "Remember to bring your board games!",
            "I'm bringing Scrabble and Monopoly.",
            "Looking forward to it!",
            "Love you all!",
        ])
        lines.append(f"10/22/26, 10:{i:02d} - {sender}: {banter}")

    out_file = SYNTHETIC_DIR / "sample_family_thanksgiving.txt"
    out_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated {out_file.name} ({len(lines)} messages)")


def generate_class_council_5000():
    """Generates a 5,000-message academic student group chat to benchmark unattended processing."""
    students = [
        "Marcus O'Connor", "Prof. Henderson", "Elena Rostova", "Kevin Zhang",
        "Priya Patel", "Liam Smith", "Chloe Martin", "Lucas Silva",
        "Amina Diallo", "Noah Kim", "Hannah Abbott", "Jack Dawson"
    ]
    chat_lines = [
        "[01/10/2026, 08:30:00] Marcus O'Connor: Welcome everyone to the CS301 Class Forum for Fall 2026.",
        "[01/10/2026, 08:31:12] Prof. Henderson: Welcome students. Important syllabus note: Lab 1 report is due on Friday Oct 16 at 5:00 PM.",
        "[01/10/2026, 08:32:00] Kevin Zhang: Thanks Professor. Marcus, can you please upload the lecture slides to the shared drive?",
        "[01/10/2026, 08:33:05] Marcus O'Connor: Uploading slides right now.",
    ]

    # Insert periodic critical dates and action items at known lines
    milestones = {
        500: ("Prof. Henderson", "Midterm Examination will take place on Wednesday Nov 04 from 10 AM to 12 PM in Hall B."),
        1200: ("Elena Rostova", "Marcus, please reserve Room 302 for our study group session on Monday Nov 02 at 4 PM."),
        2500: ("Prof. Henderson", "Final project proposal deadline has been extended to Friday Nov 20 at midnight."),
        3800: ("Priya Patel", "Team leads must submit team member roster to TA Kevin by Thursday Nov 12 at 3 PM."),
        4800: ("Marcus O'Connor", "Reminder: Course feedback survey closes on Monday Nov 30 at 11:59 PM."),
    }

    banter_phrases = [
        "Has anyone solved question 3?",
        "Check equation 4.2 in the textbook",
        "Thanks!",
        "Understood 👍",
        "Office hours are on Tuesday at 2 PM",
        "Coffee break time",
        "Good luck with the assignment",
        "Working on the proof now",
        "See you in lecture",
        "Does anyone have an extra notebook?",
        "The code compiles without errors now",
        "Don't forget to push your git tags",
    ]

    day = 1
    hour = 9
    minute = 0

    for i in range(5, 5001):
        minute += 1
        if minute >= 60:
            minute = 0
            hour += 1
            if hour >= 22:
                hour = 8
                day += 1

        date_str = f"[{day:02d}/10/2026, {hour:02d}:{minute:02d}:{random.randint(10, 59):02d}]"

        if i in milestones:
            sender, text = milestones[i]
            chat_lines.append(f"{date_str} {sender}: {text}")
        else:
            sender = random.choice(students)
            text = random.choice(banter_phrases)
            chat_lines.append(f"{date_str} {sender}: {text}")

    out_file = SYNTHETIC_DIR / "sample_class_council_5000.txt"
    out_file.write_text("\n".join(chat_lines), encoding="utf-8")
    print(f"Generated {out_file.name} ({len(chat_lines)} messages)")


if __name__ == "__main__":
    generate_hackathon_sample()
    generate_family_sample()
    generate_class_council_5000()
