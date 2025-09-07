from flask import Flask, render_template, request, redirect, url_for, flash
import os
import telebot
from config import BOT_TOKEN, MARZBAN_URL, MARZBAN_USER, MARZBAN_PASS

app = Flask(__name__)
app.secret_key = "vpn_secret"

bot = telebot.TeleBot(BOT_TOKEN)

# صفحه اصلی
@app.route("/")
def index():
    return render_template("index.html")

# آپلود رسید
@app.route("/upload", methods=["GET", "POST"])
def upload_receipt():
    if request.method == "POST":
        file = request.files["receipt"]
        username = request.form["username"]
        if file:
            path = os.path.join("static/receipts", file.filename)
            file.save(path)
            flash("رسید شما با موفقیت ارسال شد. پس از تایید، اشتراک ارسال می‌شود.", "success")

            # پیام به ادمین
            bot.send_message(
                "<ADMIN_CHAT_ID>",
                f"📥 رسید جدید از کاربر: {username}\n\nبرای تایید وارد پنل شوید."
            )

            return redirect(url_for("index"))
    return render_template("upload_receipt.html")

# پنل ادمین برای تایید
@app.route("/admin")
def admin_panel():
    # اینجا می‌تونی لیست رسیدها رو نشون بدی و گزینه تایید بذاری
    return render_template("admin_panel.html")

if __name__ == "__main__":
    os.makedirs("static/receipts", exist_ok=True)
    app.run(host="0.0.0.0", port=5000)