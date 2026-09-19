
import streamlit as st
import json
import os
import re
import hashlib
from datetime import date, datetime
from difflib import SequenceMatcher
from PIL import Image, ImageOps
from io import BytesIO

# ---------------- CONFIG ----------------

st.set_page_config(
    page_title="AI Lost & Found",
    page_icon="🔎",
    layout="wide"
)

DATA_FILE = "reports.json"
IMAGE_DIR = "item_images"

os.makedirs(IMAGE_DIR, exist_ok=True)

# ---------------- STORAGE ----------------

def load_reports():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def save_reports(reports):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(reports, f, indent=2, ensure_ascii=False)


def save_image(uploaded_file):
    if uploaded_file is None:
        return ""

    image = Image.open(uploaded_file).convert("RGB")
    filename = hashlib.sha256(
        uploaded_file.getvalue()
    ).hexdigest()[:20] + ".jpg"

    path = os.path.join(IMAGE_DIR, filename)
    image.save(path, "JPEG", quality=85)

    return path


# ---------------- TEXT MATCHING ----------------

def clean_text(text):
    text = (text or "").lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return " ".join(text.split())


def text_similarity(text1, text2):
    """
    Combines word overlap and sequence similarity.
    Returns a score between 0 and 1.
    """

    a = clean_text(text1)
    b = clean_text(text2)

    if not a or not b:
        return 0.0

    words_a = set(a.split())
    words_b = set(b.split())

    overlap = len(words_a & words_b) / max(
        len(words_a | words_b), 1
    )

    sequence = SequenceMatcher(None, a, b).ratio()

    return 0.65 * overlap + 0.35 * sequence


# ---------------- IMAGE MATCHING ----------------

def image_hash(image):
    """
    Creates a simple perceptual difference hash.
    Similar-looking images may have similar hashes.
    """

    image = ImageOps.grayscale(image)
    image = image.resize((9, 8))

    pixels = list(image.getdata())
    bits = []

    for row in range(8):
        for col in range(8):
            left = pixels[row * 9 + col]
            right = pixels[row * 9 + col + 1]
            bits.append(left > right)

    return bits


def image_similarity(path1, path2):
    if not path1 or not path2:
        return None

    if not os.path.exists(path1) or not os.path.exists(path2):
        return None

    try:
        with Image.open(path1) as img1:
            hash1 = image_hash(img1.copy())

        with Image.open(path2) as img2:
            hash2 = image_hash(img2.copy())

        differences = sum(a != b for a, b in zip(hash1, hash2))

        return 1 - differences / len(hash1)

    except Exception:
        return None


# ---------------- MATCH SCORING ----------------

def calculate_match(lost, found):
    """
    Combines text, location, and optional image similarity.
    Returns score and matching reasons.
    """

    item_score = text_similarity(
        lost.get("item", ""),
        found.get("item", "")
    )

    description_score = text_similarity(
        lost.get("description", ""),
        found.get("description", "")
    )

    location_score = text_similarity(
        lost.get("location", ""),
        found.get("location", "")
    )

    image_score = image_similarity(
        lost.get("image", ""),
        found.get("image", "")
    )

    # Weighted text and location score
    score = (
        0.40 * item_score
        + 0.35 * description_score
        + 0.15 * location_score
    )

    # Include image comparison only when both images exist.
    if image_score is not None:
        score = (
            0.90 * score
            + 0.10 * image_score
        )

    score = max(0.0, min(score, 1.0))

    reasons = []

    if item_score >= 0.35:
        reasons.append("Similar item name")

    if description_score >= 0.25:
        reasons.append("Similar description")

    if location_score >= 0.35:
        reasons.append("Similar location")

    if image_score is not None and image_score >= 0.70:
        reasons.append("Similar image patterns")

    return score, reasons


def get_matches(lost, reports):
    matches = []

    for report in reports:
        if report.get("type") != "Found":
            continue

        score, reasons = calculate_match(lost, report)

        matches.append({
            "report": report,
            "score": score,
            "reasons": reasons
        })

    matches.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return matches


# ---------------- HEADER ----------------

st.title("🔎 AI Lost & Found")
st.write(
    "Report lost and found items, discover possible matches, "
    "and connect with the person who reported the item."
)

st.info(
    "For railway stations, colleges, public places, and other "
    "locations. Contact the reporter and verify ownership "
    "before collecting an item."
)

reports = load_reports()

# ---------------- NAVIGATION ----------------

tab1, tab2, tab3 = st.tabs([
    "📝 Report an Item",
    "🔍 Find Matches",
    "📋 Browse Reports"
])


# ==================================================
# TAB 1: REPORT ITEM
# ==================================================

with tab1:
    st.header("Report a Lost or Found Item")

    with st.form("report_form", clear_on_submit=True):

        report_type = st.radio(
            "What are you reporting?",
            ["Lost", "Found"],
            horizontal=True
        )

        item_name = st.text_input(
            "Item name *",
            placeholder="e.g. Brown leather wallet"
        )

        description = st.text_area(
            "Description *",
            placeholder=(
                "Describe colour, brand, identifying marks, "
                "contents, or other details..."
            )
        )

        location = st.text_input(
            "Location *",
            placeholder="e.g. Dadar Railway Station, Platform 2"
        )

        report_date = st.date_input(
            "Date item was lost/found",
            value=date.today()
        )

        uploaded_image = st.file_uploader(
            "Upload item image (optional)",
            type=["jpg", "jpeg", "png"]
        )

        reporter_name = st.text_input(
            "Your name *"
        )

        reporter_contact = st.text_input(
            "Contact information *",
            placeholder="Phone number or email"
        )

        submitted = st.form_submit_button(
            "Submit Report",
            use_container_width=True
        )

        if submitted:
            if not all([
                item_name.strip(),
                description.strip(),
                location.strip(),
                reporter_name.strip(),
                reporter_contact.strip()
            ]):
                st.error(
                    "Please fill in all required fields."
                )

            else:
                image_path = ""

                if uploaded_image is not None:
                    image_path = save_image(uploaded_image)

                new_report = {
                    "id": hashlib.sha256(
                        (
                            item_name
                            + location
                            + str(datetime.now())
                        ).encode()
                    ).hexdigest()[:10],

                    "type": report_type,
                    "item": item_name.strip(),
                    "description": description.strip(),
                    "location": location.strip(),
                    "date": str(report_date),
                    "image": image_path,
                    "name": reporter_name.strip(),
                    "contact": reporter_contact.strip(),
                    "created": str(datetime.now())
                }

                reports.append(new_report)
                save_reports(reports)

                st.success(
                    f"{report_type} item report submitted!"
                )

                st.rerun()


# ==================================================
# TAB 2: FIND MATCHES
# ==================================================

with tab2:
    st.header("🔍 Find Possible Matches")

    lost_reports = [
        r for r in reports
        if r.get("type") == "Lost"
    ]

    if not lost_reports:
        st.info(
            "No lost-item reports yet. Submit a Lost report "
            "in the first tab to find possible matches."
        )

    else:
        lost_options = {
            (
                f'{r["item"]} — {r["location"]} '
                f'({r["date"]})'
            ): r
            for r in lost_reports
        }

        selected_label = st.selectbox(
            "Select your lost-item report",
            list(lost_options.keys())
        )

        lost = lost_options[selected_label]

        with st.container(border=True):
            st.subheader("Your Lost Item")

            st.write(f'**Item:** {lost["item"]}')
            st.write(f'**Description:** {lost["description"]}')
            st.write(f'**Location:** {lost["location"]}')
            st.write(f'**Date:** {lost["date"]}')

            if lost.get("image") and os.path.exists(lost["image"]):
                st.image(
                    lost["image"],
                    caption="Your uploaded item",
                    width=220
                )

        if st.button(
            "Find Matching Found Reports",
            type="primary",
            use_container_width=True
        ):
            matches = get_matches(lost, reports)

            st.session_state["matches"] = matches
            st.session_state["selected_lost_id"] = lost["id"]

        if (
            "matches" in st.session_state
            and st.session_state.get("selected_lost_id") == lost["id"]
        ):
            matches = st.session_state["matches"]

            st.divider()
            st.subheader("Possible Matches")

            # Avoid showing weak matches as if they were reliable.
            relevant_matches = [
                m for m in matches
                if m["score"] >= 0.20
            ]

            if not relevant_matches:
                st.warning(
                    "No strong possible matches found yet. "
                    "Try checking again later as new found-item "
                    "reports are submitted."
                )

            else:
                st.caption(
                    "Results are sorted by estimated similarity. "
                    "Scores are not probabilities of ownership."
                )

                for index, match in enumerate(
                    relevant_matches, start=1
                ):
                    found = match["report"]
                    score = match["score"]
                    reasons = match["reasons"]

                    with st.container(border=True):
                        col1, col2 = st.columns([3, 1])

                        with col1:
                            st.subheader(
                                f"{index}. {found['item']}"
                            )

                        with col2:
                            st.metric(
                                "Match score",
                                f"{score * 100:.0f}%"
                            )

                        st.progress(score)

                        if reasons:
                            st.write(
                                "**Why it matched:** "
                                + ", ".join(reasons)
                            )
                        else:
                            st.write(
                                "**Why it matched:** "
                                "Some text or location similarity "
                                "was detected."
                            )

                        st.write(
                            f'**Description:** {found["description"]}'
                        )
                        st.write(
                            f'**Found at:** {found["location"]}'
                        )
                        st.write(
                            f'**Date:** {found["date"]}'
                        )

                        if (
                            found.get("image")
                            and os.path.exists(found["image"])
                        ):
                            st.image(
                                found["image"],
                                caption="Found item image",
                                width=250
                            )

                        st.markdown("#### Contact the reporter")

                        st.write(
                            f'**Name:** {found["name"]}'
                        )
                        st.write(
                            f'**Contact:** {found["contact"]}'
                        )

                        st.caption(
                            "Contact the reporter to verify "
                            "the item. Do not share sensitive "
                            "personal information publicly."
                        )


# ==================================================
# TAB 3: BROWSE REPORTS
# ==================================================

with tab3:
    st.header("📋 Browse Lost & Found Reports")

    filter_type = st.selectbox(
        "Filter reports",
        ["All", "Lost", "Found"]
    )

    search_text = st.text_input(
        "Search by item or location"
    )

    visible_reports = reports

    if filter_type != "All":
        visible_reports = [
            r for r in visible_reports
            if r.get("type") == filter_type
        ]

    if search_text.strip():
        query = clean_text(search_text)

        visible_reports = [
            r for r in visible_reports
            if query in clean_text(
                r.get("item", "") + " "
                + r.get("description", "") + " "
                + r.get("location", "")
            )
        ]

    st.caption(
        f"{len(visible_reports)} report(s) found"
    )

    if not visible_reports:
        st.info("No reports match your search.")

    for report in reversed(visible_reports):
        with st.container(border=True):
            st.subheader(
                f'{report["type"]}: {report["item"]}'
            )

            st.write(
                f'**Description:** {report["description"]}'
            )
            st.write(
                f'**Location:** {report["location"]}'
            )
            st.write(
                f'**Date:** {report["date"]}'
            )

            if (
                report.get("image")
                and os.path.exists(report["image"])
            ):
                st.image(
                    report["image"],
                    width=200
                )

            st.write(
                f'**Reporter:** {report["name"]}'
            )
            st.write(
                f'**Contact:** {report["contact"]}'
            )

# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "AI Lost & Found | Prototype for lost-item reporting "
    "and possible-match discovery."
)
