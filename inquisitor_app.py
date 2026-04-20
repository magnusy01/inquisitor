import os
import threading
import tkinter as tk
from tkinter import font, scrolledtext, ttk

from dotenv import load_dotenv
from openai import OpenAI


ENGINES = {
    "Claude Opus (云端)": {
        "base_url": "https://openrouter.ai/api/v1",
        "model": "anthropic/claude-opus-4.6",
        "api_key_env": "OPENROUTER_API_KEY",
    },
    "DeepSeek (云端)": {
        "base_url": "https://api.deepseek.com",
        "model": "deepseek-chat",
        "api_key_env": "DEEPSEEK_API_KEY",
    },
    "Gemma 4 E4B (本地)": {
        "base_url": "http://localhost:11434/v1",
        "model": "huihui_ai/gemma-4-abliterated:e4b",
        "api_key_env": None,
    },
}

DEFAULT_ENGINE = "Claude Opus (云端)"
SPINNER_FRAMES = ["|", "/", "-", "\\"]

TITLE_LINE = "I N Q U I S I T O R"
SUBTITLE_LINE = "审 查 官"
SCRIPTURE_LINE = (
    "「我岂没有吩咐你吗？你当刚强壮胆！不要惧怕，也不要惊惶；"
    "因为你无论往哪里去，耶和华你的神必与你同在。」── 约书亚记 1:9"
)
SIGNATURE_LINE = "Authored by magnusy · v2.0"


def load_taste_text() -> str:
    with open("taste.json", "r", encoding="utf-8") as file:
        return file.read().strip()


def build_prompt(taste_text: str, movie: str) -> str:
    return f"""你是一位电影内容审查官，为用户服务。

以下是审查官的工作手册（原文照录，请自行理解其结构与规则）：
{taste_text}

现在用户想看《{movie}》。

请基于你对这部电影的知识，扫描全片，告诉用户哪些场景可能让其不适。
输出格式：
- 不适等级总评（轻微/中等/严重/无）
- 具体场景列表（大概时间点 + 类型 + 严重程度 + 简短描述，不剧透）
- 观看建议（直接看/开头小心/某段快进/换一部）

回答请简洁，不要废话。"""


class InquisitorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.is_running = False
        self.run_id = 0
        self.spinner_index = 0

        load_dotenv()

        root.title("INQUISITOR 审查官 v1.3")
        root.geometry("920x780")
        root.configure(bg="#1a1a1a")

        ui_font = font.Font(family="PingFang SC", size=12)
        logo_title_font = font.Font(family="Menlo", size=22, weight="bold")
        logo_subtitle_font = font.Font(family="PingFang SC", size=14, weight="bold")
        logo_scripture_font = font.Font(family="PingFang SC", size=11, slant="italic")
        logo_signature_font = font.Font(family="Menlo", size=11)

        logo_frame = tk.Frame(root, bg="#d4af37")
        logo_frame.pack(pady=14, padx=40, fill=tk.X)
        logo_inner = tk.Frame(logo_frame, bg="#1a1a1a")
        logo_inner.pack(padx=2, pady=2, fill=tk.X)

        tk.Label(
            logo_inner,
            text=TITLE_LINE,
            font=logo_title_font,
            fg="#d4af37",
            bg="#1a1a1a",
            justify=tk.CENTER,
        ).pack(pady=(16, 2))
        tk.Label(
            logo_inner,
            text=SUBTITLE_LINE,
            font=logo_subtitle_font,
            fg="#d4af37",
            bg="#1a1a1a",
            justify=tk.CENTER,
        ).pack(pady=(0, 10))
        tk.Label(
            logo_inner,
            text=SCRIPTURE_LINE,
            font=logo_scripture_font,
            fg="#d4af37",
            bg="#1a1a1a",
            justify=tk.CENTER,
            wraplength=780,
        ).pack(pady=(0, 8))
        tk.Label(
            logo_inner,
            text=SIGNATURE_LINE,
            font=logo_signature_font,
            fg="#8f8f8f",
            bg="#1a1a1a",
            justify=tk.CENTER,
        ).pack(pady=(0, 16))

        input_frame = tk.Frame(root, bg="#1a1a1a")
        input_frame.pack(pady=10, fill=tk.X, padx=30)

        tk.Label(input_frame, text="引擎：", font=ui_font, fg="#d4af37", bg="#1a1a1a").pack(
            side=tk.LEFT
        )
        self.engine_var = tk.StringVar(value=DEFAULT_ENGINE)
        self.engine_menu = ttk.Combobox(
            input_frame,
            textvariable=self.engine_var,
            values=list(ENGINES.keys()),
            state="readonly",
            width=24,
            font=ui_font,
        )
        self.engine_menu.pack(side=tk.LEFT, padx=(5, 15))

        tk.Label(input_frame, text="电影：", font=ui_font, fg="#d4af37", bg="#1a1a1a").pack(
            side=tk.LEFT
        )
        self.movie_entry = tk.Entry(
            input_frame,
            font=ui_font,
            bg="#0f0f0f",
            fg="#d4af37",
            insertbackground="#d4af37",
            relief=tk.FLAT,
            bd=8,
        )
        self.movie_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        self.movie_entry.bind("<Return>", lambda _: self.toggle_review())

        self.action_button = tk.Button(
            input_frame,
            text="审查",
            font=ui_font,
            bg="#d4af37",
            fg="#1a1a1a",
            activebackground="#c8a82f",
            activeforeground="#1a1a1a",
            relief=tk.FLAT,
            command=self.toggle_review,
            padx=22,
        )
        self.action_button.pack(side=tk.LEFT)

        self.status_label = tk.Label(
            root,
            text="等待输入电影名...",
            font=ui_font,
            fg="#d4af37",
            bg="#1a1a1a",
        )
        self.status_label.pack(pady=5)

        self.output = scrolledtext.ScrolledText(
            root,
            font=ui_font,
            bg="#0f0f0f",
            fg="#d4af37",
            insertbackground="#d4af37",
            relief=tk.FLAT,
            padx=15,
            pady=15,
            wrap=tk.WORD,
        )
        self.output.pack(fill=tk.BOTH, expand=True, padx=30, pady=15)
        self.movie_entry.focus_set()

    def toggle_review(self) -> None:
        if self.is_running:
            self.stop_review()
        else:
            self.start_review()

    def start_review(self) -> None:
        movie = self.movie_entry.get().strip()
        if not movie:
            self.status_label.config(text="请输入电影名。", fg="#d4af37")
            return

        self.is_running = True
        self.run_id += 1
        current_run_id = self.run_id

        self.action_button.config(text="停止", bg="#8f3b3b", activebackground="#7a3333")
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, f"开始审查：《{movie}》\n\n")

        self.spinner_index = 0
        self.update_spinner(current_run_id, movie)

        worker = threading.Thread(target=self.call_api, args=(movie, current_run_id), daemon=True)
        worker.start()

    def stop_review(self) -> None:
        if not self.is_running:
            return
        self.is_running = False
        self.status_label.config(text="审查已停止。", fg="#d4af37")
        self.action_button.config(text="审查", bg="#d4af37", activebackground="#c8a82f")
        self.output.insert(tk.END, "\n\n[用户已停止本次审查]")

    def update_spinner(self, run_id: int, movie: str) -> None:
        if not self.is_running or run_id != self.run_id:
            return
        frame = SPINNER_FRAMES[self.spinner_index % len(SPINNER_FRAMES)]
        self.spinner_index += 1
        engine_name = self.engine_var.get()
        self.status_label.config(text=f"{frame} 审查中（{engine_name}）：《{movie}》", fg="#d4af37")
        self.root.after(120, self.update_spinner, run_id, movie)

    def resolve_api_key(self, engine_conf: dict) -> str:
        key_env = engine_conf["api_key_env"]
        if key_env is None:
            return "ollama"
        api_key = os.getenv(key_env, "").strip()
        if not api_key:
            raise RuntimeError(f"缺少环境变量 `{key_env}`，请先在 .env 中配置。")
        return api_key

    def call_api(self, movie: str, run_id: int) -> None:
        try:
            engine_conf = ENGINES[self.engine_var.get()]
            api_key = self.resolve_api_key(engine_conf)
            taste_text = load_taste_text()
            prompt = build_prompt(taste_text, movie)

            client = OpenAI(
                api_key=api_key,
                base_url=engine_conf["base_url"],
                timeout=180.0,
            )
            response = client.chat.completions.create(
                model=engine_conf["model"],
                messages=[{"role": "user", "content": prompt}],
            )
            result = response.choices[0].message.content or "(模型返回空内容)"
            self.root.after(0, self.show_result, run_id, result)
        except Exception as exc:
            self.root.after(0, self.show_error, run_id, str(exc))

    def show_result(self, run_id: int, result: str) -> None:
        if run_id != self.run_id or not self.is_running:
            return
        self.is_running = False
        self.action_button.config(text="审查", bg="#d4af37", activebackground="#c8a82f")
        self.status_label.config(text="审查完毕。", fg="#d4af37")
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, result)
        self.output.insert(tk.END, "\n\n" + "=" * 40 + "\n审查完毕，安心观影。")

    def show_error(self, run_id: int, error_message: str) -> None:
        if run_id != self.run_id or not self.is_running:
            return
        self.is_running = False
        self.action_button.config(text="审查", bg="#d4af37", activebackground="#c8a82f")
        self.status_label.config(text="审查失败。", fg="#d4af37")
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, f"出错了：\n\n{error_message}")


if __name__ == "__main__":
    root = tk.Tk()
    app = InquisitorApp(root)
    root.mainloop()
