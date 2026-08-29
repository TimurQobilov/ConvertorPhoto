import os
import sys
import webbrowser
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw

# Настройка темы интерфейса
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


def get_resource_path(relative_path):
    """ Вспомогательная функция для корректного пути к ресурсам внутри .exe """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def create_telegram_icon():
    """ Генерирует четкий фирменный логотип Telegram (синий круг с белым самолётиком) """
    size = 48
    img = Image.new("RGBA", (size, size), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Фирменный синий фоновый круг Telegram
    draw.ellipse([0, 0, size - 1, size - 1], fill=(34, 158, 217))

    # Полигон крыла бумажного самолетика (координаты точно по формуле)
    plane_points = [
        (11, 24),
        (37, 13),
        (30, 35),
        (23, 29),
        (19, 34),
        (19, 26),
    ]
    draw.polygon(plane_points, fill=(255, 255, 255))

    # Тень / сгиб на самолетике
    fold_points = [
        (23, 29),
        (19, 34),
        (23, 26)
    ]
    draw.polygon(fold_points, fill=(200, 220, 240))

    return img


class ImageResizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Понятное название приложения
        self.title("ФотоКонвертер — Ресайз и конвертация фото")
        self.geometry("600x530")
        self.resizable(False, False)

        # Подключение иконки окна приложения
        icon_path = get_resource_path("app_icon.ico")
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception:
                pass

        # Переменные настроек по умолчанию
        self.save_folder = ctk.StringVar(value=os.path.join(os.path.expanduser("~"), "Desktop"))
        self.target_width = ctk.StringVar(value="650")
        self.target_height = ctk.StringVar(value="650")
        self.target_format = ctk.StringVar(value="PNG")

        self._create_widgets()

    def _create_widgets(self):
        # Главный контейнер
        main_frame = ctk.CTkFrame(self, corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=(20, 10))

        # --- Секция Выбора файла ---
        self.drop_frame = ctk.CTkFrame(main_frame, fg_color=("gray85", "gray20"), height=130, corner_radius=10)
        self.drop_frame.pack(fill="x", padx=15, pady=15)
        self.drop_frame.pack_propagate(False)

        label_drop = ctk.CTkLabel(
            self.drop_frame, 
            text="Выберите фото для смены размера и формата", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        label_drop.pack(pady=(20, 10))

        btn_select_file = ctk.CTkButton(
            self.drop_frame, 
            text="📁 Обзор (выбрать фото)", 
            command=self.process_image
        )
        btn_select_file.pack()

        # --- Секция Настроек ---
        settings_frame = ctk.CTkFrame(main_frame)
        settings_frame.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        # Заголовок настроек
        settings_title = ctk.CTkLabel(
            settings_frame, 
            text="Параметры сохранения", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        settings_title.pack(anchor="w", padx=15, pady=(10, 10))

        # 1. Выбор папки для сохранения
        folder_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        folder_frame.pack(fill="x", padx=15, pady=5)

        lbl_folder = ctk.CTkLabel(folder_frame, text="Папка сохранения:", width=140, anchor="w")
        lbl_folder.pack(side="left")

        entry_folder = ctk.CTkEntry(folder_frame, textvariable=self.save_folder)
        entry_folder.pack(side="left", fill="x", expand=True, padx=5)

        btn_browse_folder = ctk.CTkButton(folder_frame, text="Изменить", width=80, command=self.browse_folder)
        btn_browse_folder.pack(side="right")

        # 2. Размер (Ширина x Высота)
        size_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        size_frame.pack(fill="x", padx=15, pady=5)

        lbl_size = ctk.CTkLabel(size_frame, text="Размер (Ш х В, px):", width=140, anchor="w")
        lbl_size.pack(side="left")

        entry_width = ctk.CTkEntry(size_frame, textvariable=self.target_width, width=80)
        entry_width.pack(side="left", padx=(0, 5))

        lbl_x = ctk.CTkLabel(size_frame, text="x")
        lbl_x.pack(side="left", padx=5)

        entry_height = ctk.CTkEntry(size_frame, textvariable=self.target_height, width=80)
        entry_height.pack(side="left", padx=(5, 0))

        # 3. Формат файла
        format_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        format_frame.pack(fill="x", padx=15, pady=5)

        lbl_format = ctk.CTkLabel(format_frame, text="Выходной формат:", width=140, anchor="w")
        lbl_format.pack(side="left")

        format_option = ctk.CTkOptionMenu(
            format_frame, 
            values=["PNG", "JPEG", "WEBP", "BMP"], 
            variable=self.target_format
        )
        format_option.pack(side="left")

        # Статусная строка
        self.status_label = ctk.CTkLabel(
            main_frame, 
            text="Готов к обработке", 
            text_color="gray"
        )
        self.status_label.pack(pady=(0, 5))

        # --- Блок Авторства с фирменным логотипом Telegram ---
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.pack(fill="x", side="bottom", pady=(0, 10))

        lbl_author = ctk.CTkLabel(
            footer_frame, 
            text="Разработал: ", 
            font=ctk.CTkFont(size=12)
        )
        lbl_author.pack(side="left", padx=(20, 0))

        # Создаем и конвертируем изображение Telegram для CTk
        tg_pil_img = create_telegram_icon()
        self.tg_icon_image = ctk.CTkImage(light_image=tg_pil_img, dark_image=tg_pil_img, size=(18, 18))

        # Картинка Telegram (кликабельная)
        tg_icon_label = ctk.CTkLabel(footer_frame, image=self.tg_icon_image, text="", cursor="hand2")
        tg_icon_label.pack(side="left", padx=(0, 5))
        tg_icon_label.bind("<Button-1>", lambda e: webbrowser.open_new_tab("https://t.me/timurqobilov"))

        # Текст ссылки Telegram (кликабельный)
        link_author = ctk.CTkLabel(
            footer_frame, 
            text="Тимур (@timurqobilov)", 
            font=ctk.CTkFont(size=12, weight="bold", underline=True),
            text_color=("#1D4ED8", "#60A5FA"),
            cursor="hand2"
        )
        link_author.pack(side="left")
        link_author.bind("<Button-1>", lambda e: webbrowser.open_new_tab("https://t.me/timurqobilov"))

    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.save_folder.get())
        if folder:
            self.save_folder.set(folder)

    def process_image(self):
        file_path = filedialog.askopenfilename(
            title="Выберите фото",
            filetypes=[("Изображения", "*.jpg *.jpeg *.png *.webp *.bmp *.tiff")]
        )
        
        if not file_path:
            return

        try:
            w = int(self.target_width.get())
            h = int(self.target_height.get())
            if w <= 0 or h <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Ширина и высота должны быть положительными целыми числами!")
            return

        save_dir = self.save_folder.get()
        if not os.path.exists(save_dir):
            try:
                os.makedirs(save_dir)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось создать папку:\n{e}")
                return

        fmt = self.target_format.get().lower()

        try:
            with Image.open(file_path) as img:
                if fmt in ["jpg", "jpeg"] and img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")

                resized_img = img.resize((w, h), Image.Resampling.LANCZOS)

                base_name = os.path.splitext(os.path.basename(file_path))[0]
                new_filename = f"{base_name}_{w}x{h}.{fmt}"
                output_path = os.path.join(save_dir, new_filename)

                resized_img.save(output_path, format=self.target_format.get())

            self.status_label.configure(
                text=f"Успешно сохранено: {new_filename}", 
                text_color="green"
            )
            messagebox.showinfo("Успех", f"Файл успешно сохранен в:\n{output_path}")

        except Exception as e:
            self.status_label.configure(text="Ошибка обработки", text_color="red")
            messagebox.showerror("Ошибка", f"Не удалось обработать изображение:\n{e}")


if __name__ == "__main__":
    app = ImageResizerApp()
    app.mainloop()