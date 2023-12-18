import tkinter as tk
from tkinter import ttk
import time


class TypingSpeedApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Typing Speed Calculator")
        self.master.geometry("700x450")

        style = ttk.Style()
        style.configure('TFrame', borderwidth=10, relief='flat', background='#e7e7e7')
        style.configure('TLabel', background='#e7e7e7')
        style.configure('TButton', padding=10, relief='flat', background='#4CAF50', foreground='black')
        style.map('TButton', background=[('active', '#45a049')])

        self.frame = ttk.Frame(self.master, style='TFrame')
        self.frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.sentence_label = ttk.Label(self.frame, text="Type the following sentences one by one:", style='TLabel')
        self.sentence_label.pack(pady=10)

        self.sentence = (
            "The quick brown fox jumps over the lazy dog.\n"
            "Pack my box with five dozen liquor jugs.\n"
            "How razorback-jumping frogs can level six piqued gymnasts!"
        )
        self.sentence_display = ttk.Label(self.frame, text=self.sentence, font=("Helvetica", 12), style='TLabel')
        self.sentence_display.pack(pady=10)

        self.text_widget = tk.Text(self.frame, wrap=tk.WORD, height=5, width=60, font=("Helvetica", 12))
        self.text_widget.pack(pady=10)

        button_frame = ttk.Frame(self.frame, style='TFrame')
        button_frame.pack(pady=10)

        self.start_button = ttk.Button(button_frame, text="Start Typing Test", command=self.start_typing_test,
                                       style='TButton')
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = ttk.Button(button_frame, text="Reset", command=self.reset, style='TButton',
                                       state=tk.DISABLED)
        self.reset_button.pack(side=tk.LEFT, padx=5)

        self.result_label = ttk.Label(self.frame, text="", style='TLabel')
        self.result_label.pack(pady=10)

        self.timer_label = ttk.Label(self.frame, text="", font=("Helvetica", 12), style='TLabel')
        self.timer_label.pack()

        self.start_time = 0
        self.timer_running = False

    def start_typing_test(self):
        if not self.timer_running:
            self.start_button.config(state=tk.DISABLED)
            self.reset_button.config(state=tk.NORMAL)
            self.text_widget.delete(1.0, tk.END)
            self.result_label.config(text="")
            self.timer_label.config(text="Time left: 60 seconds")

            self.start_time = time.time()
            self.timer_running = True
            self.master.after(1000, self.update_timer)

    def update_timer(self):
        elapsed_time = int(time.time() - self.start_time)
        remaining_time = max(60 - elapsed_time, 0)

        self.timer_label.config(text=f"Time left: {remaining_time} seconds")

        if remaining_time > 0 and self.timer_running:
            self.master.after(1000, self.update_timer)
        else:
            self.end_typing_test()

    def end_typing_test(self):
        self.timer_running = False

        typed_text = self.text_widget.get("1.0", tk.END)
        words_per_minute = (len(typed_text.split()) / 60) * 60  # Words per minute

        accuracy = self.calculate_accuracy(typed_text, self.sentence)

        result_text = f"Typing Speed: {words_per_minute:.2f} words per minute\nAccuracy: {accuracy:.2f}%"
        self.result_label.config(text=result_text)
        self.start_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.DISABLED)

    def reset(self):
        self.timer_running = False
        self.text_widget.delete(1.0, tk.END)
        self.result_label.config(text="")
        self.start_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.DISABLED)
        self.timer_label.config(text="Time left: 60 seconds")

    def calculate_accuracy(self, typed_text, original_text):
        correct_words = sum(a == b for a, b in zip(typed_text.split(), original_text.split()))
        total_words = len(original_text.split())
        accuracy_percentage = (correct_words / total_words) * 100
        return accuracy_percentage


if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedApp(root)
    root.mainloop()
