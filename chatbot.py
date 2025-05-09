import tkinter as tk
import requests
import threading
from datetime import datetime

# دالة لحفظ الحادثة في سجل (ملف نصي)
def save_to_log(user_input, answer):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("chat_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"{current_time} - أنت: {user_input}\n")
        log_file.write(f"{current_time} - شات بوت: {answer}\n\n")

# دالة لإضافة رسالة إلى واجهة الشات بطريقة آمنة
def append_to_chat(text):
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, text)
    chat_area.config(state=tk.DISABLED)
    chat_area.yview(tk.END)  # التمرير لآخر الرسائل

# دالة لإرسال السؤال إلى Ollama واستلام الجواب
def ask_ollama():
    user_input = entry.get()
    if not user_input.strip():
        return

    append_to_chat(f"أنت: {user_input}\n")
    entry.delete(0, tk.END)

    def fetch_response():
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3.2",
                    "prompt": user_input,
                    "stream": False
                }
            )
            data = response.json()
            answer = data.get("response", "لم يتم الحصول على رد.")
        except Exception as e:
            answer = f"حدث خطأ: {e}"

        append_to_chat(f"شات بوت: {answer}\n\n")
        save_to_log(user_input, answer)

    threading.Thread(target=fetch_response).start()

# إنشاء نافذة البرنامج
window = tk.Tk()
window.title("شات بوت ذكي - LLaMA3.2")
window.geometry("500x500")

# منطقة الشات
chat_area = tk.Text(window, wrap=tk.WORD, state=tk.DISABLED, height=20, width=70)
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# رسالة ترحيبية
append_to_chat("مرحبًا بك في الشات بوت! يمكنك الآن طرح أسئلتك وسأجيب عليها.\n\n")

# خانة الإدخال
entry = tk.Entry(window, font=("Arial", 12), width=60)
entry.pack(padx=10, pady=5, fill=tk.X)

# زر الإرسال
send_button = tk.Button(window, text="إرسال", command=ask_ollama)
send_button.pack(pady=5)

# منع الكتابة داخل منطقة الشات
chat_area.bind("<Key>", lambda e: "break")

# تشغيل البرنامج
window.mainloop()
