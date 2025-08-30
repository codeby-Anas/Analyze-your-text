import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox, ttk
from collections import Counter
import re
import os

def analyze_text():
    text = text_input.get("1.0", tk.END).strip()
    
    if not text:
        result_label.config(text="⚠️ من فضلك أدخل نص لتحليله.")
        return

    total_chars = len(text)
    chars_no_spaces = len(text.replace(" ", "").replace("\n", ""))
    words = re.findall(r'\b\w+\b', text)
    total_words = len(words)
    sentences = re.split(r'[.!?]+', text)
    sentences = [s for s in sentences if s.strip()]
    total_sentences = len(sentences)
    word_counts = Counter(word.lower() for word in words)
    most_common_words = word_counts.most_common(5)

    # متوسط طول الكلمة
    avg_word_length = (sum(len(w) for w in words) / total_words) if total_words else 0

    # كثافة الحروف (بدون فراغات / عدد الكلمات)
    char_density = (chars_no_spaces / total_words) if total_words else 0

    # كلمات فريدة (ظهرت مرة واحدة فقط)
    unique_words_count = sum(1 for count in word_counts.values() if count == 1)

    global last_result_text
    last_result_text = (
        f"عدد الحروف (مع الفراغات): {total_chars}\n"
        f"عدد الحروف (بدون الفراغات): {chars_no_spaces}\n"
        f"عدد الكلمات: {total_words}\n"
        f"عدد الجمل: {total_sentences}\n"
        f"متوسط طول الكلمة: {avg_word_length:.2f} حرف\n"
        f"كثافة الحروف (بدون فراغات لكل كلمة): {char_density:.2f}\n"
        f"عدد الكلمات الفريدة (مرة واحدة فقط): {unique_words_count}\n"
        f"الكلمات الأكثر تكراراً:\n"
    )
    for word, count in most_common_words:
        last_result_text += f" • {word}: {count} مرة\n"

    result_label.config(text=last_result_text)

def clear_text():
    text_input.delete("1.0", tk.END)
    result_label.config(text="")

def save_results():
    if not last_result_text:
        messagebox.showwarning("تنبيه", "لا يوجد نتائج للحفظ. يرجى تحليل نص أولاً.")
        return
    
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("ملفات نصية", "*.txt")],
                                             title="احفظ نتائج التحليل")
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("نتائج تحليل النص:\n\n")
                f.write(last_result_text)
            messagebox.showinfo("تم الحفظ", f"تم حفظ النتائج في الملف:\n{file_path}")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء الحفظ:\n{e}")

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("ملفات نصية", "*.txt *.md *.py *.csv *.json")],
                                           title="اختر ملف نصي للتحميل")
    if file_path:
        try:
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            if size_mb > 5:
                messagebox.showwarning("تنبيه", "الملف كبير جداً (أكبر من 5 ميجابايت). قد يتسبب في بطء التطبيق.")
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            text_input.delete("1.0", tk.END)
            text_input.insert(tk.END, content)
            result_label.config(text="تم تحميل النص من الملف. اضغط 'تحليل النص' لتحليل المحتوى.")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء تحميل الملف:\n{e}")

def clean_text():
    text = text_input.get("1.0", tk.END).strip()
    if not text:
        messagebox.showinfo("تنبيه", "لا يوجد نص لتنظيفه.")
        return
    # تحويل النص لحروف صغيرة وإزالة التكرار مع الحفاظ على الترتيب
    words = re.findall(r'\b\w+\b', text.lower())
    unique_words_ordered = []
    seen = set()
    for w in words:
        if w not in seen:
            unique_words_ordered.append(w)
            seen.add(w)
    cleaned_text = " ".join(unique_words_ordered)
    text_input.delete("1.0", tk.END)
    text_input.insert(tk.END, cleaned_text)
    result_label.config(text="تم تنظيف النص (توحيد حروف وإزالة التكرار).")

def change_font(event=None):
    selected_font = font_combo.get()
    selected_size = size_combo.get()
    text_input.config(font=(selected_font, selected_size))
    result_label.config(font=(selected_font, selected_size-1))

# متغير لتخزين آخر نتائج التحليل
last_result_text = ""

# إعداد واجهة المستخدم
root = tk.Tk()
root.title("محلل النصوص المتقدم")
root.geometry("700x600")
root.configure(bg="#f0f4f8")

title_label = tk.Label(root, text="محلل النصوص المتقدم", font=("Segoe UI", 22, "bold"), bg="#f0f4f8", fg="#2c3e50")
title_label.pack(pady=10)

# إطار التحكم في الخط
font_frame = tk.Frame(root, bg="#f0f4f8")
font_frame.pack(pady=5)

tk.Label(font_frame, text="نوع الخط:", font=("Segoe UI", 12), bg="#f0f4f8").grid(row=0, column=0, padx=5)
font_combo = ttk.Combobox(font_frame, values=["Segoe UI", "Arial", "Courier New", "Times New Roman", "Tahoma"], state="readonly", width=15)
font_combo.current(0)
font_combo.grid(row=0, column=1, padx=5)
font_combo.bind("<<ComboboxSelected>>", change_font)

tk.Label(font_frame, text="حجم الخط:", font=("Segoe UI", 12), bg="#f0f4f8").grid(row=0, column=2, padx=5)
size_combo = ttk.Combobox(font_frame, values=[10, 12, 14, 16, 18, 20, 22], state="readonly", width=5)
size_combo.current(2)
size_combo.grid(row=0, column=3, padx=5)
size_combo.bind("<<ComboboxSelected>>", change_font)

text_frame = tk.Frame(root)
text_frame.pack(padx=15, pady=5, fill=tk.BOTH, expand=True)

text_input = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, font=("Segoe UI", 14), height=12, bg="#ffffff", fg="#34495e", relief=tk.GROOVE, borderwidth=2)
text_input.pack(fill=tk.BOTH, expand=True)

button_frame = tk.Frame(root, bg="#f0f4f8")
button_frame.pack(pady=10)

analyze_button = tk.Button(button_frame, text="🔍 تحليل النص", font=("Segoe UI", 14), bg="#27ae60", fg="white", activebackground="#2ecc71", activeforeground="white", command=analyze_text, width=15)
analyze_button.grid(row=0, column=0, padx=8, pady=5)

clear_button = tk.Button(button_frame, text="🧹 مسح النص", font=("Segoe UI", 14), bg="#c0392b", fg="white", activebackground="#e74c3c", activeforeground="white", command=clear_text, width=15)
clear_button.grid(row=0, column=1, padx=8, pady=5)

clean_button = tk.Button(button_frame, text="✨ تنظيف النص", font=("Segoe UI", 14), bg="#d35400", fg="white", activebackground="#e67e22", activeforeground="white", command=clean_text, width=15)
clean_button.grid(row=0, column=2, padx=8, pady=5)

save_button = tk.Button(button_frame, text="💾 حفظ النتائج", font=("Segoe UI", 14), bg="#2980b9", fg="white", activebackground="#3498db", activeforeground="white", command=save_results, width=15)
save_button.grid(row=1, column=0, padx=8, pady=10)

load_button = tk.Button(button_frame, text="📂 تحميل ملف نصي", font=("Segoe UI", 14), bg="#8e44ad", fg="white", activebackground="#9b59b6", activeforeground="white", command=load_file, width=15)
load_button.grid(row=1, column=1, padx=8, pady=10)

result_frame = tk.Frame(root, bg="#ecf0f1", relief=tk.RIDGE, borderwidth=2)
result_frame.pack(padx=15, pady=10, fill=tk.BOTH, expand=True)

result_label = tk.Label(result_frame, text="", font=("Segoe UI", 13), bg="#ecf0f1", fg="#2c3e50", justify=tk.LEFT, anchor="nw")
result_label.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

root.mainloop()













