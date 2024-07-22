import os
import time
import google.generativeai as genai
from sqlalchemy.orm import Session
from app.models.user import DBUser


def generate_ai_reply(
    post_content: str, comment_content: str, user_id: int, db: Session
) -> str:
    user = db.query(DBUser).filter(DBUser.id == user_id).first()

    if user and user.auto_reply:
        time.sleep(user.reply_delay)

    genai.configure(api_key=os.environ["GOOGLE_AI_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = (
        f"Generate a relevant reply to the comment based on the post content.\n\n"
        f"Post: {post_content}\n"
        f"Comment: {comment_content}\n"
        f"Reply:"
    )
    response = model.generate_content(prompt)
    return response.text
